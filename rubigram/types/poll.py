#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from .config import Object

if TYPE_CHECKING:
    from rubigram.types import PollStatus


@dataclass
class Poll(Object):
    """
    **Represents a poll in Rubigram.**
        `from rubigram.types import Poll`

    Attributes:
        question (`Optional[str]`):
            The poll question text.

        options (`Optional[list[str]]`):
            List of possible answer options.

        poll_status (`Optional[rubigram.types.PollStatus]`):
            Status information of the poll.
    """
    question: Optional[str] = None
    options: Optional[list[str]] = None
    poll_status: Optional[PollStatus] = None