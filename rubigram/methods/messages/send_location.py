#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, TYPE_CHECKING
from rubigram.utils import AutoDelete
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import ChatKeypadType


class SendLocation:
    async def send_location(
        self: rubigram.Client,
        chat_id: str,
        latitude: str,
        longitude: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadType]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        **Send a location to a chat.**
            `await client.send_location(chat_id, latitude, longitude)`

        This method sends a geographical location to the specified chat.
        The location appears as an interactive map that users can tap to
        open in their maps application.

        Args:
            chat_id (`str`):
                The ID of the chat where the location will be sent.

            latitude (`str`):
                The latitude coordinate of the location.

            longitude (`str`):
                The longitude coordinate of the location.

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
            rubigram.types.UMessage: The sent location message object.

        Example:
        .. code-block:: python

            # Send a location (Tokyo coordinates)
            await client.send_location(
                chat_id=chat_id,
                latitude="35.6895",
                longitude="139.6917",
                disable_notification=True
            )

        Note:
            The location will be displayed as an interactive map preview
            that users can tap to open in their preferred maps application.
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

        response = await self.request("sendLocation", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message
