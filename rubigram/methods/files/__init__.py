#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .get_file import GetFile
from .send_gif import SendGif
from .send_file import SendFile
from .send_music import SendMusic
from .send_photo import SendPhoto
from .send_video import SendVideo
from .send_voice import SendVoice
from .send_document import SendDocument
from .request_send_file import RequestSendFile


class Files(
    GetFile,
    SendGif,
    SendFile,
    SendMusic,
    SendPhoto,
    SendVideo,
    SendVoice,
    SendDocument,
    RequestSendFile,
):
    pass