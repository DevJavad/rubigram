#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union, BinaryIO
import rubigram


class SendGif:
    async def send_gif(
        self: "rubigram.Client",
        chat_id: str,
        gif: Union[str, bytes, BinaryIO],
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
        **Send a GIF animation to a chat.**
            `await client.send_gif(chat_id, gif, caption="Funny animation")`

        This method sends a GIF file to the specified chat. GIFs are displayed
        as auto-playing animations in the chat interface.

        Args:
            chat_id (`str`):
                The ID of the chat where the GIF will be sent.

            gif (`Union[str, bytes, BinaryIO]`):
                The GIF file to send. Can be:
                - Local file path
                - Bytes data
                - Binary file-like object

            caption (`Optional[str]`):
                Caption text for the GIF. Defaults to None.

            filename (`Optional[str]`):
                Custom filename for the GIF. Defaults to None.

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
            rubigram.types.UMessage: The sent GIF message object.

        Example:
        .. code-block:: python

            # Send a local GIF file
            message = await client.send_gif(
                chat_id="g0123456789",
                gif="animation.gif",
                caption="Check out this cool animation!",
                disable_notification=True
            )

            # Send GIF from bytes with auto-delete
            with open("reaction.gif", "rb") as f:
                message = await client.send_gif(
                    chat_id="g0123456789",
                    gif=f.read(),
                    filename="reaction.gif",
                    auto_delete=30  # Delete after 30 seconds
                )

        Note:
            - GIFs auto-play in loops without sound
            - Optimized for short animations and reactions
            - Uses the underlying send_file method with FileType.Gif
        """
        return await self.send_file(
            chat_id,
            gif,
            caption,
            filename,
            "Gif",
            chat_keypad,
            inline_keypad,
            chat_keypad_type,
            disable_notification,
            reply_to_message_id,
            auto_delete
        )