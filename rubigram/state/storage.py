#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiocache import Cache
from aiocache.serializers import JsonSerializer
import logging


logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, ttl: int = 3600):
        self.cache = Cache(
            Cache.MEMORY,
            serializer=JsonSerializer(),
            ttl=ttl
        )

    async def set_state(self, user_id: str, state: str, **kwargs):
        payload = {"state": state, "data": kwargs}
        return await self.cache.set("state:{}".format(user_id), payload)

    async def get_state(self, user_id: str):
        await self.cache.get("state:{}".format(user_id))

    async def delete_state(self, user_id: str):
        await self.cache.delete("state:{}".format(user_id))