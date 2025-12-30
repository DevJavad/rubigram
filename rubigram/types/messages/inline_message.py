#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
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
    file: Optional[rubigram.types.File] = None
    location: Optional[rubigram.types.Location] = None
    aux_data: Optional[rubigram.types.AuxData] = None
    client: Optional[rubigram.Client] = None
    
    
    async def answer(
        self,
        text: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        return await self.client.send_message(
            self.chat_id,
            text,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            parse_mode,
            auto_delete
        )