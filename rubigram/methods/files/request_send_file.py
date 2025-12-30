#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class RequestSendFile:

    __slots__ = ()

    async def request_send_file(
        self: "rubigram.Client",
        type: Union[str, "rubigram.enums.FileType"] = rubigram.enums.FileType.FILE
    ) -> str:
        """
        Request an upload URL from the Rubika server for sending a file.

        This method interacts with the Rubika API to obtain a temporary URL
        where a file can be uploaded. The URL is specific to the file type
        and is required before calling `send_file`.

        Parameters:
            type (Union[str, rubigram.enums.FileType], default=FileType.FILE):
                The type of file to upload (e.g., FILE, VOICE, DOCUMENT). Can
                be provided as a string or `FileType` enum.

        Returns:
            str: A temporary upload URL provided by the Rubika server.

        Example:
        .. code-block:: python
            upload_url = await client.request_send_file(type=rubigram.enums.FileType.FILE)
        """
        type = type if isinstance(type, str) else type.value
        response = await self.request("requestSendFile", {"type": type})
        return response["upload_url"]