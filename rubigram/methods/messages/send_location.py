#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.utils import AutoDelete
import rubigram


class SendLocation:
    async def send_location(
        self: rubigram.Client,
        chat_id: str,
        latitude: str,
        longitude: str,
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
        Send a location to a chat on Rubika.

        This method allows you to share geographical coordinates (latitude and longitude)
        with users in a chat. The location will be displayed as an interactive map point.
        Supports additional features like keyboards, notifications, reply functionality,
        and auto-deletion.

        Parameters:
            chat_id (str):
                The target chat ID where the location will be sent.

            latitude (str):
                The latitude coordinate of the location.
                Example: "35.6892"

            longitude (str):
                The longitude coordinate of the location.
                Example: "51.3890"

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
                The message object representing the sent location.

        Example:
        .. code-block:: python
            # Send a location (Tehran coordinates)
            message = await client.send_location(
                chat_id="123456",
                latitude="35.6892",
                longitude="51.3890"
            )
            
            # Send a location with reply and auto-deletion
            message = await client.send_location(
                chat_id="123456",
                latitude="40.7128",
                longitude="-74.0060",
                reply_to_message_id="msg_789",
                auto_delete=180  # Delete after 3 minutes
            )
            
            # Send a location silently with custom keypad
            from rubigram import types
            
            keypad = types.Keypad(rows=[[
                types.Button(
                    text="Open in Maps",
                    action_type="OpenURL",
                    payload="https://maps.google.com/?q=35.6892,51.3890"
                )
            ]])
            message = await client.send_location(
                chat_id="123456",
                latitude="35.6892",
                longitude="51.3890",
                disable_notification=True,
                inline_keypad=keypad
            )
            
            print(f"Location sent with message ID: {message.message_id}")

        Note:
            - The location will be displayed as an interactive map point in the chat
            - Users can click on the location to open it in maps applications
            - Coordinates should be provided as strings, but numeric values will be converted
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `chat_id` attribute updated for consistency
            - Location messages are useful for sharing addresses, meeting points, or points of interest
        """
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude
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
            "sendLocation",
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
