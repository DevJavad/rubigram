#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .auto_delete import AutoDelete
from .parser import Parser


class Utils(
    AutoDelete,
    Parser
):
    pass