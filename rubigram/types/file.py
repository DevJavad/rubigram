#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from .config import Object
import mimetypes
import rubigram



@dataclass
class File(Object):
    """
    **Represents a file object in Rubigram.**
        `from rubigram.types import File`

    Contains metadata about a file, such as its unique identifier,
    name, size, and MIME type.

    Attributes:
        file_id (`str`):
            Unique identifier for the file.

        file_name (`Optional[str]`):
            Name of the file (e.g., 'photo.png').

        size (`Optional[int]`):
            Size of the file in bytes.

        file_type (`Optional[str]`):
            MIME type of the file (e.g., 'image/png', 'video/mp4').
            Automatically detected from the file name if not provided.
    """

    file_id: str
    file_name: Optional[str] = None
    size: Optional[int] = None
    file_type: Optional[str] = None

    def __post_init__(self):
        if not self.file_name:
            self.file_type = rubigram.enums.FileType.FILE
            return

        mime_type, _ = mimetypes.guess_type(self.file_name)
        if not mime_type:
            self.file_type = rubigram.enums.FileType.FILE
            return

        mime_main = mime_type.split("/")[0]
        mime_sub = mime_type.split("/")[1]

        if mime_main == "image":

            if mime_sub == "gif":
                self.file_type = rubigram.enums.FileType.GIF

            else:
                self.file_type = rubigram.enums.FileType.IMAGE

        elif mime_main == "video":
            self.file_type = rubigram.enums.FileType.VIDEO

        elif mime_main == "audio":

            if mime_sub in ["ogg", "amr", "m4a"]:
                self.file_type = rubigram.enums.FileType.VOICE

            else:
                self.file_type = rubigram.enums.FileType.MUSIC

        else:
            self.file_type = rubigram.enums.FileType.FILE