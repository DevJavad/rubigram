#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO, TYPE_CHECKING
from rubigram.utils import AutoDelete, Parser
from pathlib import Path
import rubigram

if TYPE_CHECKING:
    from rubigram.types import Keypad, UMessage
    from rubigram.enums import FileType, ChatKeypadType, ParseMode


class SendFile:
    """
    File sender for Rubika API.

    This class provides an asynchronous method to send files to a
    chat. Supports sending local files, remote URLs, bytes, file-like
    objects, or existing File IDs. Handles uploading, metadata parsing,
    keypads, notifications, replies, and optional auto-deletion.
    """
    __slots__ = ()

    async def send_file(
        self: rubigram.Client,
        chat_id: str,
        file: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        type: Union[str, FileType] = FileType.FILE,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[ChatKeypadType] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        parse_mode: Optional[Union[str, ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        Send a file to a chat on Rubika.

        Parameters:
            chat_id (str):
                Unique identifier of the chat to send the file to.
            file (Union[str, bytes, BinaryIO]):
                File path, URL, bytes, file-like object, or existing File ID.
            caption (Optional[str], default=None):
                Caption or text to send with the file.
            filename (Optional[str], default=None):
                Custom file name for uploads. Inferred if not provided.
            type (Union[str, rubigram.enums.FileType], default="File"):
                Type of the file to send (e.g., File, Image, Video).
            chat_keypad (Optional[rubigram.types.Keypad], default=None):
                Custom chat keypad to attach to the message.
            inline_keypad (Optional[rubigram.types.Keypad], default=None):
                Inline keypad to attach to the message.
            chat_keypad_type (Optional[rubigram.enums.ChatKeypadType], default=None):
                Type of chat keypad (e.g., persistent, one-time).
            disable_notification (bool, default=False):
                If True, sends the message silently.
            reply_to_message_id (Optional[str], default=None):
                Message ID to reply to.
            auto_delete (Optional[int], default=None):
                Time in seconds after which the message will be deleted automatically.

        Returns:
            rubigram.types.UMessage:
                The sent message object.

        Example:
        .. code-block:: python
            # Send a local file
            message = await client.send_file(chat_id="chat_id", file="example.jpg")

            # Send a file from URL
            message = await client.send_file(chat_id="chat_id", file="https://example.com/file.png")

            # Send an existing file by File ID
            message = await client.send_file(chat_id="chat_id", file="file_id")

            # Send bytes
            message = await client.send_file(chat_id="chat_id", file=b"binary data")
        """
        upload_url = await self.request_send_file(type)

        if isinstance(file, str):
            if file.startswith(("http://", "https://")) or Path(file).exists():
                file_id = await self.upload_file(upload_url, file, filename)
            else:
                download_url = await self.get_file(file)
                if not download_url:
                    raise ValueError(f"Invalid file_id: {file}")
                file_id = await self.upload_file(upload_url, download_url, filename)
        else:
            file_id = await self.upload_file(upload_url, file, filename)

        data = {"chat_id": chat_id, "file_id": file_id, "text": caption}
        if caption:
            parse = Parser.parser(caption, parse_mode or self.parse_mode)

            if "metadata" in parse:
                data["text"] = parse["text"]
                data["metadata"] = parse["metadata"]

        if chat_keypad:
            data["chat_keypad"] = chat_keypad.as_dict()

        if inline_keypad:
            data["inline_keypad"] = inline_keypad.as_dict()

        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        if disable_notification:
            data["disable_notification"] = disable_notification

        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        response = await self.request("sendFile", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id
        message.file_id = file_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message