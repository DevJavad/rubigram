#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from dataclasses import dataclass
from ..config import Object

if TYPE_CHECKING:
    from rubigram.enums import ButtonType
    from rubigram.types import (
        ButtonSelection,
        ButtonCalendar,
        ButtonNumberPicker,
        ButtonStringPicker,
        ButtonLocation,
        ButtonTextbox
    )


@dataclass
class Button(Object):
    """
    **Represents a generic interactive button in a chat keypad.**
        `from rubigram.types import Button`

    Attributes:
        id (`str`):
            Unique identifier of the button.

        button_text (`str`):
            Text displayed on the button.

        type (`Optional[Union[str, rubigram.enums.ButtonType]]`):
            Type of the button.

        button_selection (`Optional[rubigram.types.ButtonSelection]`):
            Selection-type button.

        button_calendar (`Optional[rubigram.types.ButtonCalendar]`):
            Calendar-type button.

        button_number_picker (`Optional[rubigram.types.ButtonNumberPicker]`):
            Number-picker button.

        button_string_picker (`Optional[rubigram.types.ButtonStringPicker]`):
            String-picker button.

        button_location (`Optional[rubigram.types.ButtonLocation]`):
            Location picker button.

        button_textbox (`Optional[rubigram.types.ButtonTextbox]`):
            Textbox input button.

        button_link (`Optional[rubigram.types.ButtonLink]`):
            Link-type button.
    """
    id: str
    button_text: str
    type: Optional[Union[str, ButtonType]] = ButtonType.SIMPLE
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None