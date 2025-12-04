#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class RequestSendFile:
    async def request_send_file(
        self: "rubigram.Client",
        type: Union[str, "rubigram.enums.FileType"] = "File"
    ) -> str:
        """
        **Request an upload URL for sending files.**
            `await client.request_send_file(type)`

        This method requests a temporary upload URL from Rubigram's servers
        that can be used to upload files before sending them in messages.

        Args:
            type (`Optional[Union[str, rubigram.enums.FileType]]`):
                The type of file to upload. Defaults to FileType.File.
                Available types:
                - File: Generic file
                - Image: Image file
                - Video: Video file
                - Gif: Animated GIF
                - Music: Audio file
                - Voice: Voice message

        Returns:
            str: The upload URL for file upload.

        Example:
        .. code-block:: python

            # Get upload URL for an image
            upload_url = await client.request_send_file(rubigram.enums.FileType.Image)
            print(f"Upload URL: {upload_url}")

        Note:
            - The upload URL is temporary and should be used immediately
            - Different file types may have different size and format restrictions
            - After uploading, you'll receive a file_id that can be used in send_file methods
        """
        response = await self.request(
            "requestSendFile",
            {"type": type}
        )
        return response["upload_url"]