#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO
import rubigram


class SendGif:

    __slots__ = ()

    async def send_gif(
        self: rubigram.Client,
        chat_id: str,
        gif: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
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
        Send a GIF file to a chat on Rubika.

        This is a convenience wrapper around :meth:`send_file` specifically for sending
        GIFs. Supports the same parameters as `send_file` including captions, keyboards,
        message parsing, auto-delete, and notification options.

        Parameters:
            chat_id (str):
                The target chat ID where the GIF will be sent.

            gif (Union[str, bytes, BinaryIO]):
                The GIF to send. Can be:
                - Local file path (str)
                - HTTP/HTTPS URL (str)
                - Bytes or BinaryIO stream

            caption (Optional[str]):
                Text caption for the GIF.

            filename (Optional[str]):
                Custom filename for the uploaded GIF.

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
                The message object representing the sent GIF.

        Example:
        .. code-block:: python
            message = await client.send_gif(
                chat_id="123456",
                gif="path/to/animation.gif",
                caption="Look at this!",
                auto_delete=60
            )
        """

        return await self.send_file(
            chat_id,
            gif,
            caption,
            filename,
            rubigram.enums.FileType.GIF,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
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