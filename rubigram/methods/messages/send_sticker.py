#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.utils import AutoDelete
import rubigram


class SendSticker:
    async def send_sticker(
        self: rubigram.Client,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> rubigram.types.UMessage:
        """
        Send a sticker to a chat on Rubika.

        This method allows you to send stickers using their unique sticker ID.
        Supports additional features like keyboards, notifications, reply functionality,
        and auto-deletion.

        Parameters:
            chat_id (str):
                The target chat ID where the sticker will be sent.

            sticker_id (str):
                The unique identifier of the sticker to send.
                Sticker IDs can be obtained from Rubika's sticker packs or APIs.

            chat_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach to the chat message.

            inline_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach inline with the message.

            chat_keypad_type (Optional[Union[str, rubigram.enums.ChatKeypadType]], default: None):
                Type of chat keyboard (e.g., "New", "Remove", or enum value).

            disable_notification (bool, default: False):
                If True, sends the message silently.

            reply_to_message_id (Optional[str], default: None):
                ID of a message to reply to.

            auto_delete (Optional[int], default: None):
                Number of seconds after which the sticker message will be automatically deleted.
                If None or 0, no auto-deletion will be scheduled.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for requests.

            retries (Optional[int], default: None):
                Number of retry attempts on request failure.

            delay (Optional[float], default: None):
                Initial delay between retries in seconds.

            backoff (Optional[float], default: None):
                Backoff multiplier applied after each retry.

            max_delay (Optional[float], default: None):
                Maximum delay between retries.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            rubigram.types.UMessage:
                The message object representing the sent sticker.

        Example:
        .. code-block:: python
            # Send a sticker
            message = await client.send_sticker(
                chat_id="123456",
                sticker_id="sticker_1234567890"
            )
            
            # Send a sticker with reply and auto-deletion
            message = await client.send_sticker(
                chat_id="123456",
                sticker_id="sticker_0987654321",
                reply_to_message_id="msg_789",
                auto_delete=90  # Delete after 1.5 minutes
            )
            
            # Send a sticker silently with custom keypad
            from rubigram import types
            
            keypad = types.Keypad(rows=[[
                types.Button(
                    text="Send Another",
                    action_type="Custom",
                    payload="send_another_sticker"
                )
            ]])
            message = await client.send_sticker(
                chat_id="123456",
                sticker_id="sticker_5555555555",
                disable_notification=True,
                inline_keypad=keypad
            )
            
            print(f"Sticker sent with message ID: {message.message_id}")

        Note:
            - Sticker IDs are unique identifiers provided by Rubika's sticker system
            - You need valid sticker IDs from existing sticker packs
            - Stickers are typically animated or static images in .webp format
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `chat_id` attribute updated for consistency
            - Useful for sending emotions, reactions, or decorative elements in chats
            - Stickers don't support captions or text content (only the sticker itself)
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

        response = await self.request(
            "sendSticker",
            data,
            headers,
            proxy,
            retries,
            delay,
            backoff,
            max_delay,
            timeout,
            connect_timeout,
            read_timeout
        )
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message