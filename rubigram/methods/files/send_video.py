#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO, TYPE_CHECKING
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import FileType, ChatKeypadType, ParseMode


class SendVideo:
    """
    Video sender for Rubika API.

    This class provides an asynchronous method to send video files
    to a chat. It is a specialized wrapper around `send_file` that
    automatically sets the file type to Video and supports captions,
    keypads, notifications, replies, and auto-deletion.
    """

    __slots__ = ()

    async def send_video(
        self: rubigram.Client,
        chat_id: str,
        video: Union[str, bytes, BinaryIO],
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
        Send a video to a chat on Rubika.

        Parameters:
            chat_id (str):
                Unique identifier of the target chat.
            video (Union[str, bytes, BinaryIO]):
                Video source. Can be a local file path, URL, bytes,
                file-like object, or an existing File ID.
            caption (Optional[str], default=None):
                Caption or text to send with the video.
            filename (Optional[str], default=None):
                Custom filename for the uploaded video.
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
                The sent video message object.

        Example:
        .. code-block:: python
            # Send a local video
            message = await client.send_video(chat_id="chat_id", video="video.mp4")

            # Send a video from URL
            message = await client.send_video(chat_id="chat_id", video="https://example.com/video.mp4")

            # Send an existing video by File ID
            message = await client.send_video(chat_id="chat_id", video="file_id")

            # Send video bytes
            message = await client.send_video(chat_id="chat_id", video=b"binary data")
        """
        return await self.send_file(
            chat_id,
            video,
            caption,
            filename,
            FileType.VIDEO,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            parse_mode,
            auto_delete
        )