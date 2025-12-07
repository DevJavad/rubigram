#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class ChatActionType(Enum):
    """
    **Represents the types of actions a user can perform in a chat.**
        `from rubigram.enums import ChatActionType`

    Attributes:
        TYPING (str): Indicates the user is typing a message.
        UPLOADING (str): Indicates the user is uploading a file.
        RECORDING (str): Indicates the user is recording a voice message.
    """

    TYPING = "Typing"
    UPLOADING = "Uploading"
    RECORDING = "Recording"