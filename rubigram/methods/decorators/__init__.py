#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .on_stop import OnStop
from .on_start import OnStart
from .on_message import OnMessage
from .on_stopped_bot import OnStoppedBot
from .on_started_bot import OnStartedBot
from .on_inline_message import OnInlineMessage
from .on_update_message import OnEditedMessage
from .on_deleted_message import OnDeletedMessage


class Decorators(
    OnStop,
    OnStart,
    OnMessage,
    OnStoppedBot,
    OnStartedBot,
    OnInlineMessage,
    OnEditedMessage,
    OnDeletedMessage
):
    pass