#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class Dispatcher:
    async def dispatcher(
        self: "rubigram.Client",
        update: Union["rubigram.types.Update", "rubigram.types.InlineMessage"]
    ):
        """
        **Dispatch incoming updates to appropriate handlers.**
            `await client.dispatcher(update)`

        This method routes incoming updates to the correct handler functions
        based on the update type. It supports both regular updates and
        inline messages, and ensures that only one handler processes each update.

        Args:
            update (`Union[rubigram.types.Update, rubigram.types.InlineMessage]`):
                The incoming update to dispatch to handlers.

        Example:
        .. code-block:: python

            # This method is automatically called by the client
            # when receiving updates from Rubigram

            # Example update flow:
            # 1. New message → message_handlers
            # 2. Edited message → edit_message_handlers  
            # 3. Deleted message → delete_message_handlers
            # 4. Bot start → start_bot_handlers
            # 5. Bot stop → stop_bot_handlers
            # 6. Inline message → inline_message_handlers

        Note:
            - Stops after the first handler that returns True (indicating a match)
            - Each update type has its own dedicated handler list
            - Inline messages are processed separately from regular updates
            - The order of handler registration matters (first match wins)
        """
        if isinstance(update, rubigram.types.InlineMessage):
            handlers = self.inline_message_handlers

        else:
            type = update.type
            if type == "NewMessage":
                handlers = self.new_message_handlers
            elif type == "UpdatedMessage":
                handlers = self.update_message_handlers
            elif type == "RemovedMessage":
                handlers = self.remove_message_handlers
            elif type == "StartedBot":
                handlers = self.started_bot_handlers
            elif type == "StoppedBot":
                handlers = self.stopped_bot_handlers

        for handler in handlers:
            matched = await handler(self, update)
            if matched:
                return