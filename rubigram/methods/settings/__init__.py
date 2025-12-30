#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .set_command import SetCommands
from .update_bot_endpoint import UpdateBotEndpoints


class Settings(
    SetCommands,
    UpdateBotEndpoints
):
    pass