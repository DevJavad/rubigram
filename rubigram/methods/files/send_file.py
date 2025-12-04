#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
from rubigram.utils import AutoDelete, Parser
import rubigram


class SendFile:
    async def send_file(
        self: "rubigram.Client",
        chat_id: str,
        file: Optional[Union[str, bytes, BinaryIO]] = None,
        file_id: Optional[str] = None,
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        type: Union[str, "rubigram.enums.FileType"] = "File",
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None,
        chat_keypad_type: Optional["rubigram.enums.ChatKeypadType"] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Send a file to a chat.**
            `await client.send_file(chat_id, file, caption="File description")`

        This method sends a file to the specified chat. The file can be a local path,
        bytes, or file-like object. The file is automatically uploaded to Rubigram's
        servers before being sent.

        Args:
            chat_id (`str`):
                The ID of the chat where the file will be sent.

            file (`Union[str, bytes, BinaryIO]`):
                The file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the file. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the file. Defaults to None.

            type (`Optional[Union[str, rubigram.enums.FileType]]`):
                Type of the file. Defaults to FileType.File.
                Available types: File, Image, Video, Gif, Music, Voice.

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Custom keyboard to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keyboard to attach to the message. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad. Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the message. Defaults to False.

            reply_to_message_id (`Optional[str]`):
                ID of the message to reply to. Defaults to None.

            auto_delete (`Optional[int]`):
                Number of seconds after which the message will be automatically deleted.

        Returns:
            rubigram.types.UMessage: The sent file message object.

        Example:
        .. code-block:: python

            # Send a local file with caption
            message = await client.send_file(
                chat_id="g0123456789",
                file="document.pdf",
                caption="Here is the document you requested",
                type=rubigram.enums.FileType.File
            )

            # Send bytes data with auto-delete
            with open("photo.jpg", "rb") as f:
                message = await client.send_file(
                    chat_id="g0123456789",
                    file=f.read(),
                    filename="photo.jpg",
                    type=rubigram.enums.FileType.Image,
                    auto_delete=60  # Delete after 60 seconds
                )

        Note:
            - Files are automatically uploaded to Rubigram's servers
            - File type affects how the file is displayed in the chat
            - Auto-delete runs asynchronously in the background
        """
        upload_url = await self.request_send_file(type)

        if file_id is None:
            main_file_id = await self.upload_file(upload_url, file, filename)

        else:
            download_url = await self.get_file(file_id)
            main_file_id = await self.upload_file(upload_url, download_url, filename)

        data = {"chat_id": chat_id, "file_id": main_file_id, "text": caption}
        parse = Parser.parse(caption)

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