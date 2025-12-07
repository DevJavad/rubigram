#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
import rubigram


class SendMusic:
    async def send_music(
        self: "rubigram.Client",
        chat_id: str,
        music: Union[str, bytes, BinaryIO],
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
        **Send a music/audio file to a chat.**
            `await client.send_music(chat_id, music, caption="Song title")`

        This method sends a music or audio file to the specified chat.
        Music files are displayed with audio player controls and may
        include metadata like artist and title.

        Args:
            chat_id (`str`):
                The ID of the chat where the music will be sent.

            music (`Union[str, bytes, BinaryIO]`):
                The music file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the music file. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the music file. Defaults to None.

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
            rubigram.types.UMessage: The sent music message object.

        Example:
        .. code-block:: python

            # Send a local music file
            message = await client.send_music(
                chat_id="g0123456789",
                music="song.mp3",
                caption="My favorite song - Artist Name",
                disable_notification=True
            )

            # Send music from bytes
            with open("audio.mp3", "rb") as f:
                message = await client.send_music(
                    chat_id="g0123456789",
                    music=f.read(),
                    filename="audio_file.mp3",
                    auto_delete=120  # Delete after 2 minutes
                )

        Note:
            - Music files are displayed with built-in audio player controls
            - Supports common audio formats (MP3, FLAC, WAV, etc.)
            - Users can play the audio directly in the chat interface
            - Uses the underlying send_file method with FileType.Music
        """
        return await self.send_file(
            chat_id,
            music,
            caption,
            filename,
            "Music",
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )