#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from dataclasses import dataclass
from ..config import Object
import rubigram


@dataclass
class InlineMessage(Object):
    """
    **Represents an inline message in Rubigram.**
        `from rubigram.types import InlineMessage`

    Inline messages are sent in response to inline queries and may include text,
    files, location, or auxiliary data.

    Attributes:
        chat_id (`str`):
            ID of the chat where the message is sent.

        sender_id (`Optional[str]`):
            ID of the sender.

        text (`Optional[str]`):
            Text content of the message.

        message_id (`Optional[str]`):
            Unique identifier of the message.

        file (`Optional[rubigram.types.File]`):
            File attached to the message.

        location (`Optional[rubigram.types.Location]`):
            Location attached to the message.

        aux_data (`Optional[rubigram.types.AuxData]`):
            Additional data attached to the message.

        client (`Optional[rubigram.Client]`):
            The Rubigram client associated with the message.
    """
    chat_id: str
    sender_id: Optional[str] = None
    text: Optional[str] = None
    message_id: Optional[str] = None
    file: Optional["rubigram.types.File"] = None
    location: Optional["rubigram.types.Location"] = None
    aux_data: Optional["rubigram.types.AuxData"] = None
    client: Optional["rubigram.Client"] = None