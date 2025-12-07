#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import asyncio
import rubigram


class DeleteMessage:
    async def delete_messages(
        self: "rubigram.Client",
        chat_id: str,
        message_ids: Union[str, int, list[Union[str, int]]]
    ) -> dict:
        """
        **Delete one or multiple messages from a chat.**
            `await client.delete_message(chat_id, message_id)`

        This method can delete a single message or multiple messages in bulk.
        When deleting multiple messages, it uses asyncio.gather for efficient
        parallel execution.

        Args:
            chat_id (`str`):
                The ID of the chat where the message(s) are located.

            message_ids (`Union[str, int, list[Union[str, int]]]`):
                Single message ID or list of message IDs to delete.

        Returns:
            dict: A dictionary containing deletion results with the following keys:
                - success (int): Number of successfully deleted messages
                - failed (int): Number of messages that failed to delete
                - details (list): List of individual deletion responses

        Example:
        .. code-block:: python

            # Delete a single message
            result = await client.delete_message(
                chat_id=chat_id,
                message_ids=message_id
            )

            # Delete multiple messages
            message_ids = ["12345", "12346", "12347"]
            result = await client.delete_message(
                chat_id=chat_id,
                message_ids=message_ids
            )
            print(f"Success: {result['success']}, Failed: {result['failed']}")

        Note:
            When deleting multiple messages, the operation continues even if
            some deletions fail. Check the 'failed' count and 'details' for
            individual results.
        """
        if isinstance(message_ids, (str, int)):
            return await self.request("deleteMessage", {"chat_id": chat_id, "message_id": str(message_ids)})

        elif isinstance(message_ids, list):
            ids = [str(i) for i in message_ids]

        tasks = [
            self.request(
                "deleteMessage",
                {"chat_id": chat_id, "message_id": id}
            )
            for id in ids
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in responses if not isinstance(r, Exception))
        failed = len(responses) - success

        return {
            "success": success,
            "failed": failed,
            "details": responses
        }