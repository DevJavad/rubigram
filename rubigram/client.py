#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram

from __future__ import annotations

from typing import Optional, Callable, Union
from .enums import ParseMode
from .methods import Methods
from .state import Storage, State
from .http_session import HttpSession
import logging


logger = logging.getLogger(__name__)


class Client(Methods):
    """
    Main client class for interacting with the Rubika Bot API.

    This class extends Methods to provide API functionality and manages
    the bot's lifecycle, webhook configuration, message handlers, and
    connection settings.

    Parameters:
        token (str):
            Bot token obtained from @RubikaBot.

        webhook (Optional[str], optional):
            Webhook URL for receiving updates. If None, long polling is used.
            Defaults to None.

        parse_mode (Union[str, "ParseMode"], optional):
            Default parse mode for text messages. Can be "markdown", "html",
            or a ParseMode enum value. Defaults to "markdown".

        storage (Optional["Storage"], optional):
            Storage instance for persisting user states and data.
            If None, a new Storage instance is created. Defaults to None.

        proxy (Optional[str], optional):
            Proxy URL for HTTP requests (e.g., "http://proxy.com:8080").
            Defaults to None.

        retries (int, optional):
            Number of retries for failed HTTP requests. Defaults to 3.

        delay (float, optional):
            Initial delay between retries in seconds. Defaults to 1.0.

        backoff (int, optional):
            Exponential backoff multiplier for retries. Defaults to 2.

        timeout (float, optional):
            Total timeout for HTTP requests in seconds. Defaults to 100.0.

        connect_timeout (float, optional):
            Connection establishment timeout in seconds. Defaults to 30.0.

        read_timeout (float, optional):
            Socket read timeout in seconds. Defaults to 50.0.

        max_connections (int, optional):
            Maximum number of simultaneous HTTP connections. Defaults to 100.

    Attributes:
        token (str): Bot authentication token.
        webhook (Optional[str]): Configured webhook URL.
        parse_mode (Union[str, ParseMode]): Default parse mode.
        storage (Storage): User state storage instance.
        proxy (Optional[str]): Proxy URL for requests.
        retries (int): Number of retry attempts.
        delay (float): Initial retry delay.
        backoff (int): Retry backoff multiplier.
        http (HttpSession): HTTP session manager.
        offset_id (Union[str, None]): Last processed update ID for polling.
        set_new_endpoint (bool): Flag to configure endpoints on startup.
        api (str): Base API endpoint URL.
        new_message_handlers (list[Callable]): Handlers for new messages.
        inline_message_handlers (list[Callable]): Handlers for inline queries.
        update_message_handlers (list[Callable]): Handlers for message updates.
        remove_message_handlers (list[Callable]): Handlers for message deletions.
        started_bot_handlers (list[Callable]): Handlers for bot start events.
        stopped_bot_handlers (list[Callable]): Handlers for bot stop events.
        start_handlers (list[Callable]): Handlers for client start.
        stop_handlers (list[Callable]): Handlers for client stop.
        router_handlers (list[Callable]): Handlers for routing updates.

    Example:
    .. code-block:: python
        # Basic client
        client = Client(token="YOUR_BOT_TOKEN")

        # Client with webhook
        client = Client(
            token="YOUR_BOT_TOKEN",
            webhook="https://example.com/webhook",
            parse_mode="html",
            retries=5
        )

        # Client with storage and proxy
        storage = Storage()
        client = Client(
            token="YOUR_BOT_TOKEN",
            storage=storage,
            proxy="http://proxy:8080"
        )
    """

    def __init__(
        self,
        token: str,
        webhook: Optional[str] = None,
        parse_mode: Union[str, ParseMode] = ParseMode.MARKDOWN,
        storage: Optional[Storage] = None,
        proxy: Optional[str] = None,
        retries: int = 3,
        delay: float = 1.0,
        backoff: int = 2,
        max_delay: float = 5.0,
        timeout: float = 100.0,
        connect_timeout: float = 30.0,
        read_timeout: float = 50.0,
        max_connections: int = 100,
        offset_id: Optional[str] = None
    ):
        self.token = token
        self.webhook = webhook
        self.parse_mode = parse_mode
        self.storage = storage or Storage()
        self.proxy = proxy
        self.retries = retries
        self.delay = delay
        self.backoff = backoff
        self.max_delay = max_delay
        self.offset_id = offset_id
        self.http = HttpSession(
            timeout, connect_timeout, read_timeout, max_connections
        )

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

    def state(self, user_id: str):
        """
        Get a State object for managing user conversation state.

        Parameters:
            user_id (str):
                Unique identifier for the user (chat_id).

        Returns:
            State: A State instance bound to the specified user.

        Example:
        .. code-block:: python
            user_state = client.state("b0123456789")
            await user_state.update({"step": "waiting_for_name"})
            data = await user_state.get()
        """
        return State(self.storage, user_id)

    async def start(self):
        """
        Start the client and establish HTTP connections.

        This method:
        1. Connects the HTTP session
        2. Executes all registered start handlers
        3. Logs any handler errors

        Note:
            Called automatically when using context manager or startup().

        Example:
        .. code-block:: python
            await client.start()
        """
        await self.http.connect()
        for app in self.start_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("Start app, error=%s", error)

    async def stop(self):
        """
        Stop the client and close HTTP connections.

        This method:
        1. Executes all registered stop handlers
        2. Disconnects the HTTP session
        3. Logs any handler errors

        Note:
            Called automatically when using context manager or cleanup().

        Example:
        .. code-block:: python
            await client.stop()
        """
        await self.http.disconnect()
        for app in self.stop_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("Stop app, error=%s", error)

    async def startup(self, app):
        """
        Start the client and configure endpoints if needed.

        Parameters:
            app:
                Application context (typically from a web framework).

        Note:
            This method is designed to be used with web frameworks
            like FastAPI or Quart that have startup events.

        Example:
        .. code-block:: python
            # In FastAPI
            @app.on_event("startup")
            async def startup_event():
                await client.startup(app)
        """
        await self.start()
        if self.set_new_endpoint:
            await self.setup_endpoints()

    async def cleanup(self, app):
        """
        Stop the client during application cleanup.

        Parameters:
            app:
                Application context (typically from a web framework).

        Note:
            This method is designed to be used with web frameworks
            like FastAPI or Quart that have shutdown events.

        Example:
        .. code-block:: python
            # In FastAPI
            @app.on_event("shutdown")
            async def shutdown_event():
                await client.cleanup(app)
        """
        await self.stop()

    async def __aenter__(self):
        """
        Enter the async context manager.

        Returns:
            Client: The started client instance.

        Example:
        .. code-block:: python
            async with Client(token="YOUR_TOKEN") as client:
                # Client is started here
                await client.send_message(...)
            # Client is automatically stopped here
        """
        await self.start()
        return self

    async def __aexit__(self, *args):
        """
        Exit the async context manager.

        Parameters:
            *args: Exception information if an exception occurred.

        Note:
            Always stops the client, even if an exception occurred.
        """
        await self.stop()