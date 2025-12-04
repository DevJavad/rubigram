#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .get_update import GetUpdates
from .get_me import GetMe


class Updates(
    GetUpdates,
    GetMe
):
    pass