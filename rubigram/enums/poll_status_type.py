#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class PollStatusType(Enum):
    """
    **Represents the status of a poll.**
        `from rubigram.enums import PollStatusType`

    Attributes:
        OPEN (str): The poll is currently open and accepting votes.
        CLOSED (str): The poll is closed and no longer accepting votes.
    """

    OPEN = "Open"
    CLOSED = "Closed"