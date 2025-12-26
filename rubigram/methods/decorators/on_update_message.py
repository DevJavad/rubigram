#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnUpdateMessage:
    def on_update_message(
        self: "rubigram.Client",
        filters: Optional["Filter"] = None
    ):
        """
        **Decorator for handling edited messages.**
            `@client.on_edit_message(filters.text)`

        This decorator registers a function to handle message edit events
        that match the specified filters. If no filters are provided,
        all message edits will be handled.

        Args:
            filters (`Optional[Filter]`):
                Filter to determine which message edits should be handled.
                If None, all message edits will be processed.

        Returns:
            Callable: The decorator function.

        Example:
        .. code-block:: python

            # Handle text message edits
            @client.on_edit_message(filters.text)
            async def handle_text_edit(client, update):
                old_text = update.updated_message.text
                await client.send_message(
                    update.chat_id, 
                    f"Message was edited to: {old_text}"
                )

            # Handle edits in specific chats only
            @client.on_edit_message(filters.chat("g0123456789"))
            async def handle_group_edits(client, update):
                print(f"Message edited in group: {update.updated_message.text}")

            # Handle all message edits (no filter)
            @client.on_edit_message()
            async def handle_all_edits(client, update):
                print(f"Message {update.updated_message.message_id} was edited")

        Note:
            This handler only triggers for messages that have been edited,
            not for new messages. The edited message is available in `update.updated_message`.
        """
        def decorator(func: Callable) -> Callable:
            async def wrapper(
                client: "rubigram.Client",
                update: "rubigram.types.Update"
            ):
                if filters is None or await filters(client, update):
                    await func(client, update)
                    return True
                return False

            self.update_message_handlers.append(wrapper)
            return func
        return decorator