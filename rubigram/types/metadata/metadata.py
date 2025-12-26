#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from ..config import Object

if TYPE_CHECKING:
    from rubigram.types import MetadataParts


@dataclass
class Metadata(Object):
    """
    **Represents metadata for messages or files.**
        `from rubigram.types import MetaData`

    This class contains metadata information that can be attached to
    messages or files, typically used for additional context or
    structured data.

    Attributes:
        meta_data_parts (`Optional[list[rubigram.types.MetadataParts]]`):
            List of metadata parts containing key-value pairs or
            structured data components.
    """
    meta_data_parts: Optional[list[MetadataParts]] = None

    @classmethod
    def parse(cls, data: dict, client=None):
        """
        Parse dict into a MetaData object.
        """
        data = data or {}
        parts = [
            MetadataParts.parse(part, client)
            if isinstance(part, dict)
            else part
            for part in data.get("meta_data_parts", []) or []
        ]
        return cls(meta_data_parts=parts)