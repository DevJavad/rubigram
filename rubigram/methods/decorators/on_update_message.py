from __future__ import annotations

from typing import Callable, Optional
import rubigram


class OnEditedMessage:
    def on_edited_message(
        self: rubigram.Client,
        filters: Optional[rubigram.filters.Filter] = None,
        group: int = 0
    ):
        def decorator(func: Callable):
            handler = rubigram.Handler(
                callback=func,
                filters=filters
            )

            self.dispatcher.add_handler(
                rubigram.enums.HandlerType.EDITED,
                handler,
                group
            )

            return func

        return decorator