from __future__ import annotations

from rubigram.filters import Filter
from typing import Callable, Optional


class Handler:
    """
    Initialize a new handler.

    Parameters:
        callback (Callable):
            Async function to call when handler is triggered.
            Function signature: async def callback(client: rubigram.Client, update)

        filters (Optional[Filter], default: None):
            Optional filters to apply before executing the callback.
            If provided, the handler only runs if filters pass.

    Example:
        # Create a handler that only responds to messages containing "help"
        from rubigram.filters import command

        async def help_handler(client, update):
            await update.reply("Here is some help...")

        handler = Handler(
            callback=help_handler,
            filters=command("help")
        )
    """

    def __init__(
        self,
        callback: Callable,
        filters: Optional[Filter] = None
    ):
        self.callback = callback
        self.filters = filters

    async def check(self, client, update) -> bool:
        """
        Check if the handler should run for a given update.

        Parameters:
            client (rubigram.Client):
                The bot client instance.

            update:
                The update object to check.

        Returns:
            bool:
                True if the handler should run (filters pass or no filters),
                False otherwise.

        Note:
            - If no filters are set, returns True (handler always runs)
            - If filters are set, returns result of filter evaluation
            - Filters are evaluated asynchronously
        """

        if self.filters is None:
            return True
        return await self.filters(client, update)

    async def run(self, client, update):
        """
        Execute the handler's callback.

        Parameters:
            client (rubigram.Client):
                The bot client instance.

            update:
                The update object to process.

        Note:
            - Only called if check() returns True
            - Executes the registered callback function
            - Should handle any exceptions within the callback
        """
        await self.callback(client, update)