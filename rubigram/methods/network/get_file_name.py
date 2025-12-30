#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from urllib.parse import urlparse
import os
import rubigram


class GetFileName:
    __slots__ = ()

    async def get_file_name(
        self: "rubigram.Client",
        url: str
    ) -> str:
        """
        Extract the base name of a file from its URL.

        Parameters:
            url (str):
                The full URL of the file.

        Returns:
            str: The base name of the file (e.g., "file.jpg").

        Example:
        .. code-block:: python
            name = await client.get_file_name("https://example.com/path/to/file.png")
            print(name)  # Output: "file.png"
        """
        parser = urlparse(url)
        return os.path.basename(parser.path)