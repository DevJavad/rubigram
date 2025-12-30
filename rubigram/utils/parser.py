from __future__ import annotations

from typing import Union, TYPE_CHECKING
import re

if TYPE_CHECKING:
    from rubigram.enums import ParseMode


MARKDOWN_PATTERNS: list = [
    ("Bold", r"\*\*(.*?)\*\*", 4),
    ("Italic", r"__(.*?)__", 4),
    ("Underline", r"--(.*?)--", 4),
    ("Strike", r"~~(.*?)~~", 4),
    ("Pre", r"```([\s\S]*?)```", 6, re.DOTALL),
    ("Mono", r"(?<!`)`([^`\n]+?)`(?!`)", 2),
    ("Link", r"\[(.*?)\]\((.*?)\)", None),
    ("Quote", r"^> (.+)$", None, re.MULTILINE),
    ("Spoiler", r"\|\|(.*?)\|\|", 4),
]
HTML_PATTERNS: list = [
    ("Bold", r"<b>(.*?)</b>"),
    ("Italic", r"<i>(.*?)</i>"),
    ("Underline", r"<u>(.*?)</u>"),
    ("Strike", r"<s>(.*?)</s>"),
    ("Pre", r"<code>(.*?)</code>"),
    ("Link", r'<a href="(.*?)">(.*?)</a>'),
    ("Quote", r"<blockquote>(.*?)</blockquote>"),
    ("Spoiler", r'<span class="spoiler">(.*?)</span>'),
]


class Parser:
    @staticmethod
    def parser(text: str, type: Union[str, ParseMode]) -> dict:
        metadata_parts = []
        data = text
        
        parse_mode = type.value.lower() if hasattr(type, "value") else type.lower()
        patterns = HTML_PATTERNS if parse_mode == "html" else MARKDOWN_PATTERNS
        mention_pattern = r"@@(.+?)\|(.+?)@@"
        offset = 0
        
        for match in re.finditer(mention_pattern, data):
            start, end = match.span()
            name, user_id = match.group(1), match.group(2)
            from_index = start - offset
            data = data[:from_index] + name + data[end - offset:]
            offset += (end - start) - len(name)
            
            metadata_parts.append({
                "from_index": from_index,
                "length": len(name),
                "type": "MentionText",
                "mention_text_user_id": user_id
            })
            
        for i in patterns:
            if len(i) == 3:
                format, pattern, _ = i
                flags = 0
                
            elif len(i) == 4:
                format, pattern, _, flags = i
            
            else:
                format, pattern = i
                flags = re.DOTALL
            
            tmp_text = data
            offset = 0
            
            for match in re.finditer(pattern, tmp_text, flags):
                start, end = match.span()
                if format == "Link":
                    if parse_mode == "html":
                        url, content = match.group(1), match.group(2)
                    else:
                        content, url = match.group(1), match.group(2)
                else:
                    content, url = match.group(1), None
                
                from_index = start - offset
                
                metadata_parts.append({
                    "from_index": from_index,
                    "length": len(content),
                    "type": format,
                    **({"link_url": url} if url else {})
                })
                
                data = data[:from_index] + content + data[end - offset:]
                offset += (end - start) - len(content)
        
        result = {"text": data}
        if metadata_parts:
            result["metadata"] = {"meta_data_parts": metadata_parts}
            
        return result