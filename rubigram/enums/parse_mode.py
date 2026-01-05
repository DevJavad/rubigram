#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class ParseMode(Enum):
    """
    **Represents the text parsing modes for messages.**
        `from rubigram.enums import ParseMode`

    Attributes:
        MARKDOWN (str): Parses the message as Markdown.
        HTML (str): Parses the message as HTML.
    """

    MARKDOWN = "Markdown"
    HTML = "Html"
    DISABLED = "Disable"