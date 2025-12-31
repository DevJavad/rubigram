#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class GetChat:
    async def get_chat(
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
    ) -> rubigram.types.Chat:
        """
        Get information about a chat.

        This method retrieves detailed information about a specific chat,
        including group, channel, or private conversation details.

        Parameters:
            chat_id (str):
                The unique identifier of the chat to get information about.
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
            rubigram.types.Chat:
                A Chat object containing information about the requested chat.

        Raises:
            ValueError:
                If `chat_id` parameter is empty or invalid.

        Example:
        .. code-block:: python
            # Get chat information
            chat = await client.get_chat("chat_123456")
            
            # Access chat properties
            print(f"Chat ID: {chat.id}")
            print(f"Chat title: {chat.title}")
            print(f"Chat type: {chat.type}")
            print(f"Chat members count: {chat.members_count}")
            print(f"Chat description: {chat.description}")
            print(f"Chat username: {chat.username}")
            print(f"Chat is verified: {chat.is_verified}")
            print(f"Chat is restricted: {chat.is_restricted}")
            print(f"Chat is creator: {chat.is_creator}")
            print(f"Chat is admin: {chat.is_admin}")
            
            # Use chat info in your bot logic
            if chat.type == "Group":
                print(f"This is a group chat with {chat.members_count} members")
            elif chat.type == "Channel":
                print(f"This is a channel: {chat.title}")
            else:
                print(f"This is a private chat")

        Note:
            - You must have appropriate permissions to get information about the chat
            - Returns different information based on chat type (group, channel, private)
            - Some fields may be None depending on chat settings and permissions
            - Useful for validating chat access, displaying chat info, or making
              decisions based on chat properties
            - The response is automatically parsed into a Chat object
        """
        if not chat_id:
            raise ValueError("Parameter 'chat_id' must be a non-empty string")

        response = await self.request(
            "getChat",
            {"chat_id": chat_id},
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

        return rubigram.types.Chat.parse(response["chat"])