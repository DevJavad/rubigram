#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class RequestSendFile:
    """
    File upload URL request utility for Rubika API.

    This class provides an asynchronous method to request a temporary
    upload URL from the Rubika server. The URL can then be used to
    upload files of a specified type.
    """
    __slots__ = ()

    async def request_send_file(
        self: "rubigram.Client",
        type: Union[str, "rubigram.enums.FileType"] = "File"
    ) -> str:
        """
        Request a temporary file upload URL from the Rubika server.

        Parameters:
            type (Union[str, rubigram.enums.FileType], default="File"):
                Type of the file to upload. Can be a string or a
                FileType enum member.

        Returns:
            str: Temporary URL for uploading the file.


        Example:
        .. code-block:: python
            # Using enum
            from rubigram.enums import FileType
            upload_url = await client.request_send_file(type=FileType.Image)

            # Using string
            upload_url = await client.request_send_file(type="File")
        """
        type = type.value if isinstance(
            type, rubigram.enums.FileType
        ) else type
        response = await self.request("requestSendFile", {"type": type})
        return response["upload_url"]
