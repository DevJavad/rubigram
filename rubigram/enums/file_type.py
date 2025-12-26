#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class FileType(Enum):
    """
    **Represents the different types of files that can be sent or received.**
        `from rubigram.enums import FileType`

    Attributes:
        FILE (str): A generic file.
        IMAGE (str): An image file.
        VIDEO (str): A video file.
        GIF (str): A GIF file.
        MUSIC (str): An audio/music file.
        VOICE (str): A voice message file.
    """

    FILE = "File"
    IMAGE = "Image"
    VIDEO = "Video"
    GIF = "Gif"
    MUSIC = "Music"
    VOICE = "Voice"