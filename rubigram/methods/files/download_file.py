#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional
import aiofiles
import os
import rubigram


class DownloadFile:
    async def download_file(
        self: "rubigram.Client",
        file_id: str,
        name: Optional[str] = None,
        directory: Optional[str] = None,
        chunk_size: int = 1024
    ) -> str:
        """
        **Download a file from Rubigram's servers.**
            `await client.download_file(file_id, save_as="downloaded_file.jpg")`

        This method downloads a file from Rubigram's servers using its file ID
        and saves it to the local filesystem. The download is streamed efficiently
        to handle large files.

        Args:
            file_id (`str`):
                The unique identifier of the file to download.

            save_as (`Optional[str]`):
                The local file path to save the downloaded file.
                If not provided, the original file name is used.

        Returns:
            str: The path to the downloaded file.

        Example:
        .. code-block:: python

            # Download a file with custom name
            file_path = await client.download_file(
                file_id="FILE_123456789",
                save_as="my_document.pdf"
            )
            print(f"File downloaded to: {file_path}")

            # Download using original file name
            file_path = await client.download_file("FILE_987654321")
            print(f"File saved as: {file_path}")

            # Download and process the file
            file_path = await client.download_file("FILE_555555555", "image.png")
            # Now you can process the downloaded file...

        Note:
            - Files are downloaded in 1KB chunks to handle large files efficiently
            - Uses streaming download to minimize memory usage
            - Automatically extracts the original file name if save_as is not provided
            - Returns the full path to the downloaded file
        """
        download_url = await self.get_file(file_id)

        if not download_url:
            raise ValueError("Invalid download url: %s", file_id)

        filename = name or await self.get_file_name(download_url)

        if not directory is None:
            os.makedirs(directory, exist_ok=True)
            filename = os.path.join(directory, filename)

        async with self.http.session.get(download_url) as response:
            response.raise_for_status()

            async with aiofiles.open(filename, "wb") as file:
                async for chunk in response.content.iter_chunked(chunk_size):
                    await file.write(chunk)

        return filename