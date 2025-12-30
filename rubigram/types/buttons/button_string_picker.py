#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from dataclasses import dataclass
from ..config import Object


@dataclass
class ButtonStringPicker(Object):
    """
    **Represents a string picker button.**
        `from rubigram.types import ButtonStringPicker`

    Attributes:
        items (`Optional[list[str]]`):
            List of string options to select from.

        default_value (`Optional[str]`):
            Default selected string.

        title (`Optional[str]`):
            Title of the string picker.
    """
    items: Optional[list[str]] = None
    default_value: Optional[str] = None
    title: Optional[str] = None