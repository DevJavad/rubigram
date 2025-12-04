#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class LiveLocationStatus(Enum):
    """
    **Represents the status of a live location.**
        `from rubigram.enums import LiveLocationStatus`

    Attributes:
        STOPPED (str): The live location has been stopped.
        LIVE (str): The live location is currently active.
    """

    STOPPED = "Stopped"
    LIVE = "Live"