#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
import rubigram


class SendPhoto:
    async def send_photo(
        self: "rubigram.Client",
        chat_id: str,
        photo: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None,
        chat_keypad_type: Optional["rubigram.enums.ChatKeypadType"] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Send a photo to a chat.**
            `await client.send_photo(chat_id, photo, caption="Photo description")`

        This method sends a photo to the specified chat. Photos are displayed
        as previewable images with optional caption text.

        Args:
            chat_id (`str`):
                The ID of the chat where the photo will be sent.

            photo (`Union[str, bytes, BinaryIO]`):
                The photo file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the photo. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the photo. Defaults to None.

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
            rubigram.types.UMessage: The sent photo message object.

        Example:
        .. code-block:: python

            # Send a local photo
            message = await client.send_photo(
                chat_id="g0123456789",
                photo="landscape.jpg",
                caption="Beautiful landscape from my trip",
                disable_notification=False
            )

            # Send photo from bytes with auto-delete
            with open("profile.png", "rb") as f:
                message = await client.send_photo(
                    chat_id="g0123456789",
                    photo=f.read(),
                    filename="profile_picture.png",
                    auto_delete=60  # Delete after 1 minute
                )

        Note:
            - Photos are displayed as previewable images in the chat
            - Supports common image formats (JPEG, PNG, WEBP, etc.)
            - Users can tap to view the full-size image
            - Uses the underlying send_file method with FileType.Image
        """
        return await self.send_file(
            chat_id,
            photo,
            caption,
            filename,
            "Image",
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )