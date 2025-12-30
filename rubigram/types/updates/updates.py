#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from ..config import Object
from rubigram import types


@dataclass
class Updates(Object):
    """
    **Represents a collection of multiple updates received from Rubigram.**
        `from rubigram.types import Updates`

    This object wraps a list of `Update` instances and includes the
    `next_offset_id` to fetch additional updates.

    Attributes:
        updates (`Optional[list[rubigram.types.Update]]`):
            A list of update objects.

        next_offset_id (`Optional[str]`):
            The ID offset to fetch the next batch of updates.
    """
    updates: Optional[list[types.Update]] = None
    next_offset_id: Optional[str] = None

    @classmethod
    def parse(cls, data: dict):
        """
        **Parse a dictionary into an `Updates` instance.**

        Converts raw dictionary data into a structured `Updates` object
        containing parsed `Update` instances.

        Args:
            data (`dict`):
                The raw dictionary data representing updates.

        Returns:
            Updates: A fully parsed `Updates` object containing `Update` instances.
        """
        data = data or {}
        updates = [
            types.Update.parse(update) if isinstance(update, dict) else update
            for update in data.get("updates", []) or []
        ]
        return cls(
            updates=updates,
            next_offset_id=data.get("next_offset_id")
        )