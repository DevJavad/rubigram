#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import time
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Run:
    def is_update_recent(self, update_time: int, max_delay: int = 1) -> bool:
        now = int(time.time())
        return update_time + max_delay >= now

    async def receiver(
        self: "rubigram.Client",
        limit: int = 100,
        idle_sleep: float = 0.5
    ):
        """
        Continuous update receiver loop.

        This internal method runs the main polling loop that:
        1. Starts the client
        2. Continuously fetches updates
        3. Dispatches updates to handlers
        4. Manages offset tracking
        5. Handles idle periods

        Parameters:
            limit (int, default: 100):
                Updates per request limit.

            idle_sleep (float, default: 0.5):
                Sleep duration when no updates available.

        Note:
            - Runs in an infinite loop until interrupted
            - Sets update.client for handler context
            - Uses dispatcher to route updates to handlers
            - Logs each received update for debugging
            - Ensures proper cleanup with finally block
        """
        await self.start()
        try:
            while True:
                updates = await self.get_updates(limit, self.offset_id)

                if not updates.updates:
                    await asyncio.sleep(idle_sleep)
                    continue

                for update in updates.updates:
                    if self.is_update_recent(update.update_time):
                        logger.debug(
                            "Receive update | type=%s | chat=%s | time=%s",
                            update.type, update.chat_id, update.update_time
                        )
                        update.client = self
                        await self.dispatcher.dispatch(update)

                self.offset_id = updates.next_offset_id

        finally:
            await self.stop()

    def run(
        self: "rubigram.Client",
        limit: int = 100,
        idle_sleep: float = 1
    ):
        """
        Start the bot and begin receiving updates.

        This method runs the main event loop that continuously polls for updates
        from Rubika and dispatches them to appropriate handlers. It manages the
        bot's lifecycle including startup, update processing, and shutdown.

        Parameters:
            limit (int, default: 100):
                Maximum number of updates to retrieve per polling request.
                Higher values may improve performance but increase memory usage.

            idle_sleep (float, default: 1):
                Sleep duration in seconds when no updates are available.
                Controls polling frequency during idle periods.

        Example:
        .. code-block:: python
            # Basic bot setup
            from rubigram import Client, Dispatcher

            client = Client("YOUR_BOT_TOKEN")

            # Add message handlers
            @client.on_message()
            async def handle_message(message):
                await message.reply("Hello!")

            # Run the bot with default settings
            client.run()

            # Run with custom settings
            client.run(
                limit=50,        # Retrieve 50 updates per request
                idle_sleep=0.1   # Check every 0.1 seconds when idle
            )

            # With custom dispatcher and additional setup
            dp = Dispatcher()

            @dp.message()
            async def custom_handler(message):
                await message.answer("Custom handler response")

            client.dispatcher = dp
            client.run()

        Note:
            - Automatically calls `start()` before beginning update processing
            - Automatically calls `stop()` on shutdown or error
            - Uses `get_updates()` for long polling
            - Filters out old/stale updates based on update time
            - Sets `update.client` for handler access to client methods
            - Logs update reception for debugging
            - Handles KeyboardInterrupt (Ctrl+C) gracefully
            - Maintains offset_id for proper update sequencing
            - Update handlers should be registered before calling run()
            - Consider using webhooks for production instead of polling
        """

        try:
            logger.info(
                "Start rubigram client | first_offset_id=%s | idle_sleep=%s",
                self.offset_id, idle_sleep
            )
            asyncio.run(self.receiver(limit, idle_sleep))

        except KeyboardInterrupt:
            logger.info(
                "Stop rubigram client | last_offset_id=%s | idle_sleep=%s",
                self.offset_id, idle_sleep
            )