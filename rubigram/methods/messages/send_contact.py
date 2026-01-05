#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.utils import AutoDelete, clean_payload
import rubigram


class SendContact:
    async def send_contact(
        self: rubigram.Client,
        chat_id: str,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Union[str, rubigram.enums.ChatKeypadType] = None,
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
        Send a contact to a chat on Rubika.

        This method allows you to share contact information (phone number with name)
        with users in a chat. Supports additional features like keyboards,
        notifications, reply functionality, and auto-deletion.

        Parameters:
            chat_id (str):
                The target chat ID where the contact will be sent.

            phone_number (str):
                The phone number of the contact (including country code).
                Example: "+989123456789"

            first_name (str):
                The first name of the contact.

            last_name (Optional[str], default: None):
                The last name of the contact (optional).

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
                The message object representing the sent contact.

        Example:
        .. code-block:: python
            # Send a contact with basic information
            message = await client.send_contact(
                chat_id="123456",
                phone_number="+989123456789",
                first_name="John",
                last_name="Doe"
            )

            # Send a contact with reply and auto-deletion
            message = await client.send_contact(
                chat_id="123456",
                phone_number="+989876543210",
                first_name="Jane",
                last_name="Smith",
                reply_to_message_id="msg_789",
                auto_delete=120  # Delete after 2 minutes
            )

            # Send a contact silently with custom keypad
            from rubigram import types

            keypad = types.Keypad(rows=[[types.Button(text="Call", action_type="Call")]])
            message = await client.send_contact(
                chat_id="123456",
                phone_number="+989555555555",
                first_name="Support",
                disable_notification=True,
                chat_keypad=keypad
            )

            print(f"Contact sent with message ID: {message.message_id}")

        Note:
            - The contact will be clickable in the chat for easy saving or calling
            - Phone numbers should include country code (e.g., +98 for Iran)
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `client` attribute set for future operations
            - Users can directly save the contact to their phone from the message
        """
        data = clean_payload({
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "chat_keypad": chat_keypad.as_dict() if chat_keypad else None,
            "inline_keypad": inline_keypad.as_dict() if inline_keypad else None,
            "chat_keypad_type": chat_keypad_type,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id
        })

        response = await self.request(
            "sendContact",  data, headers, proxy, retries, delay, backoff, max_delay, timeout, connect_timeout, read_timeout
        )
        message = rubigram.types.UMessage.parse(response, self)
        message.client = self

        if (auto_delete := auto_delete or self.auto_delete) and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message