#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object
import rubigram


@dataclass
class ButtonLocation(Object):
    """
    **Represents a location picker button.**
        `from rubigram.types import ButtonLocation`

    Attributes:
        default_pointer_location (`Optional[rubigram.types.Location]`):
            Default pointer location.

        default_map_location (`Optional[rubigram.types.Location]`):
            Default map location.

        type (`Optional[Union[str, rubigram.enums.ButtonLocationType]]`):
            Type of location picker.

        title (`Optional[str]`):
            Title of the location picker.

        location_image_url (`Optional[str]`):
            Optional image URL for the location.
    """
    default_pointer_location: Optional[rubigram.types.Location] = None
    default_map_location: Optional[rubigram.types.Location] = None
    type: Optional[Union[str, rubigram.enums.ButtonLocationType]] = None
    title: Optional[str] = None
    location_image_url: Optional[str] = None