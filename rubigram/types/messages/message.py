#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object
import html
import rubigram


@dataclass
class Message(Object):
    """
    **Represents a message in Rubigram.**
        `from rubigram.types import Message`

    This object can represent different types of messages including text, files,
    stickers, contacts, polls, live locations, and forwarded messages.

    Attributes:
        message_id (`str`):
            Unique identifier of the message.

        text (`Optional[str]`):
            Text content of the message.

        time (`Optional[str]`):
            Timestamp of when the message was sent.

        is_edited (`Optional[bool]`):
            Whether the message has been edited.

        sender_type (`Optional[rubigram.enums.MessageSenderType]`):
            Type of the sender (User or Bot).

        sender_id (`Optional[str]`):
            Unique identifier of the sender.

        aux_data (`Optional[rubigram.types.AuxData]`):
            Additional data attached to the message.

        file (`Optional[rubigram.types.File]`):
            File attached to the message.

        reply_to_message_id (`Optional[str]`):
            ID of the message this is replying to.

        forwarded_from (`Optional[rubigram.types.ForwardedFrom]`):
            Information about the original sender if forwarded.

        forwarded_no_link (`Optional[str]`):
            Forwarded message without link.

        location (`Optional[rubigram.types.Location]`):
            Location attached to the message.

        sticker (`Optional[rubigram.types.Sticker]`):
            Sticker attached to the message.

        contact_message (`Optional[rubigram.types.ContactMessage]`):
            Contact information attached to the message.

        poll (`Optional[rubigram.types.Poll]`):
            Poll attached to the message.

        live_location (`Optional[rubigram.types.LiveLocation]`):
            Live location attached to the message.

        metadata (`Optional[rubigram.types.MetaData]`):
            Metadata describing text formatting, links, mentions, etc.            

        client (`Optional[rubigram.Client]`):
            The Rubigram client associated with the message.
    """
    message_id: str
    text: Optional[str] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    sender_type: Optional[Union[str, rubigram.enums.MessageSenderType]] = None
    sender_id: Optional[str] = None
    aux_data: Optional[rubigram.types.AuxData] = None
    file: Optional[rubigram.types.File] = None
    reply_to_message_id: Optional[str] = None
    forwarded_from: Optional[rubigram.types.ForwardedFrom] = None
    forwarded_no_link: Optional[str] = None
    location: Optional[rubigram.types.Location] = None
    sticker: Optional[rubigram.types.Sticker] = None
    contact_message: Optional[rubigram.types.ContactMessage] = None
    poll: Optional[rubigram.types.Poll] = None
    live_location: Optional[rubigram.types.LiveLocation] = None
    metadata: Optional[rubigram.types.Metadata] = None
    client: Optional[rubigram.Client] = None

    @property
    def mention(self):
        """
        **Generate an HTML mention for the message sender.**

        Usage:
            message.mention()
            message.mention("Custom Name")

        Returns:
            callable: Function that returns HTML mention string.
        """
        def func(text: Optional[str] = None) -> str:
            if not self.sender_id:
                raise ValueError("Cannot mention without sender_id")

            name = html.escape(text or self.sender_id)
            return f"@@{name}|{self.sender_id}@@"

        return func