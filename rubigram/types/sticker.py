#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from .config import Object
import rubigram



@dataclass
class Sticker(Object):
    """
    **Represents a sticker in Rubigram.**
        `from rubigram.types import Sticker`

    Attributes:
        sticker_id (`Optional[str]`):
            Unique identifier for the sticker.

        file (`Optional[rubigram.types.File]`):
            File object representing the sticker image.

        emoji_character (`Optional[str]`):
            Associated emoji character for the sticker.
    """
    sticker_id: Optional[str] = None
    file: Optional[rubigram.types.File] = None
    emoji_character: Optional[str] = None