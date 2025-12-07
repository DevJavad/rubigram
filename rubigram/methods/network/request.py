#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Request:
    async def request(
        self: "rubigram.Client",
        endpoint: str,
        payload: dict,
        *,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
    ) -> dict:
        actual_proxy = proxy or self.proxy
        actual_retries = retries or self.retries
        actual_delay = delay or self.delay
        actual_backoff = backoff or self.backoff
        exception = None

        for attempt in range(1, actual_retries + 1):
            try:
                logger.debug(
                    "HTTP REQUEST RUBIKA(endpoint=%s, payload=%s, attempt=%s)", endpoint, payload, attempt
                )
                url = self.api + endpoint
                async with self.http.session.post(
                    url, json=payload, headers=headers, proxy=actual_proxy
                ) as response:
                    response.raise_for_status()

                    data: dict = await response.json()
                    if data.get("status") == "OK" and data.get("data"):
                        return data["data"]
                    else:
                        raise ValueError("No response from API")

            except Exception as error:
                exception = error
                logger.warning(
                    "HTTP ERROR(attempt=%s, error=%s)", attempt, error
                )

        if attempt < actual_retries:
            await asyncio.sleep(actual_delay)
            actual_delay *= actual_backoff

        raise exception