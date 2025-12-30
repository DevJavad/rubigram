#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from .config import Object
import rubigram


@dataclass
class Chat(Object):
    """
    **Represents a chat entity in Rubigram.**
        `from rubigram.types import Chat`

    This object can represent different types of chats such as private, group, or channel.
    It contains identifying and descriptive information about the chat, including user
    details for private chats and titles for groups/channels.

    Attributes:
        chat_id (`str`):
            Unique identifier for the chat.

        chat_type (`rubigram.enums.ChatType`):
            Type of chat (e.g., User, Group, Channel).

        user_id (`str`):
            The user ID of the chat owner (for private chats).

        first_name (`Optional[str]`):
            First name of the user (if applicable).

        last_name (`Optional[str]`):
            Last name of the user (if applicable).

        title (`Optional[str]`):
            Title of the chat (for groups and channels).

        username (`Optional[str]`):
            Username of the chat or user (if available).

        full_name (`Optional[str]`):
            Full name of the user.
    """

    chat_id: str
    chat_type: Union[str, rubigram.enums.ChatType]
    user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @property
    def full_name(self) -> str:
        """
        Return the full name of the user (first + last).

        Combines `first_name` and `last_name` with a space. If one of them
        is missing, it returns only the available name. Returns an empty
        string if both are None.

        Returns:
            str: Full name of the user.
        """
        first = self.first_name or ""
        last = self.last_name or ""
        return (first + " " + last).strip()

    def as_dict(self) -> dict:
        """
        Convert this Chat object into a dictionary representation.

        Extends the base Object.as_dict() method to include the `full_name`
        property in the dictionary output.

        Returns:
            dict: Dictionary containing all chat attributes, including `full_name`.
        """
        data = super().as_dict()
        data["full_name"] = self.full_name
        return data