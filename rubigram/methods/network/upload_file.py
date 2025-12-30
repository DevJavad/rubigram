#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiohttp import FormData, ClientError, payload, ClientTimeout
from typing import Union, Optional, BinaryIO
from pathlib import Path
import asyncio
import rubigram
import logging


logger = logging.getLogger(__name__)


class UploadFile:

    __slots__ = ()

    async def upload_file(
        self: "rubigram.Client",
        upload_url: str,
        file: Union[str, bytes, BinaryIO],
        name: Optional[str] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> Union[str, None]:
        """
        Upload a file to Rubika servers.

        This method handles file uploads to Rubika's file storage system.
        Supports uploading from local files, URLs, bytes, or BinaryIO objects.
        Returns the uploaded file's unique identifier for later use.

        Parameters:
            upload_url (str):
                The upload endpoint URL provided by Rubika API.
                Must be a valid upload URL.

            file (Union[str, bytes, BinaryIO]):
                The file to upload. Can be:
                - Local file path (str)
                - HTTP/HTTPS URL (str) - will be downloaded first
                - Bytes object
                - BinaryIO stream

            name (Optional[str], default: None):
                Custom filename for the uploaded file.
                If not provided, filename will be extracted from source.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the upload request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for the upload request.
                Uses client's default proxy if not specified.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            Union[str, None]:
                The uploaded file's unique identifier (file_id) if successful,
                None if upload failed.

        Raises:
            ValueError:
                If `upload_url` is empty or invalid.
            TimeoutError:
                If the upload times out.
            ConnectionError:
                If there's a network or HTTP error.
            rubigram.errors.RubigramError:
                If Rubika API returns an error response.

        Example:
        .. code-block:: python
            # Upload local file
            file_id = await client.upload_file(
                upload_url="https://upload.rubika.ir/...",
                file="/path/to/file.jpg"
            )
            
            # Upload file from URL with custom name
            file_id = await client.upload_file(
                upload_url="https://upload.rubika.ir/...",
                file="https://example.com/image.png",
                name="custom_name.png"
            )
            
            # Upload bytes data
            with open("file.txt", "rb") as f:
                file_bytes = f.read()
            file_id = await client.upload_file(
                upload_url="https://upload.rubika.ir/...",
                file=file_bytes,
                name="document.txt"
            )
            
            # Upload BinaryIO stream
            from io import BytesIO
            buffer = BytesIO(b"file content")
            buffer.name = "myfile.txt"
            file_id = await client.upload_file(
                upload_url="https://upload.rubika.ir/...",
                file=buffer
            )
            
            # Upload with custom timeout
            file_id = await client.upload_file(
                upload_url="https://upload.rubika.ir/...",
                file="/path/to/large_file.mp4",
                timeout=120.0,
                read_timeout=60.0
            )
            
            if file_id:
                print(f"File uploaded successfully with ID: {file_id}")

        Note:
            - Upload URL must be obtained from Rubika API first
            - For HTTP URLs, file is downloaded then uploaded to Rubika
            - Automatically determines content type and extension
            - Uses multipart form data for file upload
            - Returns file_id which can be used in `send_file()` and other methods
            - Handles different file sources transparently
            - Logs upload process using the module logger
            - File size limits depend on Rubika's API restrictions
        """
        if not upload_url:
            raise ValueError("upload_url is required")

        proxy = proxy or self.proxy

        kwargs: dict = {"headers": headers, "proxy": proxy}
        if timeout:
            kwargs["timeout"] = ClientTimeout(
                timeout, connect_timeout or self.connect_timeout, read_timeout or self.read_timeout
            )

        if isinstance(file, str):
            if file.startswith(("http://", "https://")):
                async with self.http.session.get(file, **kwargs) as response:
                    response.raise_for_status()
                    data, name = await response.read(), await self.get_file_name(file)
                    if not name:
                        ext = "ogg" if response.content_type == "application/octet-stream" else str(
                            response.content_type).split("/")[1]
                        name = "rubigram.%s" % ext
            else:
                data = Path(file).read_bytes()
                name = name or Path(file).name
        else:
            data = file.read() if hasattr(file, "read") else file
            name = file.name if hasattr(file, "name") else "file.bin"

        form = FormData()
        form.add_field(
            "file", payload.BytesPayload(data), filename=name
        )

        try:
            async with self.http.session.post(upload_url, data=form) as response:
                result: dict = await response.json()
                if result.get("status") == "OK":
                    return result.get("data", {}).get("file_id")

                rubigram.errors.raise_rubigram_error(data)

        except asyncio.TimeoutError as error:
            raise TimeoutError(str(error))

        except ClientError as error:
            raise ConnectionError(str(error))