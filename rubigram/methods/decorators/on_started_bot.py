#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnStartedBot:
    def on_started_bot(
        self: "rubigram.Client",
        filters: Optional["Filter"] = None
    ):
        """
        **Decorator for handling bot start events.**
            `@client.on_start_bot(filters.private)`

        This decorator registers a function to handle bot start events
        that match the specified filters. If no filters are provided,
        all bot start events will be handled.

        Args:
            filters (`Optional[Filter]`):
                Filter to determine which bot start events should be handled.
                If None, all bot start events will be processed.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Handle bot starts in private chats only
            @client.on_start_bot(filters.private)
            async def handle_private_start(client, update):
                await client.send_message(
                    update.chat_id, 
                    "Welcome to the bot! Use /help for commands."
                )

            # Handle bot starts from specific users
            @client.on_start_bot(filters.chat(["b0123456789", "b0987654321"]))
            async def handle_specific_users(client, update):
                print(f"Bot started by user: {update.chat_id}")

            # Handle all bot start events (no filter)
            @client.on_start_bot()
            async def handle_all_starts(client, update):
                print(f"Bot started in chat: {update.chat_id}")

        Note:
            This handler triggers when the bot is started by a user,
            typically when they first interact with the bot or use a /start command.
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

            self.started_bot_handlers.append(wrapper)
            return func
        return decorator