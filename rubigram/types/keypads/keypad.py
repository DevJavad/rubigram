#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from dataclasses import dataclass, field
from ..config import Object
import rubigram


@dataclass
class Keypad(Object):
    """
    **Represents a chat keypad, which may contain multiple rows of buttons.**
        `from rubigram.types import Keypad`

    Attributes:
        rows (`list[rubigram.types.KeypadRow]`):
            A list of KeypadRow objects representing the keypad layout.

        resize_keyboard (`bool`):
            Whether the keyboard should be resized to fit the screen. Defaults to True.

        on_time_keyboard (`bool`):
            Whether the keyboard should appear temporarily and disappear after use. Defaults to False.
    """
    rows: list[rubigram.types.KeypadRow] = field(default_factory=list)
    resize_keyboard: bool = True
    on_time_keyboard: bool = False