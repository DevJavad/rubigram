#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO, TYPE_CHECKING
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import FileType, ChatKeypadType, ParseMode


class SendMusic:
    """
    Music sender for Rubika API.

    This class provides an asynchronous method to send music/audio
    files to a chat. It is a specialized wrapper around `send_file`
    that automatically sets the file type to Music and supports
    captions, keypads, notifications, replies, and auto-deletion.
    """

    __slots__ = ()

    async def send_music(
        self: rubigram.Client,
        chat_id: str,
        music: Union[str, bytes, BinaryIO],
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
        """
        Send a music/audio file to a chat on Rubika.

        Parameters:
            chat_id (str):
                Unique identifier of the target chat.
            music (Union[str, bytes, BinaryIO]):
                Music source. Can be a local file path, URL, bytes,
                file-like object, or an existing File ID.
            caption (Optional[str], default=None):
                Caption or description for the music.
            filename (Optional[str], default=None):
                Custom filename for the uploaded music.
            chat_keypad (Optional[rubigram.types.Keypad], default=None):
                Custom chat keypad to attach to the message.
            inline_keypad (Optional[rubigram.types.Keypad], default=None):
                Inline keypad to attach to the message.
            chat_keypad_type (Optional[rubigram.enums.ChatKeypadType], default=None):
                Type of chat keypad.
            disable_notification (bool, default=False):
                If True, sends the message silently.
            reply_to_message_id (Optional[str], default=None):
                Message ID to reply to.
            auto_delete (Optional[int], default=None):
                Time in seconds after which the message will be
                automatically deleted.

        Returns:
            rubigram.types.UMessage:
                The sent music message object.

        Example:
        .. code-block:: python
            # Send a local file
            message = await client.send_music(chat_id="chat_id", music="example.mp3")

            # Send a file from URL
            message = await client.send_music(chat_id="chat_id", music="https://example.com/file.mp3")

            # Send an existing file by File ID
            message = await client.send_music(chat_id="chat_id", music="file_id")

            # Send bytes
            message = await client.send_music(chat_id="chat_id", music=b"binary data")
            )
        """
        return await self.send_file(
            chat_id,
            music,
            caption,
            filename,
            FileType.MUSIC,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            parse_mode,
            auto_delete
        )