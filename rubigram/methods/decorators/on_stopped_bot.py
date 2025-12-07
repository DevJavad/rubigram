#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnStoppedBot:
    def on_stopped_bot(
        self: "rubigram.Client",
        filters: Optional["Filter"] = None
    ):
        """
        **Decorator for handling bot stop events.**
            `@client.on_stop_bot(filters.private)`

        This decorator registers a function to handle bot stop events
        that match the specified filters. If no filters are provided,
        all bot stop events will be handled.

        Args:
            filters (`Optional[Filter]`):
                Filter to determine which bot stop events should be handled.
                If None, all bot stop events will be processed.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Handle bot stops in private chats only
            @client.on_stop_bot(filters.private)
            async def handle_private_stop(client, update):
                await client.send_message(
                    update.chat_id, 
                    "Sorry to see you go! You can always start me again with /start."
                )

            # Handle bot stops from specific users
            @client.on_stop_bot(filters.chat(["b0123456789", "b0987654321"]))
            async def handle_specific_users_stop(client, update):
                print(f"Bot stopped by user: {update.chat_id}")

            # Handle all bot stop events (no filter)
            @client.on_stop_bot()
            async def handle_all_stops(client, update):
                print(f"Bot stopped in chat: {update.chat_id}")

        Note:
            This handler triggers when the bot is stopped by a user,
            typically when they block the bot or use a /stop command.
            The chat ID is available in `update.chat_id`.
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

            self.stopped_bot_handlers.append(wrapper)
            return func
        return decorator