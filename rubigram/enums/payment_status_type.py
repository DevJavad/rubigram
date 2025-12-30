#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class PaymentStatusType(Enum):
    """
    **Represents the payment status of an item or transaction.**
        `from rubigram.enums import PaymentStatusType`

    Attributes:
        PAID (str): The payment has been completed.
        NOT_PAID (str): The payment has not been completed.
    """

    PAID = "Paid"
    NOT_PAID = "NotPaid"