#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class ForwardedFromType(Enum):
    """
    **Represents the original sender of a forwarded message.**
        `from rubigram.enums import ForwardedFromType`

    Attributes:
        USER (str): The message was forwarded from a user.
        BOT (str): The message was forwarded from a bot.
        CHANNEL (str): The message was forwarded from a channel.
    """

    USER = "User"
    BOT = "Bot"
    CHANNEL = "Channel"
