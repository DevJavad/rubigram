#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class ChatKeypadType(Enum):
    """
    **Represents the types of keypads that can be applied to a chat.**
        `from rubigram.enums import ChatKeypadType`

    Attributes:
        New (str): Creates and applies a new keypad to the chat.
        Remove (str): Removes the existing keypad from the chat.
    """

    NEW = "New"
    REMOVE = "Remove"