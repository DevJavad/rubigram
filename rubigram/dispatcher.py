#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, List, Union
import rubigram


class Dispatcher:
    def __init__(self, client: rubigram.Client):
        self.client = client

        self.handlers: DefaultDict[
            rubigram.enums.HandlerType,
            DefaultDict[int, List[rubigram.Handler]]
        ] = defaultdict(lambda: defaultdict(list))

    def add_handler(
        self,
        type: rubigram.enums.HandlerType,
        handler: rubigram.Handler,
        group: int = 0
    ):
        """
        Add a handler for a specific event type.

        Parameters:
            type (rubigram.enums.HandlerType):
                The type of event to handle (e.g., MESSAGE, EDITED, DELETED).

            handler (rubigram.Handler):
                The handler object to register.

            group (int, default: 0):
                Priority group for the handler. Lower numbers execute first.

        Example:
            dp.add_handler(
                HandlerType.MESSAGE,
                MessageHandler(my_message_callback),
                group=0
            )
        """
        self.handlers[type][group].append(handler)

    def remove_handler(
        self,
        type: rubigram.enums.HandlerType,
        handler: rubigram.Handler,
        group: int = 0
    ):
        """
        Remove a previously registered handler.

        Parameters:
            type (rubigram.enums.HandlerType):
                The event type the handler was registered for.

            handler (rubigram.Handler):
                The handler object to remove.

            group (int, default: 0):
                The group the handler was registered in.

        Note:
            If the handler is not found in the specified group, no error is raised.
        """
        if type in self.handlers and group in self.handlers[type]:
            handlers = self.handlers[type][group]
            if handler in handlers:
                handlers.remove(handler)

    async def dispatch(
        self,
        update: Union[
            rubigram.types.Update,
            rubigram.types.InlineMessage
        ]
    ):
        """
        Dispatch an update to appropriate handlers.

        This method routes incoming updates to registered handlers based on
        the update type. Handlers are executed in group priority order.

        Parameters:
            update (Union[rubigram.types.Update, rubigram.types.InlineMessage]):
                The update object to process.

        Update Type Mapping:
            - "NewMessage" → HandlerType.MESSAGE
            - "UpdatedMessage" → HandlerType.EDITED
            - "RemovedMessage" → HandlerType.DELETED
            - "StartedBot" → HandlerType.START_BOT
            - "StoppedBot" → HandlerType.STOP_BOT
            - rubigram.types.InlineMessage → HandlerType.INLINE

        Handler Execution Flow:
            1. Determine event type from update
            2. Get handlers for that event type
            3. Execute handlers in group order (lowest first)
            4. Within each group, execute handlers in registration order
            5. Stop processing group if rubigram.StopPropagation is raised
            6. Continue to next handler if rubigram.ContinuePropagation is raised

        Note:
            - Each handler's `check()` method is called first to verify if it should run
            - If `check()` returns True, the handler's `run()` method is executed
            - Handlers can raise StopPropagation to prevent further processing
            - Handlers can raise ContinuePropagation to skip to the next handler
        """

        if isinstance(update, rubigram.types.InlineMessage):
            event_type = rubigram.enums.HandlerType.INLINE
        else:
            if update.type == "NewMessage":
                event_type = rubigram.enums.HandlerType.MESSAGE

            elif update.type == "UpdatedMessage":
                event_type = rubigram.enums.HandlerType.EDITED

            elif update.type == "RemovedMessage":
                event_type = rubigram.enums.HandlerType.DELETED

            elif update.type == "StartedBot":
                event_type = rubigram.enums.HandlerType.START_BOT

            elif update.type == "StoppedBot":
                event_type = rubigram.enums.HandlerType.STOP_BOT

        groups = self.handlers.get(event_type)
        if not groups:
            return

        for group in sorted(groups):
            for handler in groups[group]:
                try:
                    if await handler.check(self.client, update):
                        await handler.run(self.client, update)
                except rubigram.StopPropagation:
                    break
                except rubigram.ContinuePropagation:
                    continue