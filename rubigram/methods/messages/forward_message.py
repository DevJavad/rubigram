#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
from rubigram.utils import AutoDelete
import rubigram


class ForwardMessage:
    async def forward_message(
        self: "rubigram.Client",
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Forward a message from one chat to another.**
            `await client.forward_message(from_chat_id, message_id, to_chat_id)`

        This method forwards an existing message from a source chat to a
        destination chat while preserving all message content, attachments,
        and metadata.

        Args:
            from_chat_id (`str`):
                The ID of the chat where the original message is located.

            message_id (`str`):
                The ID of the message to forward.

            to_chat_id (`str`):
                The ID of the destination chat where the message will be forwarded.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the forwarded message.
                Defaults to False.
                
            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The forwarded message object with client binding.

        Example:
        .. code-block:: python

            # Forward a message from one chat to another
            forwarded_message = await client.forward_message(
                from_chat_id=from_chat_id,
                message_id=message_id,
                to_chat_id=to_chat_id,
                disable_notification=True
            )

        Note:
            The original message remains unchanged in the source chat.
            The forwarded message includes all original content and attachments.
        """
        response = await self.request(
            "forwardMessage",
            {
                "from_chat_id": from_chat_id,
                "message_id": message_id,
                "to_chat_id": to_chat_id,
                "disable_notification": disable_notification
            }
        )
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = to_chat_id
        
        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)
            
        return message