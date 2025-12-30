#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
import rubigram


class EditMessage:
    async def edit_message(
        self: rubigram.Client,
        chat_id: str,
        message_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None
    ):
        """
        Edit various aspects of a message or chat on Rubika.

        This is a convenience method that provides a unified interface for editing
        different parts of a message or chat. It automatically routes to the appropriate
        specific edit method based on the parameters provided.

        Parameters:
            chat_id (str):
                The chat ID containing the message or where the edit should occur.

            message_id (Optional[str], default: None):
                The ID of the message to edit (required for text and inline_keypad edits).

            text (Optional[str], default: None):
                New text content for the message.
                If provided, calls `edit_message_text()`.

            chat_keypad (Optional[rubigram.types.Keypad], default: None):
                New chat keypad to set.
                If provided, calls `edit_chat_keypad()`.

            inline_keypad (Optional[rubigram.types.Keypad], default: None):
                New inline keypad for a specific message.
                If provided, calls `edit_message_keypad()`.

            parse_mode (Optional[Union[str, rubigram.enums.ParseMode]], default: None):
                Text formatting mode for the text content.
                Only used when `text` parameter is provided.

        Returns:
            dict:
                The API response from the specific edit operation performed.

        Raises:
            ValueError:
                If no valid edit parameters are provided.
                If required parameters are missing for the chosen edit type.

        Example:
        .. code-block:: python
            from rubigram import types

            # Edit message text
            result = await client.edit_message(
                chat_id="123456",
                message_id="msg_789",
                text="Updated message text",
                parse_mode="Markdown"
            )

            # Edit chat keypad
            chat_kp = types.Keypad(rows=[[types.Button(text="Chat Button")]])
            result = await client.edit_message(
                chat_id="123456",
                chat_keypad=chat_kp
            )

            # Edit message inline keypad
            inline_kp = types.Keypad(rows=[[types.Button(text="Inline Button")]])
            result = await client.edit_message(
                chat_id="123456",
                message_id="msg_789",
                inline_keypad=inline_kp
            )

        Note:
            - Only one type of edit can be performed per call (text, chat_keypad, or inline_keypad)
            - The method determines which specific edit function to call based on parameter priority:
                1. `text` (requires message_id)
                2. `chat_keypad`
                3. `inline_keypad` (requires message_id)
            - `message_id` is required for text and inline_keypad edits
            - `parse_mode` is only used when editing text
        """
        if text:
            return await self.edit_message_text(chat_id, message_id, text, parse_mode)

        if chat_keypad:
            return await self.edit_chat_keypad(chat_id, chat_keypad)

        if inline_keypad:
            return await self.edit_message_keypad(chat_id, message_id, inline_keypad)