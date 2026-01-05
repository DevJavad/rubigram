#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO
import rubigram


class SendDocument:

    __slots__ = ()

    async def send_document(
        self: rubigram.Client,
        chat_id: str,
        document: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[rubigram.enums.ChatKeypadType] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        metadata: Optional[rubigram.types.Metadata] = None,
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
        Send a document file to a chat on Rubika.

        This is a convenience wrapper around :meth:`send_file` specifically for sending
        document files. Supports the same parameters as `send_file` including captions, keyboards,
        message parsing, auto-delete, and notification options.

        Note: Uses `FileType.FILE` for document files. Ensure the file format is supported by Rubika.

        Parameters:
            chat_id (str):
                The target chat ID where the document will be sent.

            document (Union[str, bytes, BinaryIO]):
                The document file to send. Can be:
                - Local file path (str)
                - HTTP/HTTPS URL (str)
                - Bytes or BinaryIO stream

            caption (Optional[str], default: None):
                Text caption for the document file.

            filename (Optional[str], default: None):
                Custom filename for the uploaded document file.

            chat_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach to the chat message.

            inline_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach inline with the message.

            chat_keypad_type (Optional[rubigram.enums.ChatKeypadType], default: None):
                Type of chat keyboard (e.g., INLINE, REPLY).

            disable_notification (bool, default: False):
                If True, sends the message silently.

            reply_to_message_id (Optional[str], default: None):
                ID of a message to reply to.

            parse_mode (Optional[Union[str, rubigram.enums.ParseMode]], default: None):
                Text formatting mode for the caption.

            auto_delete (Optional[int], default: None):
                Number of seconds after which the message will be automatically deleted.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the upload request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for requests.

            retries (Optional[int], default: None):
                Number of retry attempts on request failure.

            delay (Optional[float], default: None):
                Initial delay between retries in seconds.

            backoff (Optional[float], default: None):
                Backoff multiplier applied after each retry.

            max_delay (Optional[float], default: None):
                Maximum delay between retries.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            rubigram.types.UMessage:
                The message object representing the sent document file.

        Example:
        .. code-block:: python
            # Send document from local file
            message = await client.send_document(
                chat_id="123456",
                document="path/to/document.pdf",
                caption="Listen to this track!",
                auto_delete=120
            )

            # Send document from URL
            message = await client.send_document(
                chat_id="789012",
                document="https://example.com/document.pdf",
                caption="document from the web"
            )

            # Send document as bytes
            with open("fdocument.pdf", "rb") as f:
                document_bytes = f.read()
            message = await client.send_document(
                chat_id="345678",
                document=document_bytes,
                filename="custom_name.pdf"
            )
        """
        return await self.send_file(
            chat_id,
            document,
            caption,
            filename,
            rubigram.enums.FileType.FILE,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            metadata,
            parse_mode,
            auto_delete,
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