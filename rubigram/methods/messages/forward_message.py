#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from rubigram.utils import AutoDelete
import rubigram


class ForwardMessage:
    async def forward_message(
        self: rubigram.Client,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False,
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
        Forward a message from one chat to another on Rubika.

        This method allows you to forward an existing message to a different chat.
        Supports notification control and automatic message deletion.

        Parameters:
            from_chat_id (str):
                The source chat ID from which the message will be forwarded.

            message_id (str):
                The ID of the message to forward.

            to_chat_id (str):
                The destination chat ID where the message will be forwarded.

            disable_notification (bool, default: False):
                If True, forwards the message silently (no notification).

            auto_delete (Optional[int], default: None):
                Number of seconds after which the forwarded message will be automatically deleted.
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
                The message object representing the forwarded message.

        Example:
        .. code-block:: python
            # Forward a message silently
            message = await client.forward_message(
                from_chat_id="source_chat_123",
                message_id="msg_456",
                to_chat_id="destination_chat_789",
                disable_notification=True
            )
            
            # Forward with auto-deletion
            message = await client.forward_message(
                from_chat_id="source_chat_123",
                message_id="msg_456",
                to_chat_id="destination_chat_789",
                auto_delete=60  # Delete after 60 seconds
            )
            
            print(f"Forwarded message ID: {message.message_id} to chat: {message.chat_id}")

        Note:
            - You need appropriate permissions to forward messages from/to the specified chats
            - The forwarded message retains its original content and media
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `chat_id` updated to the destination chat
            - Forwarded messages may have limitations based on chat privacy settings
        """
        response = await self.request(
            "forwardMessage",
            {
                "from_chat_id": from_chat_id,
                "message_id": message_id,
                "to_chat_id": to_chat_id,
                "disable_notification": disable_notification
            },
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
        message.chat_id = to_chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message