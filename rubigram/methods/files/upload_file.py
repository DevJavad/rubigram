#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union, Optional, BinaryIO
from pathlib import Path
from aiohttp import FormData
import rubigram


class UploadFile:
    async def upload_file(
        self: "rubigram.Client",
        upload_url: str,
        file: Union[str, bytes, BinaryIO],
        name: Optional[str] = None
    ) -> str:
        """
        **Upload a file to Rubigram's servers.**
            `await client.upload_file(upload_url, file, name)`

        This method uploads a file to Rubigram's servers using the provided
        upload URL. The file can be a local file path, a URL, or raw bytes.

        Args:
            upload_url (`str`):
                The upload URL obtained from `request_send_file`.

            file (`Union[str, bytes, BinaryIO]`):
                The file to upload. Can be:
                - Local file path
                - URL to download file from
                - Raw bytes data

            name (`Optional[str]`):
                The file name to use for the upload. Required when file is bytes.

        Returns:
            str: The file_id assigned by Rubigram for the uploaded file.

        Example:
        .. code-block:: python

            # Upload a local file
            upload_url = await client.request_send_file("Image")
            file_id = await client.upload_file(upload_url, "photo.jpg")
            print(f"Uploaded file ID: {file_id}")

        Raises:
            FileNotFoundError: If local file path doesn't exist
            ValueError: If name is not provided for bytes data
            TypeError: If file type is not supported
            aiohttp.ClientError: If upload fails

        Note:
            - The upload URL must be obtained first using `request_send_file`
            - File name is automatically extracted for local files and URLs
            - Returns a file_id that can be used in subsequent API calls
        """
        if isinstance(file, str):
            path = Path(file)

            if path.is_file():
                file = path.read_bytes()
                name = name or path.name

            elif file.startswith("http"):
                async with self.http.session.get(file) as response:
                    response.raise_for_status()
                    file = await response.read()
                    name = name or await self.get_file_name(file)
            else:
                raise FileNotFoundError("Invalid path or url file: %s", file)

        else:
            name = name or "file"

        form = FormData()
        form.add_field(
            "file", file, filename=name, content_type="application/octet-stream"
        )

        async with self.http.session.post(upload_url, data=form) as response:
            response.raise_for_status()
            data: dict = await response.json()
            return data.get("data", {}).get("file_id")