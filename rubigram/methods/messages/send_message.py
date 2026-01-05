#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.parser import Parser
from rubigram.utils import AutoDelete, clean_payload
import rubigram


class SendMessage:
    async def send_message(
        self: rubigram.Client,
        chat_id: str,
        text: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Union[str, rubigram.enums.ChatKeypadType] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        metadata: Optional[rubigram.types.Metadata] = None,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
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
        Send a text message to a chat on Rubika.

        This is the primary method for sending text messages with support for formatting,
        keyboards, notifications, reply functionality, parsing modes, and auto-deletion.

        Parameters:
            chat_id (str):
                The target chat ID where the message will be sent.

            text (str):
                The text content of the message to send.

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

            parse_mode (Optional[Union[str, rubigram.enums.ParseMode]], default: None):
                Text formatting mode for the message content.
                If not provided, uses the client's default parse_mode.

            auto_delete (Optional[int], default: None):
                Number of seconds after which the message will be automatically deleted.
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
                The message object representing the sent message.

        Example:
        .. code-block:: python
            # Send a simple text message
            message = await client.send_message(
                chat_id="123456",
                text="Hello, world!"
            )

            # Send a formatted message with Markdown
            message = await client.send_message(
                chat_id="123456",
                text="*Bold text* and _italic text_",
                parse_mode="Markdown"
            )

            # Send a message with inline keyboard
            from rubigram import types

            keypad = types.Keypad(rows=[[
                types.Button(
                    text="Click me",
                    action_type="Custom",
                    payload="button_clicked"
                )
            ]])
            message = await client.send_message(
                chat_id="123456",
                text="Choose an option:",
                inline_keypad=keypad,
                auto_delete=60  # Delete after 1 minute
            )

            # Send a reply message silently
            message = await client.send_message(
                chat_id="123456",
                text="This is a reply",
                reply_to_message_id="msg_789",
                disable_notification=True
            )

            print(f"Message sent with ID: {message.message_id}")

        Note:
            - Text is automatically parsed based on the specified parse_mode
            - Metadata from parsed text is included in the request if present
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `chat_id` attribute set for consistency
            - This is the most commonly used method for text-based communication
            - Supports multiple formatting styles (Markdown, HTML, etc.) through parse_mode
        """
        if metadata is None:
            text, metadata = Parser.parse(text, parse_mode or self.parse_mode)
            
        data = clean_payload({
            "chat_id": chat_id,
            "text": text,
            "metadata": metadata,
            "chat_keypad": chat_keypad.as_dict() if chat_keypad else None,
            "inline_keypad": inline_keypad.as_dict() if inline_keypad else None,
            "chat_keypad_type": chat_keypad_type,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id
        })

        response = await self.request(
            "sendMessage", data, headers, proxy, retries, delay, backoff, max_delay, timeout, connect_timeout, read_timeout
        )
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if (auto_delete := auto_delete or self.auto_delete) and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message