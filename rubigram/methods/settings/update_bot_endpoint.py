#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class UpdateBotEndpoints:
    async def update_bot_endpoints(
        self: "rubigram.Client",
        url: str,
        type: Union[str, "rubigram.enums.UpdateEndpointType"] = "ReceiveUpdate"
    ) -> dict:
        """
        **Update webhook endpoints for receiving bot updates.**
            `await client.update_bot_endpoints(url, type)`

        This method sets or updates the webhook URL where Rubigram will send
        bot updates. Different endpoint types can be configured for various
        types of interactions.

        Args:
            url (`str`):
                The webhook URL where updates will be sent.

            type (`Optional[Union[str, rubigram.enums.UpdateEndpointType]]`):
                The type of endpoint to update. Defaults to "ReceiveUpdate".
                Available types:
                - "ReceiveUpdate": General updates
                - "ReceiveInlineMessage": Inline message updates
                - "ReceiveQuery": Callback query updates
                - "GetSelectionItem": Selection item retrieval
                - "SearchSelectionItems": Selection item search

        Returns:
            dict: The API response from Rubigram.

        Example:
        .. code-block:: python

            # Set webhook for general updates
            result = await client.update_bot_endpoints(
                url="https://api.example.com/webhook",
                type="ReceiveUpdate"
            )

            # Set webhook for inline messages
            from rubigram.enums import UpdateEndpointType
            result = await client.update_bot_endpoints(
                url="https://api.example.com/inline",
                type=UpdateEndpointType.ReceiveInlineMessage
            )

        Note:
            - The URL must be HTTPS for security reasons
            - Each endpoint type requires a separate configuration
            - Make sure your webhook server can handle POST requests with JSON payloads
        """
        response = await self.request("updateBotEndpoints", {"url": url, "type": type})
        return response