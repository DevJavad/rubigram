import enum


class Enum(str, enum.Enum):
    def __str__(self):
        return f"rubigram.enums.{self.__class__.__name__}.{self.name}"