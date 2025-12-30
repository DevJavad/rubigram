from __future__ import annotations

from typing import Callable, Optional
import rubigram


class OnMessage:
    def on_message(
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
                rubigram.enums.HandlerType.MESSAGE,
                handler,
                group
            )

            return func

        return decorator