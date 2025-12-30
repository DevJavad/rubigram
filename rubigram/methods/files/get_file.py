#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Union
import rubigram


class GetFile:
    
    __slots__ = ()

    async def get_file(
        self: "rubigram.Client",
        file_id: str
    ) -> Union[str, None]:
        """
        Retrieve the download URL of a file by its ID.

        Parameters:
            file_id (str):
                Unique identifier of the file on the Rubika server.

        Returns:
            Union[str, None]:
                The download URL of the file if found, otherwise None.

        Example:
        .. code-block:: python
            url = await client.get_file(file_id="file_id")
        """
        response = await self.request("getFile", {"file_id": file_id})
        return response.get("download_url")