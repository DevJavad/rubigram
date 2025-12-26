#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from urllib.parse import urlparse
import os
import rubigram


class GetFileName:
    """
    Utility to extract the file name from a URL.

    This class provides a simple asynchronous method to parse a
    given file URL and return its base name. It is intended to be
    used internally by Rubigram for file management operations.
    """
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
