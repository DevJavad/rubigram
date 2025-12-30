#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from .config import Object
import rubigram


@dataclass
class LiveLocation(Object):
    """
    **Represents a live location shared by a user.**
        `from rubigram.types import LiveLocation`

    Attributes:
        start_time (`Optional[str]`):
            The start time of the live location sharing.

        live_period (`Optional[int]`):
            Duration of the live location in seconds.

        current_location (`Optional[rubigram.types.Location]`):
            Current coordinates of the live location.

        user_id (`Optional[str]`):
            User ID of the person sharing the location.

        status (`Optional[Union[str, rubigram.enums.LiveLocationStatus]]`):
            Status of the live location (Live or Stopped).

        last_update_time (`Optional[str]`):
            Timestamp of the last location update.
    """
    start_time: Optional[str] = None
    live_period: Optional[int] = None
    current_location: Optional[rubigram.types.Location] = None
    user_id: Optional[str] = None
    status: Optional[Union[str, rubigram.enums.LiveLocationStatus]] = None
    last_update_time: Optional[str] = None