#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object
import rubigram


@dataclass
class ButtonCalendar(Object):
    """
    **Represents a calendar picker button.**
        `from rubigram.types import ButtonCalendar`

    Attributes:
        default_value (`Optional[str]`):
            The default selected date.

        type (`Optional[Union[str, rubigram.enums.ButtonCalendarType]]`):
            Type of calendar picker.

        min_year (`Optional[str]`):
            Minimum selectable year.

        max_year (`Optional[str]`):
            Maximum selectable year.

        title (`Optional[str]`):
            Title of the calendar picker.
    """
    default_value: Optional[str] = None
    type: Optional[Union[str, rubigram.enums.ButtonCalendarType]] = None
    min_year: Optional[str] = None
    max_year: Optional[str] = None
    title: Optional[str] = None