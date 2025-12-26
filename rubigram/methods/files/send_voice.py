#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO, TYPE_CHECKING
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import FileType, ChatKeypadType, ParseMode


class SendVoice:
    """
    Voice message sender for Rubika API.

    This class provides an asynchronous method to send voice/audio
    messages to a chat. It is a specialized wrapper around `send_file`
    that automatically sets the file type to Voice and supports
    captions, keypads, notifications, replies, and auto-deletion.
    """

    __slots__ = ()

    async def send_voice(
        self: rubigram.Client,
        chat_id: str,
        voice: Union[str, bytes, BinaryIO],
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
        Send a voice message to a chat on Rubika.

        Parameters:
            chat_id (str):
                Unique identifier of the target chat.
            voice (Union[str, bytes, BinaryIO]):
                Voice source. Can be a local file path, URL, bytes,
                file-like object, or an existing File ID.
            caption (Optional[str], default=None):
                Caption or text to send with the voice message.
            filename (Optional[str], default=None):
                Custom filename for the uploaded voice file.
            chat_keypad (Optional[rubigram.types.Keypad], default=None):
                Custom chat keypad to attach to the message.
            inline_keypad (Optional[rubigram.types.Keypad], default=None):
                Inline keypad to attach to the message.
            chat_keypad_type (Optional[rubigram.enums.ChatKeypadType], default=None):
                Type of chat keypad.
            disable_notification (Optional[bool], default=False):
                If True, sends the message silently.
            reply_to_message_id (Optional[str], default=None):
                Message ID to reply to.
            auto_delete (Optional[int], default=None):
                Time in seconds after which the message will be
                automatically deleted.

        Returns:
            rubigram.types.UMessage:
                The sent voice message object.

        Example:
        .. code-block:: python
            # Send a local voice file
            message = await client.send_voice(chat_id="chat_id", voice="voice.ogg")

            # Send a voice message from URL
            message = await client.send_voice(chat_id="chat_id", voice="https://example.com/voice.ogg")

            # Send an existing voice by File ID
            message = await client.send_voice(chat_id="chat_id", voice="file_id")

            # Send voice bytes
            message = await client.send_voice(chat_id="chat_id", voice=b"binary data")
        """
        return await self.send_file(
            chat_id,
            voice,
            caption,
            filename,
            FileType.VOICE,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )