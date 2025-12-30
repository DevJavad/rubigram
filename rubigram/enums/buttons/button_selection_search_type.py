#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonSelectionSearchType(Enum):
    """
    **Represents the search modes available for selection buttons.**
        `from rubigram.enums import ButtonSelectionSearchType`

    Attributes:
        LOCAL (str): Search is performed locally.
        API (str): Search is performed via API.
    """

    LOCAL = "Local"
    API = "Api"