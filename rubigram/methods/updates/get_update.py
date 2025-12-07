#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import rubigram


class GetUpdates:
    async def get_updates(
        self: "rubigram.Client",
        limit: Optional[int] = 1,
        offset_id: Optional[str] = None
    ) -> "rubigram.types.Updates":
        """
        **Retrieve incoming updates from Rubigram.**
            `await client.get_updates(limit=10, offset_id="12345")`

        This method fetches updates (new messages, edits, deletions, etc.)
        from the Rubigram server. It supports pagination through the offset_id
        parameter for efficient update retrieval.

        Args:
            limit (`Optional[int]`):
                Maximum number of updates to retrieve. Defaults to 1.

            offset_id (`Optional[str]`):
                ID of the last received update. Updates with higher IDs
                will be returned. Defaults to None.

        Returns:
            rubigram.types.Updates: A collection of update objects with next_offset_id.

        Example:
        .. code-block:: python

            # Get the latest 10 updates
            updates = await client.get_updates(limit=10)
            for update in updates.updates:
                print(f"New update type: {update.type}")

            # Get updates after a specific ID
            updates = await client.get_updates(
                limit=5,
                offset_id="12345"
            )
            print(f"Next offset: {updates.next_offset_id}")

        Note:
            - Use the returned next_offset_id for subsequent calls to avoid missing updates
            - Updates are automatically marked as received by the server
            - Consider using a reasonable limit to avoid overwhelming the client
        """
        response = await self.request(
            "getUpdates",
            {
                "limit": limit,
                "offset_id": offset_id
            }
        )
        return rubigram.types.Updates.parse(response)