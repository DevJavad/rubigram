#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from dataclasses import dataclass
from ..config import Object
from io import BytesIO
import rubigram


@dataclass
class UMessage(Object):
    """
    **Represents an updatable message in Rubigram.**
        `from rubigram.types import UMessage`

    This class extends the base message functionality by providing
    methods to edit, delete, and forward messages directly through
    the bound Rubigram client instance.

    Attributes:
        message_id (`Optional[str]`):
            Unique identifier of the message.

        file_id (`Optional[str]`):
            Identifier of the file attached to the message (if any).

        chat_id (`Optional[str]`):
            Identifier of the chat where the message is located.

        client (`Optional[rubigram.Client]`):
            The Rubigram client instance bound to this message.
    """

    message_id: Optional[str] = None
    file_id: Optional[str] = None
    chat_id: Optional[str] = None
    client: Optional["rubigram.Client"] = None

    async def reply(
        self,
        text: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        **Reply to the current message with text and optional keypads.**

        Args:
            text (`str`):
                The text of the reply message.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigramenums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the message. Defaults to None.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

                await update.reply(
                    text=text,
                    chat_keypad=chat_keypad,
                    chat_keypad_type=rubigram.enums.ChatKeypadType.New,
                    disable_notification=True
                )
        """
        return await self.client.send_message(
            self.chat_id,
            text,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            parse_mode,
            auto_delete
        )

    async def delete(self):
        """
        **Delete this message from the chat.**

        Sends a request to Rubigram to remove the message identified
        by this object's `message_id` from its associated chat.

        Example:
        .. code-block:: python

            message = await client.send_message(
                chat_id=chat_id,
                text=text
            )
            await message.delete()

        Returns:
        Raises:
        """
        return await self.client.delete_messages(self.chat_id, self.message_id)

    async def edit(
        self,
        text: Optional[str] = None,
        inline: Optional[rubigram.types.Keypad] = None,
        keypad: Optional[rubigram.types.Keypad] = None,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None
    ) -> None:
        """
        **Edit this message's text, inline keyboard, or chat keypad.**

        This method provides a unified way to update message components such as text,
        inline keyboards, and chat keypads. You can update one or more components
        in a single call.

        Args:
            text (`Optional[str]`):
                New text content to replace the current message text.
                If None, the text remains unchanged.

            inline (`Optional[rubigram.types.Keypad]`):
                New inline keyboard to attach to the message.
                If None, the inline keyboard remains unchanged.

            keypad (`Optional[rubigram.types.Keypad]`):
                New chat keypad to attach to the chat.
                If None, the chat keypad remains unchanged.


        Example:
        .. code-block:: python

            await client.send_message(
                chat_id=chat_id,
                text=text,
                chat_keypad=keypad,
                chat_keypad_type=rubigram.enums.ChatKeypadType.New
            )

            # Edit only the text
            await message.edit(text=new_text)

            # Edit only the chat keyboard
            await message.edit(keypad=new_keypad)

            # Edit both text and keypad
            await message.edit(
                text=new_text,
                keypad=new_keypad
            )

        Returns:
        Raises:
        """
        if text:
            await self.edit_text(text, parse_mode)
        if inline:
            await self.edit_inline(inline)
        if keypad:
            await self.edit_keypad(keypad)

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None
    ):
        """
        **Edit the text content of this message.**

        Updates the text content of the message while preserving other
        message components like inline keyboards or attachments.

        Args:
            text (`str`):
                The new text content for the message.
                Cannot be empty or None.

        Example:
        .. code-block:: python

            message = await client.send_message(
                chat_id=chat_id,
                text=text
            )
            updated_message = await message.edit_text(text=new_text)

        Raises:
            ValueError: If text is empty or None.
            Exception: If the message cannot be edited due to permissions or other issues.
        """
        return await self.client.edit_message_text(
            self.chat_id,
            self.message_id,
            text,
            parse_mode
        )

    async def edit_keypad(
        self,
        keypad: rubigram.types.Keypad
    ):
        """
        **Edit the chat keypad for the chat of this message.**

        Updates the chat keypad (custom keyboard) for the chat where this message
        is located. This affects the keyboard shown to all users in the chat.

        Args:
            keypad (`rubigram.types.Keypad`):
                The new chat keypad to attach to the chat.
                Contains rows of buttons and display settings.

        Example:
        .. code-block:: python

            from rubigram.types import Keypad, KeypadRow, Button

            keypad = Keypad(rows=[
                KeypadRow(buttons=[
                    Button(button_text="Option 1", id="btn1"),
                    Button(button_text="Option 2", id="btn2")
                ])
            ])

            await message.edit_keypad(keypad=keypad)

        Note:
            This method updates the keypad for the entire chat, not just this specific message.
        """
        return await self.client.edit_chat_keypad(
            self.chat_id,
            keypad
        )

    async def edit_inline(
        self,
        inline: rubigram.types.Keypad
    ):
        """
        **Edit the inline keyboard attached to this message.**

        Updates the inline keyboard (buttons displayed below the message)
        for this specific message without affecting the message text.

        Args:
            inline (`rubigram.types.Keypad`):
                The new inline keyboard to attach to the message.
                Contains rows of interactive buttons.

        Example:
        .. code-block:: python
            from rubigram.types import Keypad, KeypadRow, Button

            inline_keypad = Keypad(rows=[
                KeypadRow(buttons=[
                    Button(button_text="Like", id="like_btn"),
                    Button(button_text="Share", id="share_btn")
                ])
            ])

            updated_message = await message.edit_inline(inline=inline_keypad)

        Note:
            This method only affects the inline keyboard of this specific message,
            not the chat's main keypad.
        """
        return await self.client.edit_message_keypad(
            self.chat_id,
            self.message_id,
            inline
        )

    async def forward(
        self,
        chat_id: str,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> UMessage:
        """
        **Forward this message to another chat.**

        Forwards this message to the specified target chat while preserving
        all message content, attachments, and metadata.

        Args:
            chat_id (`str`):
                The target chat ID to forward the message to.

        Returns:
            UMessage: The forwarded message object in the target chat.

        Example:
        .. code-block:: python
            message = await client.send_message(
                chat_id=chat_id,
                text=text
            )
            await message.forward(chat_id=chat_id)
        """
        return await self.client.forward_message(
            self.chat_id,
            self.message_id,
            chat_id,
            disable_notification,
            auto_delete
        )
        
    async def download(
        self,
        file_name: Optional[str] = None,
        directory: Optional[str] = None,
        chunk_size: int = 64 * 1024,
        in_memory: bool = False,
    ) -> Union[str, BytesIO]:
        return await self.client.download_file(
            self.file_id,
            file_name,
            directory,
            chunk_size,
            in_memory
        )