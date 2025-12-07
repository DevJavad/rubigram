#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union
import re
import rubigram


class Parser:
    @staticmethod
    def parse(
        text: str,
        type: Optional[Union[str, "rubigram.enums.ParseMode"]] = "markdown"
    ) -> dict:
        """
        **Parse text with specified formatting mode into structured metadata.**
            `Parser.parse("**bold** text", type="markdown")`

        This static method converts text with either Markdown or HTML formatting
        into a structured format with metadata that can be used by Rubigram's API.
        It supports parsing based on the specified parse mode.

        Args:
            text (`str`):
                The input text containing formatting markers.

            type (`Optional[Union[str, rubigram.enums.ParseMode]]`):
                The parsing mode to use. Can be "markdown", "html", or ParseMode enum.
                Defaults to "markdown".

        Returns:
            dict: A dictionary containing:
                - text: The cleaned text without formatting markers
                - metadata: Structured metadata with formatting information (if any)

        Example:
        .. code-block:: python

            # Parse Markdown text
            result = Parser.parse("**Hello** __world__", type="markdown")
            print(result["text"])  # Output: "Hello world"

            # Parse HTML text
            result = Parser.parse("<b>Bold</b> <i>italic</i>", type="html")
            print(result["text"])  # Output: "Bold italic"

            # Use ParseMode enum
            from rubigram.enums import ParseMode
            result = Parser.parse("**text**", type=ParseMode.MARKDOWN)

        Note:
            Supported Markdown formats:
            - **Bold**: `**text**`
            - __Italic__: `__text__`
            - --Underline--: `--text--`
            - ~~Strike~~: `~~text~~`
            - `Inline Code`: `` `text` ``
            - ```Preformatted```: ```text```
            - [Links]: `[text](url)`
            - > Quotes: `> text`
            - ||Spoiler||: `||text||`

            Supported HTML formats:
            - <b>Bold</b>
            - <i>Italic</i>
            - <u>Underline</u>
            - <s>Strike</s>
            - <code>Code</code>
            - <a href="url">Link</a>
            - <blockquote>Quote</blockquote>
            - <span class="spoiler">Spoiler</span>
        """
        meta_data_parts = []
        clean_text = text

        markdown_patterns = [
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

        html_patterns = [
            ("Bold", r"<b>(.*?)</b>"),
            ("Italic", r"<i>(.*?)</i>"),
            ("Underline", r"<u>(.*?)</u>"),
            ("Strike", r"<s>(.*?)</s>"),
            ("Pre", r"<code>(.*?)</code>"),
            ("Link", r'<a href="(.*?)">(.*?)</a>'),
            ("Quote", r"<blockquote>(.*?)</blockquote>"),
            ("Spoiler", r'<span class="spoiler">(.*?)</span>'),
        ]

        parse_mode = (
            type.value.lower()
            if hasattr(type, "value")
            else (type or "markdown").lower()
        )

        if parse_mode == "markdown":
            patterns = markdown_patterns
        elif parse_mode == "html":
            patterns = html_patterns
        else:
            return {"text": text}

        for item in patterns:
            if len(item) == 3:
                fmt, pattern, remove_len = item
                flags = 0
            elif len(item) == 4:
                fmt, pattern, remove_len, flags = item
            else:
                fmt, pattern = item
                remove_len = None
                flags = re.DOTALL

            text = clean_text
            offset = 0

            for match in re.finditer(pattern, text, flags):
                start, end = match.span()

                if fmt == "Link":
                    if parse_mode == "html":
                        url, content = match.group(1), match.group(2)
                    else:
                        content, url = match.group(1), match.group(2)
                else:
                    content, url = match.group(1), None

                from_index = start - offset

                meta_data_parts.append({
                    "from_index": from_index,
                    "length": len(content),
                    "type": fmt,
                    **({"link_url": url} if url else {})
                })

                clean_text = (
                    clean_text[:from_index]
                    + content
                    + clean_text[end - offset:]
                )
                offset += (end - start) - len(content)

        data = {"text": clean_text}
        if meta_data_parts:
            data["metadata"] = {"meta_data_parts": meta_data_parts}

        return data