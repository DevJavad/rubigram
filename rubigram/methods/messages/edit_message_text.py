#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.utils import Parser
import rubigram


class EditMessageText:
    async def edit_message_text(
        self: rubigram.Client,
        chat_id: str,
        message_id: str,
        text: str,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ):
        """
        Edit the text content of an existing message on Rubika.

        This method allows you to modify the text of a message that was previously sent.
        Supports text parsing with metadata for formatted content.

        Parameters:
            chat_id (str):
                The chat ID containing the message to edit.
                Must be a non-empty string.

            message_id (str):
                The ID of the message to edit.
                Must be a non-empty string.

            text (str):
                The new text content for the message.
                Must be a non-empty string.

            parse_mode (Optional[Union[str, rubigram.enums.ParseMode]], default: None):
                Text formatting mode for the new text content.
                If not provided, uses the client's default parse_mode.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the request.

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
            dict:
                The API response from Rubika after editing the message text.

        Raises:
            ValueError:
                If `chat_id`, `message_id`, or `text` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Edit message with plain text
            result = await client.edit_message_text(
                chat_id="123456",
                message_id="msg_789",
                text="This is the updated message text"
            )
            
            # Edit message with formatted text
            result = await client.edit_message_text(
                chat_id="123456",
                message_id="msg_789",
                text="*Bold text* and _italic text_",
                parse_mode="Markdown"
            )
            
            # Edit message using enum for parse_mode
            from rubigram.enums import ParseMode
            
            result = await client.edit_message_text(
                chat_id="123456",
                message_id="msg_789",
                text="<b>Bold HTML</b> and <i>italic HTML</i>",
                parse_mode=ParseMode.HTML
            )

        Note:
            - You can only edit messages sent by the bot
            - There may be time limits on editing messages
            - The parser automatically extracts metadata for formatted text
            - If metadata is present in parsed text, it's included in the request
        """
        if not chat_id:
            raise ValueError("Parameter 'chat_id' must be a non-empty string")
        if not message_id:
            raise ValueError("Parameter 'message_id' must be a non-empty string")
        if not text:
            raise ValueError("Parameter 'text' must be a non-empty string")

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }

        parse = Parser.parser(text, parse_mode or self.parse_mode)

        if "metadata" in parse:
            data["text"] = parse["text"]
            data["metadata"] = parse["metadata"]

        return await self.request(
            "editMessageText",
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