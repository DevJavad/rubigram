#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonLocationType(Enum):
    """
    **Represents the types of location buttons.**
        `from rubigram.enums import ButtonLocationType`

    Attributes:
        PICKER (str): A button to pick a location.
        VIEW (str): A button to view a location.
    """

    PICKER = "Picker"
    VIEW = "View"