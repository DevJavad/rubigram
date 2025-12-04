#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable, Union
from .enums import ParseMode
from .methods import Methods
from .http import Http
import logging


logger = logging.getLogger(__name__)


class Client(Methods):
    def __init__(
        self,
        token: str,
        webhook: Optional[str] = None,
        parse_mode: Union[str, "ParseMode"] = "markdown",
        proxy: Optional[str] = None,
        retries: int = 3,
        delay: float = 1.0,
        backoff: int = 2,
        timeout: float = 30.0,
        connect_timeout: float = 10.0,
        read_timeout: float = 20.0,
        max_connections: int = 100
    ):
        self.token = token
        self.webhook = webhook
        self.parse_mode = parse_mode
        self.proxy = proxy
        self.retries = retries
        self.delay = delay
        self.backoff = backoff
        self.http = Http(
            timeout, connect_timeout, read_timeout, max_connections
        )

        self.offset_id: Union[str, None] = None
        self.set_new_endpoint: bool = True
        self.api: str = f"https://botapi.rubika.ir/v3/{token}/"

        self.new_message_handlers: list[Callable] = []
        self.inline_message_handlers: list[Callable] = []
        self.update_message_handlers: list[Callable] = []
        self.remove_message_handlers: list[Callable] = []
        self.started_bot_handlers: list[Callable] = []
        self.stopped_bot_handlers: list[Callable] = []
        self.start_handlers: list[Callable] = []
        self.stop_handlers: list[Callable] = []
        self.router_handlers: list[Callable] = []

        super().__init__()

    async def start(self):
        await self.http.connect()
        for app in self.start_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("APP START ERROR(error=%s)", error)

    async def stop(self):
        await self.http.disconnect()
        for app in self.stop_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("APP STOP ERROR(error=%s)", error)

    async def startup(self, app):
        await self.start()
        if self.set_new_endpoint:
            await self.setup_endpoints()

    async def cleanup(self, app):
        await self.stop()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.stop()