#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from aiohttp import ClientError, ClientTimeout
from typing import Optional
import asyncio
import rubigram
import logging


logger = logging.getLogger(__name__)


class Request:

    __slots__ = ()

    async def request(
        self: rubigram.Client,
        method: str,
        payload: Optional[dict] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> dict:
        proxy = proxy or self.proxy
        retries = retries or self.retries
        delay = delay or self.delay
        backoff = backoff or self.backoff
        max_delay = max_delay or self.max_delay

        last_error = None
        kwargs: dict = {"json": payload, "headers": headers, "proxy": proxy}
        if timeout or connect_timeout or read_timeout:
            kwargs["timeout"] = ClientTimeout(
                timeout, connect_timeout, read_timeout
            )

        for attempt in range(1, retries + 1):
            logger.debug(
                "Request attempt %s/%s for method '%s' | timeout=%s",
                attempt, retries, method, self.http.session.timeout.total
            )
            try:
                async with self.http.session.post(self.api + method, **kwargs) as response:
                    response.raise_for_status()
                    data: dict = await response.json()
                    if data.get("status") == "OK":
                        return data.get("data")

                    rubigram.errors.raise_rubigram_error(data)

            except (ClientError, asyncio.TimeoutError) as error:
                last_error = error
                await asyncio.sleep(min(delay, max_delay))
                delay += backoff

        raise last_error or RuntimeError("Max retries exceeded")