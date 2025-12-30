#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Callable
import rubigram


class OnStart:
    def on_start(self: "rubigram.Client"):
        """
        **Decorator for handling application startup events.**
            `@client.on_start()`

        This decorator registers a function to be executed when the
        Rubigram client starts up and connects to the server. This is
        useful for initialization tasks, setting up webhooks, or
        performing any setup required before the bot starts processing updates.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Initialize bot on startup
            @client.on_start()
            async def initialize_bot(client):
                await client.set_commands([
                    rubigram.types.BotCommand(command="start", description="Start the bot"),
                    rubigram.types.BotCommand(command="help", description="Get help")
                ])
                print("Bot started and commands registered!")

            # Set up webhook on startup
            @client.on_start()
            async def setup_webhook(client):
                await client.update_bot_endpoints(
                    url="https://api.example.com/webhook",
                    type="ReceiveUpdate"
                )
                print("Webhook configured successfully!")

            # Perform database initialization
            @client.on_start()
            async def init_database(client):
                # Initialize database connections
                # Create necessary tables
                # Load initial data
                print("Database initialized!")

        Note:
            - This handler runs only once when the client starts
            - Multiple startup handlers can be registered
            - All startup handlers run before the client begins processing updates
            - The client parameter provides access to all bot methods
        """
        def decorator(func: Callable) -> Callable:
            async def wrapper(client):
                return await func(client)

            self.start_handlers.append(wrapper)
            return func
        return decorator