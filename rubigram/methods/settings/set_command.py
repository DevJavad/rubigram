#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import rubigram


class SetCommands:
    async def set_commands(
        self: "rubigram.Client",
        commands: list["rubigram.types.BotCommand"],
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
        Set bot commands for the current bot.

        This method registers or updates the list of commands that users can see
        and use when interacting with your bot through the Rubika interface.

        Parameters:
            commands (list[rubigram.types.BotCommand]):
                List of bot command objects to register.
                Each command should have a command name and description.

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
                The API response from Rubika after setting the commands.

        Example:
        .. code-block:: python
            from rubigram import types
            
            # Define bot commands
            commands = [
                types.BotCommand(
                    command="/start",
                    description="Start the bot and see welcome message"
                ),
                types.BotCommand(
                    command="/help",
                    description="Get help and instructions"
                ),
                types.BotCommand(
                    command="/settings",
                    description="Configure bot settings"
                ),
                types.BotCommand(
                    command="/profile",
                    description="View your profile"
                )
            ]
            
            # Set the commands
            result = await client.set_commands(commands)
            
            print(f"Commands set successfully: {result}")

        Note:
            - Commands are typically shown in the chat input area when typing "/"
            - Each command should start with "/" (e.g., "/start")
            - Descriptions should be clear and concise (usually 1-3 words)
            - Commands are automatically serialized using `as_dict()` method
            - You can update commands at any time by calling this method again
            - Maximum number of commands may be limited by Rubika
            - Useful for making your bot more discoverable and user-friendly
        """
        data = {"bot_commands": [command.as_dict() for command in commands]}
        response = await self.request(
            "setCommands",
            data,
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
        return response