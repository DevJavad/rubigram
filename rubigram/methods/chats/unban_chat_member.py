#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class UnbanChatMember:
    async def unban_chat_member(
        self: rubigram.Client,
        chat_id: str,
        user_id: str,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> rubigram.types.Chat:
        """
        Unban a previously banned chat member.

        This method removes a user from the chat's ban list, allowing them
        to rejoin the chat. Useful for moderation and user management.

        Parameters:
            chat_id (str):
                The chat ID from which the member will be unbanned.
                Must be a non-empty string.

            user_id (str):
                The user ID to unban from the chat.
                Must be a non-empty string.

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
                The API response from Rubika after unbanning the member.
                Typically includes success status and chat information.

        Raises:
            ValueError:
                If `chat_id` or `user_id` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Unban a user from a chat
            result = await client.unban_chat_member(
                chat_id="chat_123456",
                user_id="user_789012"
            )
            
            if result.get("status") == "OK":
                print(f"User unbanned successfully from chat")
            else:
                print(f"Failed to unban user: {result}")
            
            # Unban with error handling
            try:
                result = await client.unban_chat_member(
                    chat_id="chat_123456",
                    user_id="user_789012"
                )
                print(f"Unban result: {result}")
            except Exception as e:
                print(f"Error unbanning user: {e}")

        Note:
            - You must have appropriate admin permissions in the chat
            - User must be previously banned for this to have effect
            - Works for groups and channels
            - Unbanned users can rejoin the chat normally
            - May fail if user is not banned or if bot lacks permissions
            - Useful for implementing forgiveness systems or temporary bans
        """
        if not chat_id or not user_id:
            raise ValueError("Parameters ('chat_id', 'user_id') is required")

        return await self.request(
            "unbanChatMember",
            {"chat_id": chat_id, "user_id": user_id},
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