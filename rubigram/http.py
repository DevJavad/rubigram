#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiohttp import ClientSession, TCPConnector, ClientTimeout
from typing import Union
import logging


logger = logging.getLogger(__name__)


class Http:
    def __init__(
        self,
        timeout: float = 30.0,
        connect_timeout: float = 10.0,
        read_timeout: float = 20.0,
        max_connections: int = 100
    ):
        self.timeout = ClientTimeout(timeout, connect_timeout, read_timeout)
        self.max_connections = max_connections
        self.session: Union[ClientSession, None] = None

    async def connect(self):
        if self.session is None or self.session.closed:
            connector = TCPConnector(limit=self.max_connections)
            self.session = ClientSession(
                connector=connector, timeout=self.timeout
            )

            logger.info(
                "HTTP SESSION CREATE(timeout=%s, connections=%s)",
                self.timeout.total, self.max_connections
            )

    async def disconnect(self):
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("HTTP SESSION CLOSED")
        self.session = None