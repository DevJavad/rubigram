#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class MessageSenderType(Enum):
    """
    **Represents the sender type of a message.**
        `from rubigram.enums import MessageSenderType`

    Attributes:
        USER (str): The message was sent by a user.
        BOT (str): The message was sent by a bot.
    """

    USER = "User"
    BOT = "Bot"