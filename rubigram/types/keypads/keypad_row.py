#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from ..config import Object

if TYPE_CHECKING:
    from rubigram.types import Button


@dataclass
class KeypadRow(Object):
    """
    **Represents a single row of buttons in a chat keypad.**
        `from rubigram.types import KeypadRow`

    Attributes:
        buttons (`list[rubigram.types.Button]`):
            A list of Button objects in this row.
    """
    buttons: list[Button] = field(default_factory=list)