import re
from typing import Union, Any


PATTERNS = [
    ("Pre", r"```([\s\S]*?)```"),
    ("Quote", r"^> ?(.+)$", re.MULTILINE),
    ("Bold", r"\*\*(.+?)\*\*"),
    ("Italic", r"__(.+?)__"),
    ("Underline", r"--(.+?)--"),
    ("Strike", r"~~(.+?)~~"),
    ("Mono", r"`([^`\n]+?)`"),
    ("Spoiler", r"\|\|(.+?)\|\|"),
    ("Link", r"\[(.+?)\]\((.+?)\)"),
]

MENTION_PREFIX: tuple = ("u", "b")


class Markdown:
    @staticmethod
    def parse(text: str) -> tuple[str, Union[dict[str, Any], None]]:
        plain = text
        matches = []
        metadata_parts: list[dict[str, Any]] = []

        for name, pattern, *flags in PATTERNS:
            flags = flags[0] if flags else 0

            for match in re.finditer(pattern, plain, flags):
                start, end = match.span()
                groups = match.groups()

                content = groups[0]
                data = {
                    "type": name, "start": start, "end": end, "content": content
                }

                if name == "Link":
                    content, url = groups
                    data["content"] = content
                    if url[0] in MENTION_PREFIX:
                        data["type"] = "MentionText"
                        data["mention_text_user_id"] = url
                    else:
                        data["link_url"] = url

                matches.append(data)

        for match in sorted(matches, key=lambda x: x["start"], reverse=True):
            plain = plain[:match["start"]] + \
                match["content"] + plain[match["end"]:]

        shift = 0

        for match in sorted(matches, key=lambda x: x["start"]):
            from_index = match["start"] - shift
            removed = (match["end"] - match["start"]) - len(match["content"])
            shift += removed

            part = {
                "type": match["type"],
                "from_index": from_index,
                "length": len(match["content"])
            }

            if "link_url" in match:
                part["link_url"] = match["link_url"]
            if "mention_text_user_id" in match:
                part["mention_text_user_id"] = match["mention_text_user_id"]

            metadata_parts.append(part)

        return plain, {"meta_data_parts": metadata_parts} if metadata_parts else None