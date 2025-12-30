#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiohttp import ClientSession, TCPConnector, ClientTimeout
from typing import Optional, Union
import logging


logger = logging.getLogger(__name__)


class HttpSession:
    """
    Asynchronous HTTP session manager based on aiohttp.

    This class manages the lifecycle of a shared aiohttp ClientSession,
    providing configurable timeouts and connection pooling. It is intended
    to be used as the low-level HTTP transport layer for Rubigram.

    Parameters:
        timeout (float):
            Total timeout (in seconds) for a single HTTP request, including
            connection, redirects, and response reading.

        connect_timeout (float):
            Maximum time (in seconds) allowed to establish a connection
            to the remote server.

        read_timeout (float):
            Maximum time (in seconds) to wait for data to be read from
            the socket after the connection is established.

        max_connections (int):
            Maximum number of simultaneous connections allowed in the
            connection pool.

    Example:
    .. code-block:: python
        async with HttpSession(timeout=30, max_connections=100) as http:
            session = http.get_session()
            await session.get("https://example.com")
    """

    def __init__(
        self,
        timeout: Union[int, float],
        connect_timeout: Union[int, float],
        read_timeout: Union[int, float],
        max_connections: int
    ):
        self.timeout = ClientTimeout(
            total=timeout,
            connect=connect_timeout,
            sock_read=read_timeout
        )
        self.max_connections = max_connections
        self.session: Optional[ClientSession] = None

    async def connect(self) -> None:
        if not self.is_connected:
            connector = TCPConnector(
                limit=self.max_connections, enable_cleanup_closed=True
            )
            self.session = ClientSession(
                connector=connector, timeout=self.timeout
            )
            logger.info(
                "Connect to HTTP session, timeout=%s, connections=%s",
                int(self.timeout.total), self.max_connections
            )
        else:
            logger.debug("HTTP session already connected")

    async def disconnect(self) -> None:
        if self.is_connected:
            await self.session.close()
            logger.info("HTTP session closed")
        self.session = None

    @property
    def is_connected(self) -> bool:
        return self.session is not None and not self.session.closed

    def get_session(self) -> "ClientSession":
        if not self.is_connected:
            raise RuntimeError("HTTP session is not connected")
        return self.session

    async def __aenter__(self) -> "HttpSession":
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.disconnect()