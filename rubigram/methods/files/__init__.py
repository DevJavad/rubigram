#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .get_file import GetFile
from .upload_file import UploadFile
from .get_file_name import GetFileName
from .send_file import SendFile
from .send_gif import SendGif
from .send_music import SendMusic
from .send_photo import SendPhoto
from .send_video import SendVideo
from .send_voice import SendVoice
from .download_file import DownloadFile
from .request_send_file import RequestSendFile


class Files(
    GetFile,
    UploadFile,
    GetFileName,
    RequestSendFile,
    SendFile,
    SendGif,
    SendMusic,
    SendPhoto,
    SendVideo,
    SendVoice,
    DownloadFile
):
    pass