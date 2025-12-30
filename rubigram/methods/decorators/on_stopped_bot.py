from __future__ import annotations

from typing import Callable, Optional
import rubigram


class OnStoppedBot:
    def on_stopped_bot(
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
                rubigram.enums.HandlerType.STOP_BOT,
                handler,
                group
            )

            return func

        return decorator