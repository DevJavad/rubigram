#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class UpdateType(Enum):
    """
    **Represents the types of updates that can occur in a chat or bot.**
        `from rubigram.enums import UpdateType`

    Attributes:
        UPDATED_MESSAGE (str): A message was updated.
        NEW_MESSAGE (str): A new message was received.
        REMOVED_MESSAGE (str): A message was removed.
        STARTED_BOT (str): A bot was started.
        STOPPED_BOT (str): A bot was stopped.
        UPDATED_PAYMENT (str): A payment status was updated.
    """

    UPDATED_MESSAGE = "UpdatedMessage"
    NEW_MESSAGE = "NewMessage"
    REMOVED_MESSAGE = "RemovedMessage"
    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"
    UPDATED_PAYMENT = "UpdatedPayment"