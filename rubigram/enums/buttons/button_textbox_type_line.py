#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonTextboxTypeLine(Enum):
    """
    **Represents the line types available for textbox buttons.**
        `from rubigram.enums import ButtonTextboxTypeLine`

    Attributes:
        SINGLE_LINE (str): Textbox is a single-line input.
        MULTI_LINE (str): Textbox allows multiple lines.
    """

    SINGLE_LINE = "SingleLine"
    MULTI_LINE = "MultiLine"