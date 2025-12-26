#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO, TYPE_CHECKING
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import FileType, ChatKeypadType, ParseMode


class SendGif:
    """
    Gif sender for Rubika API.

    This class provides an asynchronous method to send Gif
    files to a chat. It is a specialized wrapper around `send_gif`
    that automatically sets the file type to Gif and supports
    captions, keypads, notifications, replies, and auto-deletion.
    """

    __slots__ = ()

    async def send_gif(
        self: rubigram.Client,
        chat_id: str,
        gif: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[ChatKeypadType] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        parse_mode: Optional[Union[str, ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        return await self.send_file(
            chat_id,
            gif,
            caption,
            filename,
            FileType.GIF,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            parse_mode,
            auto_delete
        )