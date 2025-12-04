#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from dataclasses import dataclass
from .config import Object


@dataclass
class ContactMessage(Object):
    """
    **Represents a contact message containing user contact information.**
        `from rubigram.types import ContactMessage`

    Attributes:
        phone_number (`str`):
            The contact's phone number.

        first_name (`Optional[str]`):
            The contact's first name.

        last_name (`Optional[str]`):
            The contact's last name.
    """
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None