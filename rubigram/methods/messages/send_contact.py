#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union
from rubigram.utils import AutoDelete
import rubigram


class SendContact:
    async def send_contact(
        self: "rubigram.Client",
        chat_id: str,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None,
        chat_keypad_type: Optional[
            Union[str, "rubigram.enums.ChatKeypadType"]
        ] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Send a contact to a chat.**
            `await client.send_contact(chat_id, phone_number, first_name, last_name)`

        This method sends a contact card with phone number and name information
        to the specified chat. The contact can be saved directly to the user's
        device contacts.

        Args:
            chat_id (`str`):
                The ID of the chat where the contact will be sent.

            phone_number (`str`):
                The contact's phone number.

            first_name (`str`):
                The contact's first name.

            last_name (`Optional[str]`):
                The contact's last name. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Custom keyboard to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keyboard to attach to the message. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the message. Defaults to False.

            reply_to_message_id (`Optional[str]`):
                ID of the message to reply to. Defaults to None.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent contact message object.

        Example:
        .. code-block:: python

            # Send a contact with full details
            await client.send_contact(
                chat_id=chat_id,
                phone_number="+1234567890",
                first_name="John",
                last_name="Doe",
                disable_notification=True
            )

        Note:
            The contact information will be displayed as a clickable card
            that users can save to their device contacts.
        """
        data = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
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

        response = await self.request("sendContact", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.client = self

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message