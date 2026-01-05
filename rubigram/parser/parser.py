from markdownify import markdownify
from .markdown import Markdown


class Parser:
    @staticmethod
    def parse(text: str, parse_mode: str):
        if parse_mode.lower() == "markdown":
            return Markdown.parse(text)

        elif parse_mode.lower() == "html":
            text = markdownify(text)
            return Markdown.parse(text)

        else:
            return text, None