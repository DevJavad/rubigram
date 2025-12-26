#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from dataclasses import dataclass
from .config import Object


@dataclass
class Location(Object):
    """
    **Represents a geographical location.**
        `from rubigram.types import Location`

    Attributes:
        longitude (`str`):
            Longitude of the location.

        latitude (`str`):
            Latitude of the location.
    """
    longitude: str
    latitude: str