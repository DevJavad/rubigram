#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from datetime import datetime
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Run:
    """
    Long-polling update receiver for Rubika Bot API.

    This class provides methods for running the bot in long-polling mode,
    continuously fetching updates from the API and dispatching them to
    registered handlers. It includes timestamp validation to ensure only
    recent updates are processed.

    Note:
        This class is typically used as a mixin or extension to the
        Client class via monkey-patching or inheritance.

    Example:
    .. code-block:: python
        # Monkey-patch the client with run methods
        client = Client(token="YOUR_BOT_TOKEN")
        client.receiver = Run.receiver.__get__(client, Client)
        client.run = Run.run.__get__(client, Client)

        # Run the bot in polling mode
        client.run()
    """

    async def receiver(self: "rubigram.Client"):
        """
        Continuously receive and process updates via long-polling.

        This method:
        1. Starts the client
        2. Enters an infinite loop to fetch updates
        3. Validates update timestamps to prevent replay attacks
        4. Dispatches valid updates to handlers
        5. Manages the update offset for incremental fetching
        6. Stops the client on error or exit

        Workflow:
            - Fetches up to 100 updates at a time
            - Validates that message timestamps are recent (within 2 seconds)
            - Sets the client on each update for handler access
            - Updates the offset to avoid processing the same update twice
            - Continues polling until an error occurs

        Note:
            Timestamp validation ensures updates are not older than 2 seconds
            from current time to prevent processing delayed or replayed messages.

        Raises:
            Exception: Any error during update fetching or processing.

        Example:
        .. code-block:: python
            # Manual receiver usage
            await client.receiver()
        """
        await self.start()
        try:
            while True:
                updates = await self.get_updates(100, self.offset_id)
                if updates.updates:
                    for update in updates.updates:
                        time = update.update_time
                        now = int(datetime.now().timestamp())
                        if time and (time >= now or time + 2 >= now):
                            logger.debug("New Event, type: %s", update.type)
                            update.client = self
                            await self.dispatcher(update)

                        self.offset_id = updates.next_offset_id
        finally:
            await self.stop()

    def run(self: "rubigram.Client"):
        """
        Run the bot in long-polling mode (blocking call).

        This method:
        1. Creates and runs an asyncio event loop
        2. Executes the receiver method
        3. Handles KeyboardInterrupt for graceful shutdown
        4. Closes the event loop on exit

        Note:
            This is a blocking method that runs indefinitely until
            interrupted by Ctrl+C or a fatal error.

        Example:
        .. code-block:: python
            # Simple bot runner
            client = Client(token="YOUR_BOT_TOKEN")
            client.run = Run.run.__get__(client, Client)
            client.run()  # Blocks here
        """
        try:
            logger.info(
                "Run rubigram client, token: %s",
                self.token[:20] + "*" * max(0, len(self.token) - 20)
            )
            asyncio.run(self.receiver())
        except KeyboardInterrupt:
            logger.info(
                "Stop Runing rubigram client, token: %s",
                self.token[:20] + "*" * max(0, len(self.token) - 20)
            )