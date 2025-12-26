#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from rubigram.utils import AutoDelete, Parser
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import ChatKeypadType, ParseMode
    

class SendMessage:
    async def send_message(
        self: rubigram.Client,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadType]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        parse_mode: Optional[Union[str, ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        **Send a text message to a chat.**
            `await client.send_message(chat_id, text)`

        This method sends a text message to the specified chat with optional
        keyboards, notification settings, and reply functionality.

        Args:
            chat_id (`str`):
                The ID of the chat where the message will be sent.

            text (`str`):
                The text content of the message.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Custom keyboard to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keyboard to attach below the message. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad (New, Remove). Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the message. Defaults to False.

            reply_to_message_id (`Optional[str]`):
                ID of the message to reply to. Defaults to None.
            
            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent message object with client binding.

        Example:
        .. code-block:: python

            from rubigram.types import Keypad, KeypadRow, Button

            # Create an inline keyboard
            inline_keypad = Keypad(rows=[
                KeypadRow(buttons=[
                    Button(button_text="Option 1", id="btn1"),
                    Button(button_text="Option 2", id="btn2")
                ])
            ])

            # Send a message with inline keyboard
            await client.send_message(
                chat_id=chat_id,
                text=text,
                inline_keypad=inline_keypad,
                disable_notification=True
            )

        Note:
            The returned UMessage object includes methods for editing,
            deleting, and forwarding the message.
        """
        
        data = {"chat_id": chat_id, "text": text}
        
        parse = Parser.parser(text, parse_mode or self.parse_mode)
        
        if "metadata" in parse:
            data["text"] = parse["text"]
            data["metadata"] = parse["metadata"]

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

        
        response = await self.request("sendMessage", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id
        
        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)
            
        return message