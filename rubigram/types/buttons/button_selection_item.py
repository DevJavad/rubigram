#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from dataclasses import dataclass
from ..config import Object

if TYPE_CHECKING:
    from rubigram.enums import ButtonSelectionType


@dataclass
class ButtonSelectionItem(Object):
    """
    **Represents an individual selectable item in a ButtonSelection.**
        `from rubigram.types import ButtonSelectionItem`

    Attributes:
        text (`Optional[str]`):
            The display text of the item.

        image_url (`Optional[str]`):
            Optional URL for an image representing the item.

        type (`Optional[Union[str, rubigram.enums.ButtonSelectionType]]`):
            Type of selection item.
    """
    text: Optional[str] = None
    image_url: Optional[str] = None
    type: Optional[Union[str, ButtonSelectionType]] = None