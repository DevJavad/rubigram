#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import rubigram


class EditMessage:
    async def edit_message(
        self: "rubigram.Client",
        chat_id: str,
        message_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None
    ):
        """
        **Edit various components of a message or chat.**
            `await client.edit_message(chat_id, message_id, text=text, inline_keypad=keypad)`

        This method provides a unified way to update message text, chat keypads,
        and inline keyboards in a single call. You can update one or more
        components simultaneously.

        Args:
            chat_id (`str`):
                The ID of the chat where the edits should be applied.

            message_id (`Optional[str]`):
                The ID of the message to edit (required for text and inline keyboard edits).

            text (`Optional[str]`):
                New text content for the message. If provided, updates the message text.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                New chat keypad to set for the chat. Updates the keyboard for all users.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                New inline keyboard to attach to the message. Updates buttons below the message.

        Returns:
            None: This method doesn't return a value as it may perform multiple operations.

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

            # Edit message text and inline keyboard
            await client.edit_message(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                inline_keypad=inline_keypad
            )

        Note:
            - At least one of `text`, `chat_keypad`, or `inline_keypad` must be provided
            - `message_id` is required when editing text or inline keyboards
            - Chat keypad updates affect the entire chat, not just a specific message
        """
        if text:
            return await self.edit_message_text(chat_id, message_id, text)

        if chat_keypad:
            return await self.edit_chat_keypad(chat_id, chat_keypad)

        if inline_keypad:
            return await self.edit_message_keypad(chat_id, message_id, inline_keypad)