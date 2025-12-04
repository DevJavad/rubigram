#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnMessage:
    def on_message(
        self: "rubigram.Client",
        filters: Optional["Filter"] = None
    ):
        """
        **Decorator for handling incoming messages.**
            `@client.on_message(filters.text)`

        This decorator registers a function to handle incoming messages
        that match the specified filters. If no filters are provided,
        all messages will be handled.

        Args:
            filters (`Optional[Filter]`):
                Filter to determine which messages should be handled.
                If None, all messages will be processed.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Handle all text messages
            @client.on_message(filters.text)
            async def handle_text(client, update):
                await client.send_message(update.chat_id, "Text message received!")

            # Handle commands
            @client.on_message(filters.command("start"))
            async def handle_start(client, update):
                await client.send_message(update.chat_id, "Bot started!")

            # Handle all messages (no filter)
            @client.on_message()
            async def handle_all(client, update):
                print(f"Received message: {update.new_message.text}")
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

            self.new_message_handlers.append(wrapper)
            return func
        return decorator