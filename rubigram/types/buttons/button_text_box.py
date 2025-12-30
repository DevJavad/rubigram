#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object
import rubigram


@dataclass
class ButtonTextbox(Object):
    """
    **Represents a textbox input button.**
        `from rubigram.types import ButtonTextbox`

    Attributes:
        type_line (`Optional[Union[str, rubigram.enums.ButtonTextboxTypeLine]]`):
            Line type for the textbox.

        type_keypad (`Optional[Union[str, rubigram.enums.ButtonTextboxTypeKeypad]]`):
            Keypad type for the textbox.

        place_holder (`Optional[str]`):
            Placeholder text.

        title (`Optional[str]`):
            Title of the textbox.

        default_value (`Optional[str]`):
            Default text in the textbox.
    """
    type_line: Optional[Union[str, rubigram.enums.ButtonTextboxTypeLine]] = None
    type_keypad: Optional[Union[str, rubigram.enums.ButtonTextboxTypeKeypad]] = None
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None