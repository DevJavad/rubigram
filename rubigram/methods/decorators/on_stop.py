#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Callable
import rubigram


class OnStop:
    def on_stop(self: "rubigram.Client"):
        """
        **Decorator for handling application shutdown events.**
            `@client.on_stop()`

        This decorator registers a function to be executed when the
        Rubigram client is shutting down. This is useful for cleanup tasks,
        closing database connections, saving state, or performing any
        cleanup required before the bot stops completely.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Cleanup resources on shutdown
            @client.on_stop()
            async def cleanup_resources(client):
                # Close database connections
                # Save bot state
                # Clean up temporary files
                print("Resources cleaned up successfully!")

            # Send shutdown notification
            @client.on_stop()
            async def send_shutdown_notification(client):
                await client.send_message(
                    "b0ADMIN_USER_ID",
                    "Bot is shutting down for maintenance."
                )
                print("Shutdown notification sent!")

            # Backup data before shutdown
            @client.on_stop()
            async def backup_data(client):
                # Backup user data
                # Save logs
                # Export statistics
                print("Data backup completed!")

        Note:
            - This handler runs only once when the client is shutting down
            - Multiple shutdown handlers can be registered
            - All shutdown handlers run before the client completely stops
            - The client parameter provides access to all bot methods until shutdown completes
            - Useful for graceful shutdown and resource cleanup
        """
        def decorator(func: Callable) -> Callable:
            async def wrapper(client):
                return await func(client)

            self.stop_handlers.append(wrapper)
            return func
        return decorator