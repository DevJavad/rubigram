#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonCalendarType(Enum):
    """
    **Represents the calendar types available for calendar buttons.**
        `from rubigram.enums import ButtonCalendarType`

    Attributes:
        DATE_PERSIAN (str): Persian (Jalali) calendar type.
        DATE_GREGORIAN (str): Gregorian calendar type.
    """

    DATE_PERSIAN = "DatePersian"
    DATE_GREGORIAN = "DateGregorian"