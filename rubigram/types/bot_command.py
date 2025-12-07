#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from dataclasses import dataclass
from .config import Object


@dataclass
class BotCommand(Object):
    """
    **Represents a command for a bot in Rubigram.**
        `from rubigram.types import Bot`

    Contains the command text and its description. Typically used
    to show available commands in the bot interface.

    Attributes:
        command (`str`):
            The command text (e.g., '/start').
        description (`str`):
            Description of what the command does.
    """
    command: str
    description: str