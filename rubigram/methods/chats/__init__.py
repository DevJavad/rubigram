#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .get_chat import GetChat
from .get_chat_member import GetChatMember
from .ban_chat_member import BanChatMember
from .unban_chat_member import UnbanChatMember


class Chats(
    GetChat,
    GetChatMember,
    BanChatMember,
    UnbanChatMember
):
    pass