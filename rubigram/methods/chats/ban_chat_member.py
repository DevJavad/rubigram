#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class BanChatMember:
    async def ban_chat_member(
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
        Ban a member from a chat.

        This method removes a user from a chat and prevents them from rejoining.
        Useful for moderation and maintaining chat rules.

        Parameters:
            chat_id (str):
                The chat ID from which the member will be banned.
                Must be a non-empty string.

            user_id (str):
                The user ID to ban from the chat.
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
                The API response from Rubika after banning the member.
                Typically includes success status and chat information.

        Raises:
            ValueError:
                If `chat_id` or `user_id` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Ban a user from a chat
            result = await client.ban_chat_member(
                chat_id="chat_123456",
                user_id="user_789012"
            )
            
            if result.get("status") == "OK":
                print(f"User banned successfully from chat")
            else:
                print(f"Failed to ban user: {result}")
            
            # Ban with error handling
            try:
                result = await client.ban_chat_member(
                    chat_id="chat_123456",
                    user_id="user_789012"
                )
                print(f"Ban result: {result}")
            except Exception as e:
                print(f"Error banning user: {e}")

        Note:
            - You must have appropriate admin permissions in the chat
            - Banned users cannot rejoin the chat unless unbanned
            - Works for groups and channels
            - Consider using with other moderation methods (kick, restrict, etc.)
            - May fail if user is already banned or if bot lacks permissions
            - Useful for automated moderation systems
        """
        if not chat_id or not user_id:
            raise ValueError("Parameters ('chat_id', 'user_id') is required")

        return await self.request(
            "banChatMember",
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