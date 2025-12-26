#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from .config import Object

if TYPE_CHECKING:
    from rubigram.types import File


@dataclass
class Bot(Object):
    """
    **Represents a bot in Rubigram.**
        `from rubigram.types import Bot`

    Contains basic information about a bot, including its identifiers,
    description, avatar, and sharing information.

    Attributes:
        bot_id (`str`):
            Unique identifier for the bot.

        bot_title (`str`):
            Display title of the bot.

        avatar (`Optional[rubigram.types.File]`):
            The bot's avatar file object.

        description (`Optional[str]`):
            Description of the bot.

        username (`str`):
            The bot's username.

        start_message (`Optional[str]`):
            Default start message of the bot.

        share_url (`str`):
            Public URL for sharing the bot.
    """
    bot_id: str = None
    bot_title: str
    avatar: Optional[File] = None
    description: Optional[str] = None
    username: str = None
    start_message: Optional[str] = None
    share_url: str = None