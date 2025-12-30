from .enum import Enum


class HandlerType(Enum):
    MESSAGE = "NewMessage"
    STOP_BOT = "StoppedBot"
    START_BOT = "StartedBot"
    INLINE = "inline_message"
    EDITED = "UpdatedMessage"
    DELETED = "RemovedMessage"