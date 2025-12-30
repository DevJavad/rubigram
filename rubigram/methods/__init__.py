#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .decorators import Decorators
from .utilities import Utilities
from .messages import Messages
from .settings import Settings
from .updates import Updates
from .network import Network
from .chats import Chats
from .files import Files
from .users import Users


class Methods(
    Decorators,
    Utilities,
    Messages,
    Network,
    Settings,
    Updates,
    Chats,
    Files,
    Users
):
    pass