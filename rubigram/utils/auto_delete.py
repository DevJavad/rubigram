#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram

from __future__ import annotations

import asyncio
import rubigram
import logging


logger = logging.getLogger(__name__)


async def auto_delete_task(client: rubigram.Client, message: rubigram.types.UMessage, delay: int):
    try:
        chat_id, message_id = message.chat_id, message.message_id
        await asyncio.sleep(delay)
        await client.delete_messages(chat_id, message_id)

    except Exception as error:
        logger.exception(
            "Error to auto delete for %s message in %s | error=%s", message_id, chat_id, error
        )


class AutoDelete:
    tasks: set[asyncio.Task] = set()

    @staticmethod
    def run(client: rubigram.Client, message: rubigram.types.UMessage, delay: int):
        if delay <= 0:
            return

        task = asyncio.create_task(auto_delete_task(client, message, delay))
        AutoDelete.tasks.add(task)

        task.add_done_callback(lambda t: AutoDelete.tasks.discard(t))

    @staticmethod
    def cancel_all():
        for task in list(AutoDelete.tasks):
            task.cancel()
        AutoDelete.tasks.clear()