#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from .config import Object
import rubigram


@dataclass
class PaymentStatus(Object):
    """
    **Represents the payment status of a transaction in Rubigram.**
        `from rubigram.types import PaymentStatus`

    Tracks the unique payment ID and the current status of the payment.

    Attributes:
        payment_id (`Optional[str]`):
            Unique identifier for the payment.

        status (`Optional[Union[str, rubigram.enums.PaymentStatusType]]`):
            Current status of the payment, either as a string or as an enum (Paid, NotPaid).
    """
    payment_id: Optional[str] = None
    status: Optional[Union[str, rubigram.enums.PaymentStatusType]] = None