#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import rubigram
import logging


logger = logging.getLogger(__name__)


class SetupEndpoints:
    async def setup_endpoints(self: "rubigram.Client"):
        """
        **Set up webhook endpoints for all update types.**
            `await client.setup_endpoints()`

        This method automatically configures webhook endpoints for all
        available update types in Rubigram. Each endpoint type will be
        registered with the base webhook URL followed by the endpoint type.

        Example:
        .. code-block:: python

            # Set up all webhook endpoints
            await client.setup_endpoints()

            # Example of configured endpoints:
            # - https://api.example.com/webhook/ReceiveUpdate
            # - https://api.example.com/webhook/ReceiveInlineMessage  
            # - https://api.example.com/webhook/ReceiveQuery
            # - https://api.example.com/webhook/GetSelectionItem
            # - https://api.example.com/webhook/SearchSelectionItems

        Note:
            - Requires `webhook_url` to be set in the client instance
            - Configures endpoints for all UpdateEndpointType enum values
            - Logs the status of each endpoint setup operation
            - Each endpoint type gets its own unique URL path
        """
        for i in rubigram.enums.UpdateEndpointType:
            type = i.value
            url = f"{self.webhook}/{type}"
            set_endpoint = await self.update_bot_endpoints(url, type)
            logger.info(
                "ENDPOINT SET(type=%s, status=%s)", type, set_endpoint["status"]
            )