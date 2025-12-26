#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from aiohttp import ClientError
import asyncio
import rubigram
import logging


logger = logging.getLogger(__name__)


class Request:
    """
    HTTP request handler with retry logic for Rubika API.

    This class provides an asynchronous method to send POST requests
    to the Rubika Bot API with configurable retries, delays, backoff,
    and optional proxy support. It handles HTTP errors and validates
    the API response, raising appropriate exceptions if the request
    fails.
    """

    __slots__ = ()

    async def request(
        self: rubigram.Client,
        endpoint: str,
        payload: dict,
        *,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: float = 5.0
    ) -> dict:
        """
        Send an HTTP request to the specified endpoint with the
        provided JSON payload.

        Parameters:
            endpoint (str):
                API endpoint name (e.g., "sendMessage").
            payload (dict):
                JSON-serializable data to send in the request body.
            headers (Optional[dict], default=None):
                Custom HTTP headers.
            proxy (Optional[str], default=None):
                Proxy URL for the request. Uses client's proxy if None.
            retries (Optional[int], default=None):
                Number of retry attempts. Uses client's default if None.
            delay (Optional[float], default=None):
                Initial delay between retries in seconds.
            backoff (Optional[float], default=None):
                Multiplier to increase delay after each retry.
            max_delay (float, default=5.0):
                Maximum delay allowed between retries.

        Returns:
            dict: The "data" field from the API response if status is "OK".

        Raises:
            rubigram.errors.InvalidInput:
                If the API response status is "INVALID_INPUT".
            rubigram.errors.InvalidInput:
                If the API response status is not "INVALID_ACCESS".
            aiohttp.ClientError:
                For network or HTTP errors.
            RuntimeError:
                If maximum retries are exceeded.

        Example:
        .. code-block:: python
            # Assuming `client` is an instance of Rubigram.Client
            response = await client.request(
                endpoint="sendMessage",
                payload={"chat_id": "chat_id", "text": "text"},
                retries=5,
                delay=1.0,
                backoff=2.0
            )
        """
        proxy = self.proxy if proxy is None else proxy
        retries = self.retries if retries is None else retries
        delay = self.delay if delay is None else delay
        backoff = self.backoff if backoff is None else backoff
        max_delay = self.max_delay if max_delay is None else max_delay

        last_error = None

        for attempt in range(1, retries + 1):
            try:
                async with self.http.session.post(
                    self.api + endpoint,
                    json=payload,
                    headers=headers,
                    proxy=proxy
                ) as response:
                    response.raise_for_status()
                    data: dict = await response.json()

                    if data.get("status") == "OK":
                        logger.debug(data.get("data"))
                        return data.get("data")

                    if data.get("status") == "INVALID_INPUT":
                        raise rubigram.errors.InvalidInput(data)

                    elif data.get("status") == "INVALID_ACCESS":
                        raise rubigram.errors.InvalidAccess(data)
                    
                    else:
                        raise Exception(str(data))

            except ClientError as error:
                last_error = error
                if attempt == retries:
                    raise error

                await asyncio.sleep(min(delay, max_delay))
                delay *= backoff

        raise last_error or RuntimeError("Max retries exceeded")