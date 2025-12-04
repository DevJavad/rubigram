#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import rubigram


class SetCommands:
    async def set_commands(
        self: "rubigram.Client",
        commands: list["rubigram.types.BotCommand"]
    ) -> dict:
        """
        **Set bot commands for the Rubigram bot.**
            `await client.set_commands(commands)`

        This method registers a list of bot commands that will be displayed
        in the chat interface and accessible to users through the bot menu.

        Args:
            commands (`list[rubigram.types.BotCommand]`):
                List of BotCommand objects to register for the bot.

        Returns:
            dict: The API response from Rubigram.

        Example:
        .. code-block:: python

            from rubigram.types import BotCommand

            # Define bot commands
            commands = [
                BotCommand(command="start", description="Start the bot"),
                BotCommand(command="help", description="Get help"),
                BotCommand(command="settings", description="Change settings")
            ]

            # Register commands with Rubigram
            result = await client.set_commands(commands)

        Note:
            - Commands will appear in the bot's menu in user chats
            - Each command should have a unique command string
            - Descriptions should be clear and concise for users
        """
        data = {"bot_commands": [command.as_dict() for command in commands]}
        response = await self.request("setCommands", data)
        return response