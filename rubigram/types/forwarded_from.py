#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from .config import Object
import rubigram


@dataclass
class ForwardedFrom(Object):
    """
    **Represents information about the original sender of a forwarded message.**
        `from rubigram.types import ForwardedFrom`

    Includes the type of sender, the original message ID, and identifiers
    for the chat or sender from which the message was forwarded.

    Attributes:
        type_from (`Optional[rubigram.enums.ForwardedFromType]`):
            Type of the original sender (User, Bot, Channel).

        message_id (`Optional[str]`):
            ID of the original message.

        from_chat_id (`Optional[str]`):
            Chat ID where the original message was sent.

        from_sender_id (`Optional[str]`):
            Sender ID of the original message.
    """
    type_from: Optional[Union[str, rubigram.enums.ForwardedFromType]] = None
    message_id: Optional[str] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None