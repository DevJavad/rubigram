#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Callable
from rubigram.filters import Filter
import rubigram


class OnInlineMessage:
    def on_inline_message(
        self: rubigram.Client,
        filters: Optional[Filter] = None,
        group: int = 0
    ):
        def decorator(func: Callable):
            handler = rubigram.Handler(
                callback=func,
                filters=filters
            )

            self.dispatcher.add_handler(
                rubigram.enums.HandlerType.INLINE,
                handler,
                group
            )

            return func

        return decorator