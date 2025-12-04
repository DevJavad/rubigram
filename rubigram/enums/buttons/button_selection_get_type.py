#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonSelectionGetType(Enum):
    """
    **Represents the methods available to retrieve selection button data.**
        `from rubigram.enums import ButtonSelectionGetType`

    Attributes:
        LOCAL (str): Retrieve data locally.
        API (str): Retrieve data via API.
    """

    LOCAL = "Local"
    API = "Api"