#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from dataclasses import dataclass
from ..config import Object


@dataclass
class ButtonNumberPicker(Object):
    """
    **Represents a number picker button.**
        `from rubigram.types import ButtonNumberPicker`

    Attributes:
        min_value (`Optional[str]`):
            Minimum selectable number.

        max_value (`Optional[str]`):
            Maximum selectable number.

        default_value (`Optional[str]`):
            Default selected number.

        title (`Optional[str]`):
            Title of the number picker.
    """

    min_value: Optional[str] = None
    max_value: Optional[str] = None
    default_value: Optional[str] = None
    title: Optional[str] = None