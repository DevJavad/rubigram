#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from ..config import Object
import rubigram


@dataclass
class ButtonSelection(Object):
    """
    **Represents a selection of multiple items that can be shown in a button.**
        `from rubigram.types import ButtonSelection`

    Attributes:
        selection_id (`Optional[str]`):
            Unique identifier for this selection.

        search_type (`Optional[str]`):
            Type of search to filter items.

        get_type (`Optional[str]`):
            Type of retrieval for items.

        items (`Optional[list[rubigram.types.ButtonSelectionItem]]`):
            List of items in the selection.

        is_multi_selection (`Optional[bool]`):
            Whether multiple items can be selected.

        columns_count (`Optional[str]`):
            Number of columns to display items in.

        title (`Optional[str]`):
            Title displayed above the selection.
    """
    selection_id: Optional[str] = None
    search_type: Optional[str] = None
    get_type: Optional[str] = None
    items: Optional[list[rubigram.types.ButtonSelectionItem]] = None
    is_multi_selection: Optional[bool] = None
    columns_count: Optional[str] = None
    title: Optional[str] = None