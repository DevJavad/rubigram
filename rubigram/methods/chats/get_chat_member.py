#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional
import rubigram


class GetChatMember:
    async def get_chat_member(
        self: rubigram.Client,
        chat_id: str,
        user_id: str,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> rubigram.types.Chat:
        if not chat_id or not user_id:
            raise ValueError("Parameters ('chat_id', 'user_id') is required")

        return await self.request(
            "get_chat_member",
            {"chat_id": chat_id, "user_id": user_id},
            headers,
            proxy,
            retries,
            delay,
            backoff,
            max_delay,
            timeout,
            connect_timeout,
            read_timeout
        )