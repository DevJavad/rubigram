#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations
import os
import asyncio
import rubigram
from io import BytesIO
from aiohttp import ClientError
from typing import Optional, Union


class DownloadFile:
    """
    File download manager for Rubika API.

    This class provides an asynchronous method to download files from
    the Rubika server by file ID, supporting saving to disk or loading
    directly into memory. It handles HTTP errors, timeouts, and
    filesystem exceptions.
    """
    __slots__ = ()

    async def download_file(
        self: "rubigram.Client",
        file_id: str,
        file_name: Optional[str] = None,
        directory: Optional[str] = None,
        chunk_size: int = 64 * 1024,
        in_memory: bool = False,
    ) -> Union[str, BytesIO]:
        """
        Download a file from Rubika by file ID.

        Parameters:
            file_id (str):
                Unique identifier of the file to download.
            file_name (Optional[str], default=None):
                Custom name for the downloaded file. If not provided,
                the name is inferred from the file URL.
            directory (Optional[str], default=None):
                Directory path to save the file. If None, saves to
                the current working directory.
            chunk_size (int, default=64*1024):
                Size (in bytes) of each chunk to read during download.
            in_memory (bool, default=False):
                If True, the file will be loaded into a BytesIO buffer
                instead of being written to disk.

        Returns:
            Union[str, BytesIO]:
                Path to the saved file on disk, or a BytesIO buffer
                if in_memory is True.

        Raises:
            ValueError:
                If the file_id is invalid or the URL cannot be obtained.
            RuntimeError:
                If file name cannot be determined or a filesystem error occurs.
            TimeoutError:
                If the download times out.
            ConnectionError:
                If a network error occurs during download.

        Example:
        .. code-block:: python
            # Save file to disk
            path = await client.download_file(file_id="file_id", directory="downloads")

            # Load file into memory
            buffer = await client.download_file(file_id="file_id", in_memory=True)
        """
        url = await self.get_file(file_id)
        if url is None:
            raise ValueError(f"Invalid file_id: {file_id}")

        name = file_name or await self.get_file_name(url)
        if name is None:
            raise RuntimeError("Could not determine file name")

        if directory:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, name)
        else:
            path = name

        try:
            async with self.http.session.get(url) as resp:
                resp.raise_for_status()

                if in_memory:
                    buf = BytesIO()
                    buf.name = name

                    async for chunk in resp.content.iter_chunked(chunk_size):
                        buf.write(chunk)

                    buf.seek(0)
                    return buf

                file_descriptor = os.open(
                    path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644
                )
                try:
                    async for chunk in resp.content.iter_chunked(chunk_size):
                        view = memoryview(chunk)
                        while view:
                            written = os.write(file_descriptor, view)
                            view = view[written:]
                finally:
                    os.close(file_descriptor)

                return path

        except asyncio.TimeoutError as error:
            raise TimeoutError(str(error))

        except ClientError as error:
            raise ConnectionError(str(error))

        except OSError as error:
            raise RuntimeError(str(error))