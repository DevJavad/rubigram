#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class EditMessageKeypad:
    async def edit_message_keypad(
        self: rubigram.Client,
        chat_id: str,
        message_id: str,
        inline_keypad: rubigram.types.Keypad,
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
        Edit the inline keypad (keyboard) of an existing message on Rubika.

        This method allows you to update or modify the inline keypad attached to a
        specific message. Useful for updating interactive buttons or menus.

        Parameters:
            chat_id (str):
                The chat ID containing the message to edit.
                Must be a non-empty string.

            message_id (str):
                The ID of the message whose inline keypad will be edited.
                Must be a non-empty string.

            inline_keypad (rubigram.types.Keypad):
                The new inline keypad object to attach to the message.
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
                The API response from Rubika after editing the message keypad.

        Raises:
            ValueError:
                If `chat_id`, `message_id`, or `inline_keypad` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Create a new inline keypad
            from rubigram import types
            
            new_keypad = types.Keypad(
                rows=[
                    [
                        types.Button(
                            text="Updated Button 1",
                            action_type="Custom",
                            payload="new_action_1"
                        )
                    ],
                    [
                        types.Button(
                            text="Updated Button 2",
                            action_type="OpenURL",
                            payload="https://example.com"
                        )
                    ]
                ]
            )
            
            # Edit the message's inline keypad
            result = await client.edit_message_keypad(
                chat_id="123456",
                message_id="msg_789",
                inline_keypad=new_keypad
            )
            
            print(f"Message keypad updated successfully: {result}")

        Note:
            - You can only edit inline keypads of messages sent by the bot
            - The original message must have an inline keypad to edit
            - Use `inline_keypad.as_dict()` to serialize the keypad object
            - This is useful for updating dynamic menus or button states
        """
        if not chat_id:
            raise ValueError("Parameter 'chat_id' must be a non-empty string")
        if not message_id:
            raise ValueError("Parameter 'message_id' must be a non-empty string")
        if not inline_keypad:
            raise ValueError("Parameter 'inline_keypad' must be a non-empty string")
        
        return await self.request(
            "editMessageKeypad",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_keypad": inline_keypad.as_dict()
            },
            headers,
            proxy,
            retries,
            delay,
            backoff,
            max_delay,
            timeout,
            connect_timeout,
            read_timeout
        )