import os
import logging
import asyncio

from pathlib import Path
from random import randint
from aiohttp import ClientSession
from typing import Optional, Union
from importlib import import_module
from asyncio import AbstractEventLoop
from concurrent.futures.thread import ThreadPoolExecutor as Executor

from rubigram.ask import AskMixin
from rubigram.utils import ainput
from rubigram import utils, enums, types, errors, handlers


from .connection import Connection
from .dispatcher import Dispatcher
from .handlers import Handler
from .methods import Methods
from .server import Server
from .crypto import Crypto
from .parser import Parser
from .storage import Storage
from .filters import Filter


logger = logging.getLogger(__name__)


class Client(Methods):

    WORKERS: int = min(32, (os.cpu_count() or 0) + 4)
    DEVICE_MODEL: str = "Rubigram"

    WSS_URL: str = "wss://nsocket11.iranlms.ir:80"
    @property
    def API_URL(self):
        return "https://messengerg2c%s.iranlms.ir/" % randint(1, 69)

    WEB_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/102.0.0.0 Safari/537.36"
    )

    WEB_HEADERS: dict[str, str] = {
        "origin": "https://m.rubika.ir",
        "referer": "https://m.rubika.ir/",
        "content-type": "application/json",
        "connection": "keep-alive",
        "user-agent": WEB_USER_AGENT
    }

    # ANDROID_HEADERS: dict[str, str] = {
    #     "Content-Type": "application/json; charset=utf-8",
    #     "Accept-Encoding": "gzip",
    #     "User-Agent": "okhttp/3.12.12"

    # }

    ANDROID_HEADERS: dict[str, str] = {
        "content-type": "application/json",
        "connection": "keep-alive",
        "user-agent": "okhttp/3.12.1"
    }

    PWA_CLIENT: dict[str, str] = {
        "app_name": "Main",
        "app_version": "2.4.6",
        "platform": "PWA",
        "package": "m.rubika.ir",
    }

    WEB_CLIENT: dict[str, str] = {
        "app_name": "Main",
        "app_version": "4.4.29",
        "platform": "Web",
        "package": "web.rubika.ir",
        "lang_code": "fa"
    }

    ANDROID_CLIENT: dict[str, str] = {
        "app_name": "Main",
        "app_version": "3.8.2",
        "lang_code": "fa",
        "package": "app.rbmain.a",
        "temp_code": "25",
        "platform": "Android"
    }

    def __init__(
        self,
        name: Optional[str] = None,
        auth: Optional[str] = None,
        private_key: Optional[str] = None,

        phone_number: Optional[str] = None,
        password: Optional[str] = None,
        hide_password: bool = False,
        device_model: str = DEVICE_MODEL,
        user_agent: Optional[str] = None,
        lang_code: str = "fa",
        auto_delete: Optional[int] = None,

        run_type: "enums.RunType" = enums.RunType.WebSocket,

        format_private_key: bool = True,

        platform: enums.Platform = enums.Platform.WEB,
        parse_mode: enums.ParseMode = enums.ParseMode.MARKDOWN,

        max_connections: int = 100,

        timeout: float = 20,
        connect_timeout: float = 20,
        socket_read_timeout: float = 20,

        retry: int = 3,
        delay: Union[int, float] = 1,
        backoff: Union[int, float] = 0.5,

        proxy: Optional[str] = None,
        headers: Optional[dict] = None,

        plugins: Optional[dict] = None,

        workers: int = WORKERS,
        loop: Optional[AbstractEventLoop] = None,

        http_session: Optional[ClientSession] = None,
        connection: Optional[Connection] = None
    ):
        self.name = name
        self.auth = auth
        self.private_key = private_key

        self.phone_number = phone_number
        self.password = password
        self.hide_password = hide_password
        self.device_model = device_model
        self.user_agent = user_agent
        self.lang_code = lang_code
        self.auto_delete = auto_delete

        self.run_type = run_type

        self.format_private_key = format_private_key

        self.platform = platform
        self.parse_mode = parse_mode

        self.max_connections = max_connections

        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.socket_read_timeout = socket_read_timeout

        self.retry = retry
        self.delay = delay
        self.backoff = backoff

        self.proxy = proxy
        self.headers = headers

        self.plugins = plugins
        self.workers = workers
        self.semaphore = asyncio.Semaphore(self.workers)

        if platform == enums.Platform.WEB:
            self.client_info = self.WEB_CLIENT
            if self.headers is None:
                self.headers = self.WEB_HEADERS

        elif platform == enums.Platform.ANDROID:
            self.client_info = self.ANDROID_CLIENT
            if self.headers is None:
                self.headers = self.ANDROID_HEADERS

        elif platform == enums.Platform.PWA:
            self.client_info = self.PWA_CLIENT
            if self.headers is None:
                self.headers = self.WEB_HEADERS

        if isinstance(loop, AbstractEventLoop):
            self.loop = loop
        else:
            self.loop = utils.get_event_loop()

        if auth and private_key:
            self.crypto = Crypto(auth, private_key)
        else:
            self.crypto = None

        self.sequential_handlers = False

        self.parser = Parser(parse_mode)

        if isinstance(http_session, ClientSession):
            self.http_session = http_session
        else:
            self.connection = Connection(
                timeout, connect_timeout, max_connections, socket_read_timeout
            )
            self.http_session = self.connection.http_session
            
        self.server = Server(
            self.connection, retry, delay, backoff, proxy, headers
        )

        self.executor = Executor(workers, thread_name_prefix="Handler")

        self.storage = Storage()
        self.me: Optional["types.User"] = None
        self.guid: Optional[str] = None

        self.dispatcher = Dispatcher(self)

        self.stop_handler: "handlers.StopHandler" = None
        self.start_handler: "handlers.StartHandler" = None
        self.connect_handler: "handlers.ConnectHandler" = None
        self.disconnect_handler: "handlers.DisconnectHandler" = None
        self.dispatcher = Dispatcher(self)
        self._pending_asks: dict[str, asyncio.Future] = {}
        self._pending_filters: dict[str, Optional[Filter]] = {}
        self._default_timeout = 60
        self._ask_manager = None

    def __enter__(self) -> "Client":
        self.start()
        return self

    def __exit__(self, *args):
        try:
            self.stop()
        except ConnectionError:
            pass

    async def __aenter__(self) -> "Client":
        await self.start()
        return self

    async def __aexit__(self, *args):
        try:
            await self.stop()
        except ConnectionError:
            pass

    @property
    def ask(self):
        if self._ask_manager is None:
            from rubigram.ask import AskManager
            self._ask_manager = AskManager(self)
        return self._ask_manager

    async def login(self) -> "types.User":
        print(f"Welcome to Rubigram (version ...)")  # Set version

        while True:
            try:
                if not self.phone_number:
                    while True:
                        phone = ainput("Enter phone number: ", loop=self.loop)

                        if not phone:
                            continue

                        confirm = await ainput(f'Is {phone} correct? (Y/N): ', loop=self.loop)

                        if confirm.lower() == "y":
                            break

                    self.phone_number = phone

                while True:
                    try:
                        sent_code = await self.send_code(phone, self.password)
                        if sent_code.status == enums.SentCodeStatus.OK:
                            break

                    except errors.SendPassword:
                        while True:
                            self.password = ainput(
                                f"Enter 2FA password ({sent_code.hint_pass_key}): ", hide=self.hide_password, loop=self.loop
                            )

                            if self.password:
                                break

                    except errors.InvalidPassword:
                        while True:
                            password = ainput(
                                f"Pssword is wrong, Enter the correct password: ", hide=self.hide_password, loop=self.loop
                            )

                            if password:
                                self.password = password
                                break

                while True:
                    code = ainput(
                        f"Enter login code: ", loop=self.loop
                    )

                    if code and code.isdigit():
                        break

                try:
                    sign_in = await self.sign_in(self.phone_number, code, sent_code.phone_code_hash)
                    if sign_in.status == enums.SignInStatus.OK:
                        break

                except errors.CodeIsInvalid:
                    ...

                except errors.CodeIsExpired:
                    ...

                except errors.CodeIsInvalid:
                    ...
            except:
                pass

    def load_plugins(self):
        if self.plugins:
            plugins = self.plugins.copy()

            for option in ["include", "exclude"]:
                if plugins.get(option, []):
                    plugins[option] = [
                        (i.split()[0], i.split()[1:] or None)
                        for i in self.plugins[option]
                    ]
        else:
            return

        if plugins.get("enabled", True):
            root = plugins["root"]
            include = plugins.get("include", [])
            exclude = plugins.get("exclude", [])

            count = 0

            if not include:
                for path in sorted(Path(root.replace(".", "/")).rglob("*.py")):
                    module_path = '.'.join(path.parent.parts + (path.stem,))
                    module = import_module(module_path)

                    for name in vars(module).keys():
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    logger.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            pass
            else:
                for path, handlers in include:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        logger.warning(
                            '[%s] [LOAD] Ignoring non-existent module "%s"', self.name, module_path)
                        continue

                    if "__path__" in dir(module):
                        logger.warning(
                            '[%s] [LOAD] Ignoring namespace "%s"', self.name, module_path)
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    logger.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            if warn_non_existent_functions:
                                logger.warning('[{}] [LOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.name, name, module_path))

            if exclude:
                for path, handlers in exclude:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        logger.warning(
                            '[%s] [UNLOAD] Ignoring non-existent module "%s"', self.name, module_path)
                        continue

                    if "__path__" in dir(module):
                        logger.warning(
                            '[%s] [UNLOAD] Ignoring namespace "%s"', self.name, module_path)
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.remove_handler(handler, group)

                                    logger.info('[{}] [UNLOAD] {}("{}") from group {} in "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count -= 1
                        except Exception:
                            if warn_non_existent_functions:
                                logger.warning('[{}] [UNLOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.name, name, module_path))

            if count > 0:
                logger.info('[{}] Successfully loaded {} plugin{} from "{}"'.format(
                    self.name, count, "s" if count > 1 else "", root))
            else:
                logger.warning('[%s] No plugin loaded from "%s"',
                               self.name, root)
