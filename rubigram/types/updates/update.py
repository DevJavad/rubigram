#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union, BinaryIO
from dataclasses import dataclass
from ..config import Object
from io import BytesIO
import rubigram


@dataclass
class Update(Object):
    """
    **Represents an incoming update in Rubigram.**
        `from rubigram.types import Update`

    An update can include new messages, edited messages, deleted messages,
    payment updates, and other types of events that occur in a chat.

    Attributes:
        type (`rubigram.enums.UpdateType`):
            The type of the update (e.g., new message, edited message).

        chat_id (`str`):
            The chat ID related to this update.

        removed_message_id (`Optional[str]`):
            The ID of a deleted message, if applicable.

        new_message (`Optional[rubigram.types.Message]`):
            The new message associated with this update.

        updated_message (`Optional[rubigram.types.Message]`):
            The updated message associated with this update.

        updated_payment (`Optional[rubigram.types.PaymentStatus]`):
            Payment status update, if applicable.

        client (`Optional[rubigram.Client]`):
            The Rubigram client bound to this update for sending replies, etc.
    """
    type: Union[str, rubigram.enums.UpdateType]
    chat_id: str
    update_time: Optional[int] = None
    removed_message_id: Optional[str] = None
    new_message: Optional[rubigram.types.Message] = None
    updated_message: Optional[rubigram.types.Message] = None
    updated_payment: Optional[rubigram.types.PaymentStatus] = None
    client: Optional[rubigram.Client] = None

    @property
    def text(self) -> Optional[str]:
        if self.new_message:
            return self.new_message.text
        elif self.updated_message:
            return self.updated_message.text
        return None

    @property
    def message_id(self) -> Optional[str]:
        if self.new_message:
            return self.new_message.message_id
        elif self.updated_message:
            return self.updated_message.message_id
        return None

    @property
    def sender_id(self) -> Optional[str]:
        if self.new_message and self.new_message.sender_id:
            return self.new_message.sender_id
        return None

    async def reply(
        self,
        text: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
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

    async def reply_poll(
        self,
        question: str,
        options: list[str],
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a poll.**

        Args:
            question (`str`):
                The poll question text.

            options (`list[str]`):
                A list of options for the poll.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for the message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent poll message object.

        Example:
        .. code-block:: python

            options = ["option1", "option2"]
            await update.reply_poll(
                question=question,
                options=options
            )
        """
        return await self.client.send_poll(
            self.chat_id,
            question,
            options,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            auto_delete
        )

    async def reply_location(
        self,
        latitude: str,
        longitude: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a location.**
            `await update.reply_location("35.6895", "139.6917")`

        Args:
            latitude (`str`):
                Latitude of the location.

            longitude (`str`):
                Longitude of the location.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent location message.

        Example:
            .. code-block:: python

                await update.reply_location("35.6895", "139.6917")
        """
        return await self.client.send_location(
            self.chat_id,
            latitude,
            longitude,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            auto_delete
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a contact.**

        Args:
            phone_number (`str`):
                Contact's phone number.

            first_name (`str`):
                Contact's first name.

            last_name (`Optional[str]`):
                Contact's last name.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent contact message.

        Example:
        .. code-block:: python

            await update.reply_contact(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name
            )
        """
        return await self.client.send_contact(
            self.chat_id,
            first_name,
            last_name,
            phone_number,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            auto_delete
        )

    async def reply_sticker(
        self,
        sticker_id: str,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a sticker.**

        Args:
            sticker_id (`str`):
                The ID of the sticker to send.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent sticker message.

        Example:
        .. code-block:: python

            await update.reply_sticker(sticker_id=sticker_id)
        """
        return await self.client.send_sticker(
            self.chat_id,
            sticker_id,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            auto_delete
        )

    async def reply_file(
        self,
        file: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        type: Optional[Union[str, rubigram.enums.FileType]] = rubigram.enums.FileType.FILE,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a file.**

        Args:
            file (`Union[str, bytes, BinaryIO]`):
                The file path or binary data to send.

            caption (`Optional[str]`):
                Caption for the file. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            type (`Optional[Union[str, rubigram.enums.FileType]]`):
                Type of the file (File, Document, etc.). Defaults to File.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to show in chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keypad to show. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent file message.

        Example:
        .. code-block:: python

            file = "home/users/rubigram/project/photo.jpg"
            await update.reply_file(
                file=file,
                caption=caption
            )

            file = "https://rubigram.ir/rubigram.jpg"
            file_name = "photo.jpg"
            await update.reply_file(
                file=file,
                caption=caption,
                file_name=file_name
            )
        """
        return await self.client.send_file(
            self.chat_id,
            file,
            caption,
            file_name,
            type,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            self.message_id,
            parse_mode,
            auto_delete
        )

    async def reply_document(
        self,
        document: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a document file.**

        Args:
            document (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the document to send.

            caption (`Optional[str]`):
                Text caption for the document. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_document(
                document=document,
                caption=caption
            )
        """
        return await self.reply_file(
            document,
            caption,
            file_name,
            rubigram.enums.FileType.FILE,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def reply_photo(
        self,
        photo: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a photo.**

        Args:
            photo (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the photo to send.

            caption (`Optional[str]`):
                Text caption for the photo. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_photo(
                photo=photo,
                caption=caption
            )
        """
        return await self.reply_file(
            photo,
            caption,
            file_name,
            rubigram.enums.FileType.IMAGE,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def reply_video(
        self,
        video: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a video file.**

        Args:
            video (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the video to send.

            caption (`Optional[str]`):
                Text caption for the video. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_video(
                video=video,
                caption=caption
            )
        """
        return await self.reply_file(
            video,
            caption,
            file_name,
            rubigram.enums.FileType.VIDEO,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def reply_gif(
        self,
        gif: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a GIF file.**

        Args:
            gif (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the GIF to send.

            caption (`Optional[str]`):
                Text caption for the GIF. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_gif(
                gif=gif,
                caption=caption
            )
        """
        return await self.reply_file(
            gif,
            caption,
            file_name,
            rubigram.enums.FileType.GIF,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def reply_music(
        self,
        music: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a music/audio file.**

        Args:
            music (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the music file to send.

            caption (`Optional[str]`):
                Text caption for the music. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_music(
                music=music,
                caption=caption
            )
        """
        return await self.reply_file(
            music,
            caption,
            file_name,
            rubigram.enums.FileType.MUSIC,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def reply_voice(
        self,
        voice: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[Union[str, rubigram.enums.ParseMode]] = None,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Reply to the current message with a voice note.**

        Args:
            voice (`Union[str, bytes, BinaryIO]`):
                The path or bytes of the voice file to send.

            caption (`Optional[str]`):
                Text caption for the voice message. Defaults to None.

            file_name (`Optional[str]`):
                Custom name for the file. Defaults to None.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach to the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Keypad to attach inline. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad if applicable. Defaults to None.

            disable_notification (`bool`):
                If True, disables notification for this message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent reply message object.

        Example:
        .. code-block:: python

            await update.reply_voice(
                voice=voice,
                caption=caption
            )
        """
        return await self.reply_file(
            voice,
            caption,
            file_name,
            rubigram.enums.FileType.VOICE,
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            parse_mode,
            auto_delete
        )

    async def download(
        self,
        file_name: Optional[str] = None,
        directory: Optional[str] = None,
        chunk_size: int = 64 * 1024,
        in_memory: bool = False,
    ) -> Union[str, BytesIO]:
        """
        **Download the file attached to the current message.**

        Args:
            save_as (`str`):
                The name (including path if needed) to save the downloaded file as.

        Returns:
            str: The path to the downloaded file.

        Example:
        .. code-block:: python

            save_as = "download/tmp/photo.jpg"
            await update.download(save_as=save_as)
        """
        if self.new_message.sticker:
            file = self.new_message.sticker.file
        elif self.new_message.file:
            file = self.new_message.file
        else:
            raise ValueError("The message is not a file or has not file_id")
        return await self.client.download_file(
            file.file_id,
            file_name or file.file_name,
            directory,
            chunk_size,
            in_memory
        )

    async def forward(
        self,
        chat_id: str,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> rubigram.types.UMessage:
        """
        **Forward the current message to another chat.**

        Args:
            chat_id (`str`):
                The target chat ID to forward the message to.

            disable_notification (`bool`):
                If True, disables notification for the message. Defaults to False.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The forwarded message object in the target chat.

        Example:
        .. code-block:: python

            await update.forward(chat_id=chat_id)
        """
        return await self.client.forward_message(
            self.chat_id,
            self.message_id,
            chat_id,
            disable_notification,
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