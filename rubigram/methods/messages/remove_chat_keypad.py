#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

import rubigram


class RemoveChatKeypad:
    async def remove_chat_keypad(
        self: rubigram.Client,
        chat_id: str
    ):
        """
        **Remove the custom keypad from a chat.**
            `await client.remove_chat_keypad(chat_id)`

        This method removes any custom keyboard (keypad) from the specified chat,
        restoring the default keyboard interface for all users in the chat.

        Args:
            chat_id (`str`):
                The ID of the chat where the keypad should be removed.

        Returns:
            dict: The API response from Rubigram.

        Example:
        .. code-block:: python

            # Remove custom keypad from a chat
            await client.remove_chat_keypad(chat_id=chat_id)

        Note:
            This action affects all users in the chat and cannot be undone
            without setting a new keypad.
        """
        return await self.request(
            "editChatKeypad",
            {
                "chat_id": chat_id,
                "chat_keypad_type": "Remove"
            }
        )