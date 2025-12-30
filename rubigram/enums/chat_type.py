#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class ChatType(Enum):
    """
    **Represents different types of chats.**
        `from rubigram.enums import ChatType`

    Attributes:
        User: Standard private chat with a user.
        Bot: Chat with an automated bot.
        Group: Multi-user group conversation.
        Channel: One-way broadcast chat.
    """

    USER = "User"
    BOT = "Bot"
    GROUP = "Group"
    CHANNEL = "Channel"