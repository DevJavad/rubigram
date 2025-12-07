#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .delete_messages import DeleteMessage
from .edit_chat_keypad import EditChatKeypad
from .edit_message_keypad import EditMessageKeypad
from .edit_message_text import EditMessageText
from .edit_message import EditMessage
from .forward_message import ForwardMessage
from .remove_chat_keypad import RemoveChatKeypad
from .send_contact import SendContact
from .send_location import SendLocation
from .send_message import SendMessage
from .send_poll import SendPoll
from .send_sticker import SendSticker


class Messages(
    DeleteMessage,
    EditChatKeypad,
    EditMessageKeypad,
    EditMessageText,
    EditMessage,
    ForwardMessage,
    RemoveChatKeypad,
    SendContact,
    SendLocation,
    SendMessage,
    SendPoll,
    SendSticker
):
    pass