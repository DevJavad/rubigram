#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiohttp import FormData, ClientError
from aiohttp import FormData, ClientError, payload
from typing import Union, Optional, BinaryIO
from pathlib import Path
from aiohttp import FormData
import asyncio
import rubigram


class UploadFile:
    """
    File uploader for Rubika API.

    This class provides an asynchronous method to upload files to a
    temporary Rubika upload URL. It supports local file paths, remote
    URLs, bytes, and file-like objects, and handles network and timeout
    errors.
    """

    __slots__ = ()

    async def upload_file(
        self: "rubigram.Client",
        upload_url: str,
        file: Union[str, bytes, BinaryIO],
        name: Optional[str] = None,
    ) -> Union[str, None]:
        """
        Upload a file to a temporary Rubika upload URL.

        Parameters:
            upload_url (str):
                The temporary URL obtained from `request_send_file`.
            file (Union[str, bytes, BinaryIO]):
                File path, remote URL, bytes, or file-like object to upload.
            name (Optional[str], default=None):
                Custom name for the uploaded file. If None, the name
                is inferred from the file path or URL, or defaults to "file".

        Returns:
            Union(str, None):
                The file_id returned by Rubika after a successful upload,
                or None if the server response does not contain a file_id.

        Raises:
            TimeoutError:
                If the upload times out.
            ConnectionError:
                If a network error occurs during upload.

        Example:
        .. code-block:: python
            # Upload a local file
            file_id = await client.upload_file(upload_url, "example.jpg")

            # Upload from URL
            file_id = await client.upload_file(upload_url, "https://example.com/file.png")

            # Upload from bytes
            file_id = await client.upload_file(upload_url, b"binary data")
        """
        if isinstance(file, str):
            if file.startswith(("http://", "https://")):
                async with self.http.session.get(file) as response:
                    response.raise_for_status()
                    data = await response.read()
                    if not name:
                        if response.content_type == "application/octet-stream":
                            ext = "ogg"
                        else:
                            ext = f"{str(response.content_type).split("/")[1]}"
                        name = await self.get_file_name(file) or f"rubigram.{ext}"
            else:
                data = Path(file).read_bytes()
                name = name or Path(file).name
        else:
            data = file.read() if hasattr(file, "read") else file
            name = name or "file"

        form = FormData()
        form.add_field(
            "file", payload.BytesPayload(data), filename=name
        )

        try:
            async with self.http.session.post(upload_url, data=form) as response:
                result: dict = await response.json()
                if result.get("status") != "OK":
                    raise rubigram.errors.InvalidInput(result)

                return result.get("data", {}).get("file_id", None)

        except asyncio.TimeoutError as error:
            raise TimeoutError(str(error))

        except ClientError as error:
            raise ConnectionError(str(error))