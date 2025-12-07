#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .storage import Storage
import logging


logger = logging.getLogger(__name__)


class State:
    def __init__(
        self,
        storage: "Storage",
        user_id: str
    ):
        self.storage = storage
        self.user_id = user_id

    async def set(self, state: str, **kwargs):
        await self.storage.set_state(self.user_id, state, **kwargs)

    async def get(self):
        return await self.storage.get_state(self.user_id)

    async def delete(self):
        await self.storage.delete_state(self.user_id)