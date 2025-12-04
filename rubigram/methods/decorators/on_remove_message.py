#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnRemoveMessage:
    def on_remove_message(
        self: "rubigram.Client",
        filters: Optional["Filter"] = None
    ):
        """
        **Decorator for handling deleted messages.**
            `@client.on_delete_message(filters.private)`

        This decorator registers a function to handle message deletion events
        that match the specified filters. If no filters are provided,
        all message deletions will be handled.

        Args:
            filters (`Optional[Filter]`):
                Filter to determine which message deletions should be handled.
                If None, all message deletions will be processed.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Handle all message deletions in private chats
            @client.on_delete_message(filters.private)
            async def handle_private_deletion(client, update):
                await client.send_message(
                    update.chat_id, 
                    "A message was deleted in this private chat!"
                )

            # Handle message deletions in specific chats
            @client.on_delete_message(filters.chat(["g0123456789", "g0987654321"]))
            async def handle_group_deletions(client, update):
                print(f"Message deleted in group: {update.chat_id}")

            # Handle all message deletions (no filter)
            @client.on_delete_message()
            async def handle_all_deletions(client, update):
                print(f"Message {update.removed_message_id} was deleted in {update.chat_id}")
        """
        def decorator(func: Callable) -> Callable:
            async def wrapper(
                client: "rubigram.Client",
                update: "rubigram.types.Update"
            ):
                if filters is None or await filters(client, update):
                    await func(client, update)
                    return True
                return False

            self.remove_message_handlers.append(wrapper)
            return func
        return decorator