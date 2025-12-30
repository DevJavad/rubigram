#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonTextboxTypeKeypad(Enum):
    """
    **Represents the keypad types available for textbox buttons.**
        `from rubigram.enums import ButtonTextboxTypeKeypad`

    Attributes:
        STRING (str): Textbox accepts string input.
        NUMBER (str): Textbox accepts numeric input.
    """

    STRING = "String"
    NUMBER = "Number"