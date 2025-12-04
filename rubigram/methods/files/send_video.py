#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
import rubigram


class SendVideo:
    async def send_video(
        self: "rubigram.Client",
        chat_id: str,
        video: Union[str, bytes, BinaryIO],
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
        **Send a video to a chat.**
            `await client.send_video(chat_id, video, caption="Video description")`

        This method sends a video file to the specified chat. Videos are displayed
        with playback controls and optional caption text.

        Args:
            chat_id (`str`):
                The ID of the chat where the video will be sent.

            video (`Union[str, bytes, BinaryIO]`):
                The video file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the video. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the video. Defaults to None.

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
            rubigram.types.UMessage: The sent video message object.

        Example:
        .. code-block:: python

            # Send a local video file
            message = await client.send_video(
                chat_id="g0123456789",
                video="presentation.mp4",
                caption="Weekly team meeting recording",
                disable_notification=True
            )

            # Send video from bytes with auto-delete
            with open("tutorial.mov", "rb") as f:
                message = await client.send_video(
                    chat_id="g0123456789",
                    video=f.read(),
                    filename="tutorial_video.mov",
                    auto_delete=300  # Delete after 5 minutes
                )

        Note:
            - Videos are displayed with built-in playback controls
            - Supports common video formats (MP4, AVI, MOV, etc.)
            - May show thumbnails and duration information
            - Users can play the video directly in the chat interface
            - Uses the underlying send_file method with FileType.Video
        """
        return await self.send_file(
            chat_id,
            video,
            caption,
            filename,
            "Video",
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )