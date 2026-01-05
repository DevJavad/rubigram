from typing import Any
import enum


class Enum(str, enum.Enum):
    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}({self.value})"

    @classmethod
    def values(cls) -> list[str]:
        return [i.value for i in cls]

    @classmethod
    def hasvalue(cls, value: Any) -> bool:
        return value in cls._value2member_map_