#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from datetime import datetime
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Run:
    async def receiver(self: "rubigram.Client"):
        await self.start()
        try:
            while True:
                updates = await self.get_updates(100, self.offset_id)
                if updates.updates:
                    for update in updates.updates:
                        time = None
                        if update.type == "NewMessage":
                            time = int(update.new_message.time)
                        elif update.type == "UpdatedMessage":
                            time = int(update.updated_message.time)
                        now = int(datetime.now().timestamp())
                        if time and (time >= now or time + 2 >= now):
                            update.client = self
                            await self.dispatcher(update)

                        self.offset_id = updates.next_offset_id

        except Exception as error:
            logger.error("RECEIVER(error=%s)", error)

        finally:
            await self.stop()

    def run(self: "rubigram.Client"):
        try:
            asyncio.run(self.receiver())
        except KeyboardInterrupt:
            pass