#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Callable, Union
from .enums import ParseMode
from .methods import Methods
from .state import Storage, State
from .dispatcher import Dispatcher
from .http_session import HttpSession
import logging


logger = logging.getLogger(__name__)


class Client(Methods):
    """
    Initialize a new Rubika bot client.

    Parameters:
        token (str):
            Your bot's authentication token from @RubikaBot.

        offset_id (Optional[str], default: None):
            Starting point for update polling. Useful for resuming from
            a specific update after restart.

        storage (Optional[Storage], default: None):
            Custom storage implementation for user states.
            If None, uses default in-memory storage.

        timeout (Union[int, float], default: 10.0):
            Total timeout for API requests in seconds.

        connect_timeout (Union[int, float], default: 30.0):
            Timeout for establishing connections in seconds.

        read_timeout (Union[int, float], default: 50.0):
            Timeout for reading response data in seconds.

        retries (int, default: 3):
            Number of automatic retries for failed requests.

        backoff (Union[int, float], default: 0.5):
            Multiplier applied to delay after each retry.

        max_delay (Union[int, float], default: 3):
            Maximum delay between retries in seconds.

        delay (Union[int, float], default: 1):
            Initial delay between retries in seconds.

        max_connections (int, default: 100):
            Maximum number of concurrent HTTP connections.

        proxy (Optional[str], default: None):
            Proxy URL for requests (e.g., "http://proxy.example.com:8080").

        parse_mode (Union[str, ParseMode], default: ParseMode.MARKDOWN):
            Default text formatting mode. Can be "Markdown", "HTML", or enum.

    Example:
        # Full-featured client setup
        client = Client(
            token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            offset_id="update_123456",
            timeout=30.0,
            connect_timeout=10.0,
            read_timeout=20.0,
            retries=5,
            delay=2.0,
            backoff=1.5,
            max_delay=10.0,
            max_connections=50,
            proxy="http://corporate-proxy:3128",
            parse_mode="HTML"
        )
    """

    def __init__(
        self,
        token: str,
        offset_id: Optional[str] = None,
        storage: Optional[Storage] = None,
        timeout: Union[int, float] = 10.0,
        connect_timeout: Union[int, float] = 30.0,
        read_timeout: Union[int, float] = 50.0,
        retries: int = 3,
        backoff: Union[int, float] = 0.5,
        max_delay: Union[int, float] = 3,
        delay: Union[int, float] = 1,
        max_connections: int = 100,
        proxy: Optional[str] = None,
        parse_mode: Union[str, ParseMode] = ParseMode.MARKDOWN,
        auto_delete: Optional[int] = None
    ):
        self.token = token
        self.offset_id = offset_id
        self.storage = storage or Storage()
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.retries = retries
        self.backoff = backoff
        self.max_delay = max_delay
        self.delay = delay
        self.max_connections = max_connections
        self.proxy = proxy
        self.parse_mode = parse_mode
        self.auto_delete = auto_delete

        self.dispatcher = Dispatcher(self)
        self.http = HttpSession(
            timeout,
            connect_timeout,
            read_timeout,
            max_connections
        )

        self.stop_handlers: list[Callable] = []
        self.start_handlers: list[Callable] = []
        self.api: str = f"https://botapi.rubika.ir/v3/{token}/"

        super().__init__()

    def state(self, user_id: str):
        """
        Get state manager for a specific user.

        Parameters:
            user_id (str):
                The user ID to manage state for.

        Returns:
            State:
                State object for managing user-specific data.

        Example:
            # Get user state
            user_state = client.state("user_123456")

            # Set state data
            user_state.set("language", "fa")
            user_state.set("step", "waiting_for_name")

            # Get state data
            language = user_state.get("language")

            # Clear state
            user_state.clear()
        """
        return State(self.storage, user_id)

    async def start(self):
        """
        Start the client and initialize connections.

        This method:
        1. Establishes HTTP connection pool
        2. Executes registered start handlers
        3. Prepares the client for receiving updates

        Note:
            - Automatically called by context manager and run() method
            - Start handlers can be used for initialization tasks
            - HTTP session is created with configured timeouts and limits
        """
        await self.http.connect()
        for app in self.start_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("Error to run start handler: %s", error)

    async def stop(self):
        """
        Stop the client and clean up resources.

        This method:
        1. Closes HTTP connections
        2. Executes registered stop handlers
        3. Performs cleanup tasks

        Note:
            - Automatically called by context manager and on shutdown
            - Stop handlers can be used for cleanup tasks
            - Ensures proper resource release
        """
        await self.http.disconnect()
        for app in self.stop_handlers:
            try:
                await app(self)
            except Exception as error:
                logger.warning("Error to run stop handler: %s", error)

    async def __aenter__(self):
        """
        Async context manager entry.

        Automatically calls start() when entering context.

        Returns:
            Client: The started client instance.

        Example:
            async with Client("TOKEN") as bot:
                # Client is automatically started
                await bot.send_message("chat_id", "Hello")
            # Client is automatically stopped
        """
        await self.start()
        return self

    async def __aexit__(self, *args):
        """
        Async context manager exit.

        Automatically calls stop() when exiting context.
        """
        await self.stop()