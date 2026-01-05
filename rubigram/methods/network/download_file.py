#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from aiohttp import ClientError, ClientTimeout
import os
import asyncio
import rubigram
from io import BytesIO
from typing import Optional, Union
import aiofiles


class DownloadFile:
    __slots__ = ()

    async def download_file(
        self: "rubigram.Client",
        file_id: str,
        file_name: Optional[str] = None,
        directory: Optional[str] = None,
        chunk_size: int = 64 * 1024,
        in_memory: bool = False,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> Union[str, BytesIO]:
        """
        Download a file from Rubika servers.

        This method downloads files using their file ID obtained from messages.
        Supports downloading to disk or to memory buffer, with configurable
        chunk size and timeout settings.

        Parameters:
            file_id (str):
                The unique file identifier obtained from a message.
                Must be a non-empty string.

            file_name (Optional[str], default: None):
                Custom filename for the downloaded file.
                If not provided, filename will be extracted from the URL.

            directory (Optional[str], default: None):
                Directory path where the file will be saved.
                If provided, the directory will be created if it doesn't exist.

            chunk_size (int, default: 65536):
                Size of chunks to read/write during download (in bytes).
                Default is 64KB (64 * 1024).

            in_memory (bool, default: False):
                If True, returns the file as a BytesIO object in memory.
                If False, saves to disk and returns the file path.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the download request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for the download request.
                Uses client's default proxy if not specified.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            Union[str, BytesIO]:
                - If `in_memory=False`: File path as string
                - If `in_memory=True`: BytesIO object containing the file data

        Raises:
            ValueError:
                If `file_id` is empty or invalid.
            RuntimeError:
                If filename cannot be determined or file cannot be saved.
            TimeoutError:
                If the download times out.
            ConnectionError:
                If there's a network or HTTP error.
            OSError:
                If there's a filesystem error.

        Example:
        .. code-block:: python
            # Download file to current directory
            file_path = await client.download_file(
                file_id="file_1234567890"
            )
            
            # Download to specific directory with custom name
            file_path = await client.download_file(
                file_id="file_1234567890",
                file_name="my_photo.jpg",
                directory="/path/to/downloads",
                chunk_size=32768  # 32KB chunks
            )
            
            # Download to memory
            file_buffer = await client.download_file(
                file_id="file_1234567890",
                in_memory=True
            )
            
            # Use the in-memory buffer
            file_buffer.seek(0)
            data = file_buffer.read()
            
            # Download with custom timeout
            file_path = await client.download_file(
                file_id="file_1234567890",
                timeout=30.0,
                connect_timeout=10.0,
                read_timeout=20.0
            )
            
            print(f"File downloaded to: {file_path}")

        Note:
            - File ID can be obtained from message objects (e.g., `message.file_id`)
            - First gets the download URL using `get_file()` method
            - Automatically extracts filename from URL if not provided
            - Uses aiohttp for efficient asynchronous downloads
            - Supports large files through chunked streaming
            - Creates directories automatically if they don't exist
            - Uses client's HTTP session for connection pooling
            - In-memory mode is useful for processing files without disk I/O
        """
        url = await self.get_file(file_id)
        if url is None:
            raise ValueError("Invalid file_id: %s", file_id)

        name = file_name or await self.get_file_name(url)
        if name is None:
            raise RuntimeError("Could not determine file name")

        proxy = proxy or self.proxy
        kwargs: dict = {
            "headers": headers, "proxy": proxy, "allow_redirects": True
        }
        if timeout:
            kwargs["timeout"] = ClientTimeout(
                timeout, connect_timeout or self.connect_timeout, read_timeout or self.read_timeout
            )

        if directory:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, name)
        else:
            path = name

        try:
            async with self.http.session.get(url, **kwargs) as response:
                response.raise_for_status()

                if in_memory:
                    buf = BytesIO()
                    buf.name = name

                    async for chunk in response.content.iter_chunked(chunk_size):
                        buf.write(chunk)

                    buf.seek(0)
                    return buf

                async with aiofiles.open(path, "wb") as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await f.write(chunk)

                return path

        except asyncio.TimeoutError as error:
            raise TimeoutError(str(error))

        except ClientError as error:
            raise ConnectionError(str(error))

        except OSError as error:
            raise RuntimeError(str(error))