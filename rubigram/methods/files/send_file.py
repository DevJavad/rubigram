#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO
from pathlib import Path
from rubigram.utils import AutoDelete, Parser
import rubigram


class SendFile:

    __slots__ = ()

    async def send_file(
        self: rubigram.Client,
        chat_id: str,
        file: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        type: Union[str, rubigram.enums.FileType] = rubigram.enums.FileType.FILE,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[rubigram.enums.ChatKeypadType] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> rubigram.types.UMessage:
        """
        Send a file to a chat on Rubika.

        This method handles uploading a file from various sources (local path, URL,
        file ID, bytes, or file-like objects) and sends it to the specified chat.
        Supports optional captions, inline or chat keyboards, message parsing,
        auto-delete, and notification settings.

        Parameters:
            chat_id (str):
                The target chat ID where the file will be sent.

            file (Union[str, bytes, BinaryIO]):
                The file to send. Can be:
                - Local file path (str or Path)
                - HTTP/HTTPS URL (str)
                - Existing Rubika file_id (str)
                - Bytes or BinaryIO stream

            caption (Optional[str]):
                Text caption for the file.

            filename (Optional[str]):
                Custom filename for the uploaded file.

            type (Union[str, rubigram.enums.FileType], default=FileType.FILE):
                Type of file being sent.

            chat_keypad (Optional[rubigram.types.Keypad]):
                Keypad to attach to the chat message.

            inline_keypad (Optional[rubigram.types.Keypad]):
                Keypad to attach inline with the message.

            chat_keypad_type (Optional[rubigram.enums.ChatKeypadType]):
                Type of chat keyboard (e.g., INLINE, REPLY).

            disable_notification (bool, default=False):
                If True, sends the message silently.

            reply_to_message_id (Optional[str]):
                ID of a message to reply to.

            parse_mode (Optional[Union[str, rubigram.enums.ParseMode]]):
                Text formatting mode for the caption.

            auto_delete (Optional[int]):
                Number of seconds after which the message will be automatically deleted.

            headers (Optional[dict]):
                Optional HTTP headers for the upload request.

            proxy (Optional[str]):
                Optional proxy URL to use for requests.

            retries (Optional[int]):
                Number of retry attempts on request failure.

            delay (Optional[float]):
                Initial delay between retries in seconds.

            backoff (Optional[float]):
                Backoff multiplier applied after each retry.

            max_delay (Optional[float]):
                Maximum delay between retries.

            timeout (Optional[float]):
                Total request timeout in seconds.

            connect_timeout (Optional[float]):
                Timeout for establishing the connection.

            read_timeout (Optional[float]):
                Timeout for reading the response data.

        Returns:
            rubigram.types.UMessage:
                The message object representing the sent file.

        Example:
        .. code-block:: python
            message = await client.send_file(
                chat_id="123456",
                file="path/to/file.mp4",
                caption="Check this out!",
                chat_keypad=my_keypad,
                auto_delete=60
            )
        """

        if not chat_id:
            raise ValueError("chat_id is required")

        if not isinstance(file, (str, bytes)) and not hasattr(file, "read"):
            raise TypeError("file must be str, bytes, or BinaryIO")

        type = type if isinstance(type, str) else type.value

        upload_url = await self.request_send_file(type)
        if not upload_url:
            raise RuntimeError("Failed to get upload_url")

        source = None

        if isinstance(file, str):
            if file.startswith(("http://", "https://")):
                source = file

            elif Path(file).exists():
                source = Path(file)

            else:
                download_url = await self.get_file(file)
                if not download_url:
                    raise ValueError("Invalid file_id: %s", file_id)
                source = download_url
        else:
            source = file

        file_id = await self.upload_file(
            upload_url,
            source,
            filename,
            headers,
            proxy,
            timeout,
            connect_timeout,
            read_timeout
        )

        if not file_id:
            raise RuntimeError("Upload succeeded but file_id is missing")

        data = {
            "chat_id": chat_id,
            "file_id": file_id
        }

        if caption:
            parsed = Parser.parser(caption, parse_mode or self.parse_mode)
            data["text"] = parsed.get("text", caption)
            if "metadata" in parsed:
                data["metadata"] = parsed["metadata"]

        if chat_keypad:
            data["chat_keypad"] = chat_keypad.as_dict()

        if inline_keypad:
            data["inline_keypad"] = inline_keypad.as_dict()

        if chat_keypad_type:
            data["chat_keypad_type"] = (
                chat_keypad_type.value
                if hasattr(chat_keypad_type, "value")
                else chat_keypad_type
            )

        if disable_notification:
            data["disable_notification"] = True

        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        response = await self.request(
            "sendFile",
            data,
            headers,
            proxy,
            retries,
            delay,
            backoff,
            max_delay,
            timeout,
            connect_timeout,
            read_timeout
        )

        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id
        message.file_id = file_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message