from __future__ import annotations

from rubigram.filters import Filter
from typing import Callable, Optional


class Handler:
    def __init__(
        self,
        callback: Callable,
        filters: Optional[Filter] = None
    ):
        self.callback = callback
        self.filters = filters

    async def check(self, client, update) -> bool:
        if self.filters is None:
            return True
        return await self.filters(client, update)

    async def run(self, client, update):
        await self.callback(client, update)