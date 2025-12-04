#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class GetFile:
    async def get_file(
        self: "rubigram.Client",
        file_id: str
    ) -> Union[str, None]:
        """
        **Get download URL for a file.**
            `await client.get_file(file_id)`

        This method retrieves a direct download URL for a file using its
        unique file identifier. The URL can be used to download the file
        directly from Rubigram's servers.

        Args:
            file_id (`str`):
                The unique identifier of the file to download.

        Returns:
            str: The direct download URL for the file.

        Example:
        .. code-block:: python

            # Get download URL for a file
            download_url = await client.get_file(file_id=file_id)
            print(f"Download URL: {download_url}")

        Note:
            - The download URL is temporary and may expire after some time
            - Files are served directly from Rubigram's servers
            - Make sure to handle potential HTTP errors when downloading
        """
        response = await self.request(
            "getFile", {"file_id": file_id}
        )
        return response.get("download_url")