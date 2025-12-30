#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
import asyncio
import rubigram


class DeleteMessage:
    async def delete_messages(
        self: rubigram.Client,
        chat_id: str,
        message_id: Union[str, list[str]],
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> dict:
        """
        Delete one or more messages from a chat on Rubika.

        This method allows you to delete messages either individually or in bulk.
        When deleting multiple messages, it uses asynchronous operations for better performance.

        Parameters:
            chat_id (str):
                The chat ID from which messages will be deleted.

            message_id (Union[str, list[str]]):
                The message ID(s) to delete. Can be:
                - Single message ID (str)
                - List of message IDs (list[str])

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
            dict:
                Response dictionary containing:
                - For single message deletion: Direct API response
                - For multiple message deletion: Dictionary with:
                    - "success": Number of successfully deleted messages
                    - "failed": Number of failed deletions
                    - "details": List of individual responses/exceptions

        Example:
        .. code-block:: python
            # Delete a single message
            result = await client.delete_messages(
                chat_id="123456",
                message_id="msg_789"
            )

            # Delete multiple messages
            result = await client.delete_messages(
                chat_id="123456",
                message_id=["msg_789", "msg_790", "msg_791"]
            )

            # Check results for multiple deletions
            if result["failed"] == 0:
                print(f"Successfully deleted {result['success']} messages")
            else:
                print(f"Deleted {result['success']} messages, {result['failed']} failed")
                for detail in result["details"]:
                    if isinstance(detail, Exception):
                        print(f"Error: {detail}")

        Note:
            - Only messages sent by the bot or within the last 48 hours can be deleted
            - In groups/channels, you must have appropriate permissions
            - Bulk deletion uses asyncio.gather for parallel processing
        """
        if isinstance(message_id, str):
            return await self.request("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

        ids = [i for i in message_id]
        tasks = [
            self.request(
                "deleteMessage",
                {"chat_id": chat_id, "message_id": id},
                headers,
                proxy,
                retries,
                delay,
                backoff,
                max_delay,
                timeout,
                connect_timeout,
                read_timeout
            ) for id in ids
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in responses if not isinstance(r, Exception))
        failed = len(responses) - success

        return {
            "success": success,
            "failed": failed,
            "details": responses
        }