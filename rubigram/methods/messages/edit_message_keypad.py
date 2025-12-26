#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import TYPE_CHECKING
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad
    


class EditMessageKeypad:
    async def edit_message_keypad(
        self: rubigram.Client,
        chat_id: str,
        message_id: str,
        inline_keypad: Keypad
    ):
        """
        **Edit the inline keyboard of a specific message.**
            `await client.edit_message_keypad(chat_id, message_id, inline_keypad)`

        This method updates the inline keyboard attached to an existing message.
        The inline keyboard appears below the message content and provides
        interactive buttons for users.

        Args:
            chat_id (`str`):
                The ID of the chat where the message is located.

            message_id (`str`):
                The ID of the message to update.

            inline_keypad (`rubigram.types.Keypad`):
                The new inline keyboard object containing rows of interactive buttons.

        Returns:
            dict: The API response from Rubigram.

        Example:
        .. code-block:: python

            from rubigram.types import Keypad, KeypadRow, Button

            # Create an inline keyboard
            inline_keypad = Keypad(
                rows=[
                    KeypadRow(buttons=[
                        Button(button_text="Like", id="like_btn"),
                        Button(button_text="Share", id="share_btn")
                    ])
                ]
            )

            # Update the message's inline keyboard
            await client.edit_message_keypad(
                chat_id=message_id,
                message_id=message_id,
                inline_keypad=inline_keypad
            )

        Note:
            This method only affects the inline keyboard of the specified message
            and does not modify the message text or other content.
        """
        return await self.request(
            "editMessageKeypad",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_keypad": inline_keypad.as_dict()
            }
        )