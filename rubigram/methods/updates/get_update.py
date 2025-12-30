#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import rubigram


class GetUpdates:
    async def get_updates(
        self: "rubigram.Client",
        limit: Optional[int] = 1,
        offset_id: Optional[str] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> "rubigram.types.Updates":
        """
        Get updates from Rubika using long polling.

        This method retrieves incoming updates (messages, events, etc.) from Rubika.
        It uses long polling technique and supports pagination through offset IDs.

        Parameters:
            limit (Optional[int], default: 1):
                Maximum number of updates to return per request.
                Default is 1 update per call.

            offset_id (Optional[str], default: None):
                Identifier of the first update to be returned.
                Use to get updates starting from a specific point.
                If None, returns the latest updates.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for requests.

            retries (Optional[int], default: None):
                Number of retry attempts on request failure.

            delay (Optional[float], default: None):
                Initial delay between retries in seconds.

            backoff (Optional[float], default: None):
                Backoff multiplier applied after each retry.

            max_delay (Optional[float], default: None):
                Maximum delay between retries.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            rubigram.types.Updates:
                An Updates object containing the retrieved updates.
                Can be iterated over to process individual updates.

        Example:
        .. code-block:: python
            # Get latest update
            updates = await client.get_updates()
            
            # Process updates
            for update in updates:
                print(f"Update type: {update.type}")
                print(f"Update time: {update.updated_time}")
            
            # Get multiple updates with higher limit
            updates = await client.get_updates(limit=10)
            
            # Get updates from specific offset (for pagination)
            last_offset_id= "update_123456"
            updates = await client.get_updates(
                limit=5,
                offset_id=last_offset_id
            )
            
            # Continuous polling loop
            last_offset_id = None
            while True:
                updates = await client.get_updates(
                    limit=10,
                    offset_id=last_offset_id
                )
                
                for update in updates:
                    # Process update
                    print(f"New update: {update}")
                    last_offset_id = update.next_offset_id
                
                # Small delay to prevent busy waiting
                import asyncio
                await asyncio.sleep(0.1)

        Note:
            - Uses long polling: request waits until updates are available
            - `offset_id` is useful for implementing update polling loops
            - Higher limits may increase response time
            - Updates are automatically parsed into appropriate types
            - Consider using webhooks (`update_bot_endpoints`) for production
            - For continuous polling, store the last processed update_id
            - Updates include messages, callbacks, and other bot events
        """
        response = await self.request(
            "getUpdates",
            {"limit": limit, "offset_id": offset_id},
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
        return rubigram.types.Updates.parse(response)