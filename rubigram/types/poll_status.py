#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from .config import Object
import rubigram


@dataclass
class PollStatus(Object):
    """
    **Represents the status of a poll in Rubigram.**
        `from rubigram.types import PollStatus`

    Attributes:
        state (`Optional[Union[str, rubigram.enums.PollStatusType]]`):
            Current state of the poll (Open or Closed).

        selection_index (`Optional[int]`):
            Index of the currently selected option (if any).

        percent_vote_options (`Optional[list[int]]`):
            List of vote percentages for each option.

        total_vote (`Optional[int]`):
            Total number of votes cast in the poll.

        show_total_votes (`Optional[bool]`):
            Whether the total votes are visible to users.
    """
    state: Optional[Union[str, rubigram.enums.PollStatusType]] = None
    selection_index: Optional[int] = None
    percent_vote_options: Optional[list[int]] = None
    total_vote: Optional[int] = None
    show_total_votes: Optional[bool] = None