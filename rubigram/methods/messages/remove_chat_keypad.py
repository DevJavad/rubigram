#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class RemoveChatKeypad:
    async def remove_chat_keypad(
        self: rubigram.Client,
        chat_id: str,
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
        Remove the chat keypad (keyboard) from a specific chat on Rubika.

        This method removes any existing custom keypad from the chat interface,
        reverting to the default chat input area.

        Parameters:
            chat_id (str):
                The chat ID from which the keypad will be removed.

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
                The API response from Rubika after removing the chat keypad.

        Example:
        .. code-block:: python
            # Remove chat keypad
            result = await client.remove_chat_keypad(
                chat_id="123456"
            )

            print(f"Chat keypad removed successfully: {result}")

        Note:
            - Uses "editChatKeypad" API method with "Remove" as the chat_keypad_type
            - You must have appropriate permissions to modify chat keypads
            - After removal, users will see the standard chat input interface
            - This is useful for cleaning up temporary or context-specific keypads
        """
        return await self.request(
            "editChatKeypad",
            {"chat_id": chat_id, "chat_keypad_type": "Remove"},
            headers, proxy, retries, delay, backoff, max_delay, timeout, connect_timeout, read_timeout
        )