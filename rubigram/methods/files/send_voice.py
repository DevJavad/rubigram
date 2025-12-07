#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
import rubigram


class SendVoice:
    async def send_voice(
        self: "rubigram.Client",
        chat_id: str,
        voice: Union[str, bytes, BinaryIO],
        caption: Optional[str] = None,
        filename: Optional[str] = None,
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None,
        chat_keypad_type: Optional["rubigram.enums.ChatKeypadType"] = None,
        disable_notification: Optional[bool] = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Send a voice message to a chat.**
            `await client.send_voice(chat_id, voice, caption="Voice note")`

        This method sends a voice message to the specified chat. Voice messages
        are displayed with waveform visualization and play button for easy playback.

        Args:
            chat_id (`str`):
                The ID of the chat where the voice message will be sent.

            voice (`Union[str, bytes, BinaryIO]`):
                The voice file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the voice message. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the voice file. Defaults to None.

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
            rubigram.types.UMessage: The sent voice message object.

        Example:
        .. code-block:: python

            # Send a local voice file
            message = await client.send_voice(
                chat_id="g0123456789",
                voice="message.ogg",
                caption="Important announcement",
                disable_notification=False
            )

            # Send voice from bytes with auto-delete
            with open("reminder.ogg", "rb") as f:
                message = await client.send_voice(
                    chat_id="g0123456789",
                    voice=f.read(),
                    filename="daily_reminder.ogg",
                    auto_delete=3600  # Delete after 1 hour
                )

        Note:
            - Voice messages are displayed with waveform visualization
            - Optimized for short audio recordings and voice notes
            - Typically uses compressed audio formats (OGG, OPUS, etc.)
            - Users can play the voice message with a single tap
            - Uses the underlying send_file method with FileType.Voice
        """
        return await self.send_file(
            chat_id,
            voice,
            caption,
            filename,
            "Voice",
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )