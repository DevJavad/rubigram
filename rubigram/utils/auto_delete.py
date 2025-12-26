#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import asyncio
import rubigram
import logging


logger = logging.getLogger(__name__)


class AutoDelete:
    @staticmethod
    def run(
        client: "rubigram.Client",
        message: "rubigram.types.UMessage",
        delay: int
    ):
        """
        **Schedule automatic deletion of a message after delay.**
            `AutoDelete.run(client, message, 10)`

        This static method schedules a message to be automatically deleted
        after the specified delay in seconds. The deletion runs asynchronously
        in the background.

        Args:
            client (`rubigram.Client`):
                The client instance used to delete the message.

            message (`rubigram.types.UMessage`):
                The message object to be deleted.

            delay (`int`):
                Number of seconds to wait before deleting the message.

        Example:
        .. code-block:: python

            # Send a message and schedule its deletion after 30 seconds
            message = await client.send_message(chat_id, "This will be deleted soon")
            AutoDelete.run(client, message, 30)

        Note:
            - If delay is 0 or negative, no deletion is scheduled
            - Deletion runs as a background task and won't block execution
            - Errors during deletion are logged as warnings but not raised
        """
        if delay <= 0:
            return

        asyncio.create_task(
            AutoDelete.auto_delete_task(client, message, delay)
        )

    @staticmethod
    async def auto_delete_task(
        client: "rubigram.Client",
        message: "rubigram.types.UMessage",
        delay: int
    ):
        """
        **Background task to automatically delete a message.**
            `await AutoDelete.auto_delete_task(client, message, 10)`

        This internal method waits for the specified delay and then
        attempts to delete the message. Any exceptions during deletion
        are caught and logged as warnings.

        Args:
            client (`rubigram.Client`):
                The client instance used to delete the message.

            message (`rubigram.types.UMessage`):
                The message object to be deleted.

            delay (`int`):
                Number of seconds to wait before deleting the message.

        Note:
            This method is designed to run as a background task and
            should not be called directly. Use `AutoDelete.run()` instead.
        """
        try:
            await asyncio.sleep(delay)
            await client.delete_messages(message.chat_id, message.message_id)

        except Exception as error:
            logger.warning(
                "Auto delete message, chat_id=%s, message_id=%s, error=%s", message.chat_id, message.message_id, error
            )