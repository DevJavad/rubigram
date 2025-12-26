#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from rubigram.utils import AutoDelete
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import ChatKeypadType


class SendSticker:
    async def send_sticker(
        self: rubigram.Client,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadType]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        **Send a sticker to a chat.**
            `await client.send_sticker(chat_id, sticker_id)`

        This method sends a sticker to the specified chat using its unique identifier.
        Stickers are graphical elements that can express emotions, reactions, or concepts.

        Args:
            chat_id (`str`):
                The ID of the chat where the sticker will be sent.

            sticker_id (`str`):
                The unique identifier of the sticker to send.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Custom keyboard to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keyboard to attach below the sticker. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad (New, Remove). Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the sticker. Defaults to False.

            reply_to_message_id (`Optional[str]`):
                ID of the message to reply to. Defaults to None.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent sticker message object with client binding.

        Example:
        .. code-block:: python

            # Send a sticker to a chat
            await client.send_sticker(
                chat_id=chat_id,
                sticker_id=sticker_id,
                disable_notification=True
            )

        Note:
            - Sticker IDs are unique identifiers for each sticker in Rubigram's sticker pack
            - Stickers are displayed as large, animated or static images
            - Users can tap on stickers to see them in full size
        """
        data = {
            "chat_id": chat_id,
            "sticker_id": sticker_id
        }

        if chat_keypad:
            data["chat_keypad"] = chat_keypad.as_dict()
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.as_dict()
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type
        if disable_notification:
            data["disable_notification"] = disable_notification
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        response = await self.request("sendSticker", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message