#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from urllib.parse import urlparse
import os
import rubigram


class GetFileName:
    async def get_file_name(
        self: "rubigram.Client",
        url: str
    ) -> str:
        """
        **Extract file name from a URL.**
            `await client.get_file_name(url)`

        This method extracts the file name from a given URL by parsing
        the path component and returning the base name. Useful for
        determining the original file name when downloading files.

        Args:
            url (`str`):
                The URL to extract the file name from.

        Returns:
            str: The extracted file name, or empty string if no file name is found.

        Example:
        .. code-block:: python

            # Extract file name from a URL
            url = "https://example.com/files/document.pdf"
            file_name = await client.get_file_name(url)
            print(f"File name: {file_name}")  # Output: "document.pdf"

            # With query parameters
            url = "https://botapi.rubika.ir/files/image.jpg?token=abc123"
            file_name = await client.get_file_name(url)
            print(f"File name: {file_name}")  # Output: "image.jpg"

            # With complex path
            url = "https://cdn.example.com/path/to/photo.png"
            file_name = await client.get_file_name(url)
            print(f"File name: {file_name}")  # Output: "photo.png"

        Note:
            - Only extracts the base name from the path, ignores query parameters and fragments
            - Returns empty string if the URL path ends with a slash
            - Useful for preserving original file names when downloading files
        """
        parser = urlparse(url)
        return os.path.basename(parser.path)