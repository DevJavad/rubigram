#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from dataclasses import dataclass, field
from ..config import Object
import rubigram


@dataclass
class KeypadRow(Object):
    """
    **Represents a single row of buttons in a chat keypad.**
        `from rubigram.types import KeypadRow`

    Attributes:
        buttons (`list[rubigram.types.Button]`):
            A list of Button objects in this row.
    """
    buttons: list[rubigram.types.Button] = field(default_factory=list)