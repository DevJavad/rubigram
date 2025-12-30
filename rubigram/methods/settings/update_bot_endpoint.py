#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union
import rubigram


class UpdateBotEndpoints:
    async def update_bot_endpoints(
        self: "rubigram.Client",
        url: str,
        type: Union[str, "rubigram.enums.UpdateEndpointType"] = rubigram.enums.UpdateEndpointType.RECEIVE_UPDATE,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
    ) -> dict:
        """
        Update bot webhook endpoints for receiving updates.

        This method configures or updates the webhook URL where Rubika will send
        bot updates and events. Supports different types of endpoints for various
        event categories.

        Parameters:
            url (str):
                The webhook URL where updates will be sent.
                Must be a valid HTTPS URL.

            type (Union[str, rubigram.enums.UpdateEndpointType], default: RECEIVE_UPDATE):
                The type of endpoint to update. Can be:
                - String value (e.g., "RECEIVE_UPDATE")
                - UpdateEndpointType enum value
                Defaults to RECEIVE_UPDATE for general bot updates.

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
                The API response from Rubika after updating the bot endpoints.

        Raises:
            ValueError:
                If `url` or `type` parameters are empty or invalid.

        Example:
        .. code-block:: python
            # Update general update endpoint
            result = await client.update_bot_endpoints(
                url="https://example.com/webhook",
                type=rubigram.enums.UpdateEndpointType.RECEIVE_UPDATE
            )
            
            # Update endpoint using string value
            result = await client.update_bot_endpoints(
                url="https://example.com/another-endpoint",
                type="ANOTHER_ENDPOINT_TYPE"
            )
            
            # Update multiple endpoint types
            from rubigram.enums import UpdateEndpointType
            
            endpoints = [
                (UpdateEndpointType.RECEIVE_UPDATE, "https://example.com/updates"),
                (UpdateEndpointType.SOME_OTHER_TYPE, "https://example.com/other"),
            ]
            
            for endpoint_type, endpoint_url in endpoints:
                result = await client.update_bot_endpoints(
                    url=endpoint_url,
                    type=endpoint_type
                )
                print(f"Endpoint {endpoint_type} updated: {result}")

        Note:
            - Webhook URLs must use HTTPS for security
            - Different endpoint types may receive different types of updates
            - The `type` parameter is automatically converted to its value if using enum
            - You may need to handle different update types separately
            - Useful for setting up webhook-based bot architectures
            - Ensure your webhook server can handle incoming POST requests
            - Consider rate limiting and error handling in your webhook implementation
        """
        if not url or not type:
            raise ValueError(
                "Parameters ('url', 'type') must be a non-empty string"
            )
        type.value if hasattr(type, "value") else type
        return await self.request(
            "updateBotEndpoints",
            {"url": url, "type": type},
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