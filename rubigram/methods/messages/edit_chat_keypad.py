#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import rubigram


class EditChatKeypad:
    async def edit_chat_keypad(
        self: "rubigram.Client",
        chat_id: str,
        chat_keypad: "rubigram.types.Keypad"
    ):
        """
        **Edit the chat keypad for a specific chat.**
            `await client.edit_chat_keypad(chat_id, chat_keypad)`

        This method updates the custom keyboard (keypad) for the specified chat.
        The new keypad will be displayed to all users in the chat.

        Args:
            chat_id (`str`):
                The ID of the chat where the keypad should be updated.

            chat_keypad (`rubigram.types.Keypad`):
                The new keypad object containing rows of buttons and display settings.

        Returns:
            dict: The API response from Rubigram.

        Example:
        .. code-block:: python

            from rubigram.types import Keypad, KeypadRow, Button

            # Create a new keypad
            keypad = Keypad(
                rows=[
                    KeypadRow(buttons=[
                        Button(button_text="Option 1", id="btn1"),
                        Button(button_text="Option 2", id="btn2")
                    ])
                ],
                resize_keyboard=True
            )

            # Update the chat keypad
            await client.edit_chat_keypad(
                chat_id=chat_id,
                chat_keypad=keypad
            )

        Note:
            This method sets the keypad type to "New" by default, replacing
            any existing keypad in the chat.
        """

        return await self.request(
            "editChatKeypad",
            {
                "chat_id": chat_id,
                "chat_keypad_type": "New",
                "chat_keypad": chat_keypad.as_dict()
            }
        )