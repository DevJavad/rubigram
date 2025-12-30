#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class UpdateEndpointType(Enum):
    """
    **Represents the types of endpoints that can trigger updates.**
        `from rubigram.enums import UpdateEndpointType`

    Attributes:
        RECEIVE_UPDATE (str): Updates triggered by receiving a standard update.
        RECEIVE_INLINE_MESSAGE (str): Updates triggered by receiving an inline message.
        RECEIVE_QUERY (str): Updates triggered by receiving a query.
        GET_SELECTION_ITEM (str): Updates triggered when retrieving a selection item.
        SEARCH_SELECTION_ITEMS (str): Updates triggered when searching selection items.
    """

    RECEIVE_UPDATE = "ReceiveUpdate"
    RECEIVE_INLINE_MESSAGE = "ReceiveInlineMessage"
    RECEIVE_QUERY = "ReceiveQuery"
    GET_SELECTION_ITEM = "GetSelectionItem"
    SEARCH_SELECTION_ITEMS = "SearchSelectionItems"