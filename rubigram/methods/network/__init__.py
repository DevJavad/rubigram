#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .request import Request
from .upload_file import UploadFile
from .get_file_name import GetFileName
from .download_file import DownloadFile


class Network(
    Request,
    UploadFile,
    GetFileName,
    DownloadFile
):
    pass