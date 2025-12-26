#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram

from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from rubigram.utils import Parser
import rubigram

if TYPE_CHECKING:
    from rubigram.enums import ParseMode


class EditMessageText:
    async def edit_message_text(
        self: rubigram.Client,
        chat_id: str,
        message_id: str,
        text: str,
        parse_mode: Optional[Union[str, ParseMode]] = None
    ):
        """
        **Edit the text content of an existing message.**
            `await client.edit_message_text(chat_id, message_id, text)`

        This method updates the text content of a previously sent message
        while preserving other message components like inline keyboards
        and attachments.

        Args:
            chat_id (`str`):
                The ID of the chat where the message is located.

            message_id (`str`):
                The ID of the message to update.

            text (`str`):
                The new text content for the message.

        Returns:
            dict: The API response from Rubigram containing the updated message data.

        Example:
        .. code-block:: python

            # Edit a message's text content
            await client.edit_message_text(
                chat_id=chat_id
                message_id=message_id,
                text=text
            )

        Note:
            This method only modifies the text content of the message.
            Other message elements like inline keyboards, files, or media
            remain unchanged.
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }

        parse = Parser.parser(text, parse_mode or self.parse_mode)

        if "metadata" in parse:
            data["text"] = parse["text"]
            data["metadata"] = parse["metadata"]

        return await self.request("editMessageText", data)