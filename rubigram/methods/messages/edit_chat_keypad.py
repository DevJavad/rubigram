#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class EditChatKeypad:
    async def edit_chat_keypad(
        self: rubigram.Client,
        chat_id: str,
        chat_keypad: rubigram.types.Keypad,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ):
        """
        Edit the chat keypad (keyboard) for a specific chat on Rubika.

        This method allows you to update or set a custom keypad for a chat.
        The keypad will be displayed to users in the chat interface.

        Parameters:
            chat_id (str):
                The chat ID where the keypad will be edited.
                Must be a non-empty string.

            chat_keypad (rubigram.types.Keypad):
                The new keypad object to set for the chat.
                Must be a valid Keypad instance.

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
            dict:
                The API response from Rubika after editing the chat keypad.

        Raises:
            ValueError:
                If `chat_id` or `chat_keypad` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Create a new keypad
            from rubigram import types

            keypad = types.Keypad(
                rows=[
                    [
                        types.Button(
                            text="Button 1",
                            action_type="Custom",
                            payload="action_1"
                        )
                    ],
                    [
                        types.Button(
                            text="Button 2",
                            action_type="Custom",
                            payload="action_2"
                        ),
                        types.Button(
                            text="Button 3",
                            action_type="Custom",
                            payload="action_3"
                        )
                    ]
                ]
            )

            # Edit the chat keypad
            result = await client.edit_chat_keypad(
                chat_id="123456",
                chat_keypad=keypad
            )

            print(f"Keypad updated successfully: {result}")

        Note:
            - The keypad type is automatically set to "New" for new keypads
            - You must have appropriate permissions to edit chat keypads
            - The keypad will be visible to all users in the chat
            - Use `chat_keypad.as_dict()` to serialize the keypad object
        """
        return await self.request(
            "editChatKeypad",
            {
                "chat_id": chat_id,
                "chat_keypad_type": "New",
                "chat_keypad": chat_keypad.as_dict()
            },
            headers, proxy, retries, delay, backoff, max_delay, timeout, connect_timeout, read_timeout
        )