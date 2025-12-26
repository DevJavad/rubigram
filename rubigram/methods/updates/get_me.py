#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


import rubigram


class GetMe:
    async def get_me(self: "rubigram.Client") -> "rubigram.types.Bot":
        """
        **Get information about the current bot.**
            `await client.get_me()`

        This method retrieves the current bot's information, including
        the bot's ID, username, and other relevant details.

        Returns:
            rubigram.types.Bot: A Bot object containing the bot's information.

        Example:
        .. code-block:: python

            # Get bot information
            bot = await client.get_me()
            print(f"Bot ID: {bot.bot_id}")
            print(f"Bot username: {bot.username}")
            print(f"Bot title : {bot.bot_title }")

        Note:
            This method is useful for verifying that the bot token is valid
            and for accessing the bot's own profile information.
        """
        response = await self.request("getMe", None)
        return rubigram.types.Bot(response["bot"])