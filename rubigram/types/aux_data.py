#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from dataclasses import dataclass
from .config import Object


@dataclass
class AuxData(Object):
    """
    **Represents auxiliary data attached to a message.**
        `from rubigram.types import AuxData`

    AuxData is typically used to store metadata related to
    buttons, interactions, or other inline components in a chat.

    Attributes:
        start_id (`Optional[str]`):
            An identifier for the start action, if applicable.

        button_id (`Optional[str]`):
            The ID of a button that triggered this auxiliary data, if applicable.
    """
    start_id: Optional[str] = None
    button_id: Optional[str] = None