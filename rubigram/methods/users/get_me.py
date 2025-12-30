#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import rubigram


class GetMe:
    async def get_me(
        self: "rubigram.Client",
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> "rubigram.types.Bot":
        """
        Get current bot information.

        This method retrieves information about the bot associated with the
        current authentication token. Useful for verifying bot identity and
        getting bot details.

        Parameters:
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
            rubigram.types.Bot:
                A Bot object containing information about the current bot.
                Typically includes bot ID, username, name, and other details.

        Example:
        .. code-block:: python
            # Get bot information
            bot_info = await client.get_me()
            
            # Access bot properties
            print(f"Bot ID: {bot_info.bot_id}")
            print(f"Bot username: {bot_info.username}")
            print(f"Bot name: {bot_info.bot_title}")
            print(f"Bot description: {bot_info.description}")
            print(f"Bot avatar: {bot_info.avatar}")
            
            # Use bot info in your application
            welcome_message = f"Hello! I'm {bot_info.bot_title} (@{bot_info.username})"
            
            # Check if bot is active and authenticated
            if bot_info.bot_title:
                print("Bot is successfully authenticated")
            else:
                print("Authentication failed or bot not found")

        Note:
            - Requires valid bot authentication token
            - Useful for verifying that the bot is properly configured
            - Bot information can be used in welcome messages and UI
            - The response is parsed into a Bot object for easy access
            - Can be used to check bot status at application startup
            - Some fields may be None if not set in bot profile
        """
        response = await self.request(
            "getMe",
            None,
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
        return rubigram.types.Bot(response["bot"])