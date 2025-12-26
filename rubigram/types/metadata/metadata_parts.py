#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object




@dataclass
class MetadataParts(Object):
    """
    **Represents a part of metadata with specific attributes.**
        `from rubigram.types import MetaDataParts`

    This class defines individual components of metadata that can be
    used to annotate messages with links, mentions, or other structured data.

    Attributes:
        from_index (`Optional[int]`):
            The starting index position in the text where this metadata applies.

        length (`Optional[int]`):
            The length of the text segment this metadata applies to.

        type (`Optional[str]`):
            The type of metadata (e.g., "link", "mention", "hashtag").

        link_url (`Optional[str]`):
            The URL for link-type metadata.

        mention_text_user_id (`Optional[str]`):
            The user ID for mention-type metadata.
    """
    from_index: int
    length: int
    type: Union[str] = None
    link_url: Optional[str] = None
    mention_text_user_id: Optional[str] = None