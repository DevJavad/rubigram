#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonSelectionType(Enum):
    """
    **Represents the different styles of selection buttons.**
        `from rubigram.enums import ButtonSelectionType`

    Attributes:
        TEXT_ONLY (str): A selection button with text only.
        TEXT_IMG_THU (str): A selection button with text and a thumbnail image.
        TEXT_IMG_BIG (str): A selection button with text and a large image.
    """

    TEXT_ONLY = "TextOnly"
    TEXT_IMG_THU = "TextImgThu"
    TEXT_IMG_BIG = "TextImgBig"