#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import rubigram


class GetChat:
    async def get_chat(
        self: "rubigram.Client",
        chat_id: str
    ) -> "rubigram.types.Chat":
        """
        **Get information about a specific chat.**
            `await client.get_chat(chat_id)`

        This method retrieves detailed information about a chat, including
        its type, title, user information (for private chats), and other
        metadata.

        Args:
            chat_id (`str`):
                The unique identifier of the chat to retrieve information for.

        Returns:
            rubigram.types.Chat: A Chat object containing the chat information.

        Example:
        .. code-block:: python

            # Get information about a chat
            chat = await client.get_chat(chat_id=chat_id)
            print(f"Chat title: {chat.title}")
            print(f"Chat type: {chat.chat_type}")
            print(f"Username: {chat.username}")

            # For private chats, access user information
            if chat.chat_type == rubigram.enums.ChatType.USER:
                print(f"User full name: {chat.full_name}")

        Note:
            - Works for all chat types (private, group, supergroup, channel)
            - For private chats, returns user information
            - For groups/channels, returns group metadata and settings
        """
        response = await self.request(
            "getChat",
            {
                "chat_id": chat_id
            }
        )
        return rubigram.types.Chat.parse(response["chat"])