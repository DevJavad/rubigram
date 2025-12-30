#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Any
from aiohttp import FormData
from ..http_session import HttpSession
from urllib.parse import urlparse
from random import randint
from pathlib import Path
from json import loads
import os


class Network:
    def __init__(
        self,
        auth: str,
        timeout: float = 30.0,
        connect_timeout: float = 10.0,
        read_timeout: float = 20.0,
        max_connections: int = 100
    ):
        self.auth = auth
        self.http = HttpSession(timeout, connect_timeout, read_timeout, max_connections)
        self.api = f"https://rubino{randint(1, 30)}.iranlms.ir"
        self.client = {
            "app_name": "Main",
            "app_version": "3.0.2",
            "lang_code": "fa",
            "package": "app.rbmain.a",
            "platform": "Android"
        }

    async def start(self):
        await self.http.connect()

    async def stop(self):
        await self.http.disconnect()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.stop()

    async def request(self, method: str, data: dict[str, Any]):
        json = {
            "api_version": "0",
            "auth": self.auth,
            "client": self.client,
            "data": data,
            "method": method
        }
        async with self.http.session.post(self.api, json=json) as response:
            response.raise_for_status()
            return await response.json()

    async def get_bytes(self, url: str) -> bytes:
        async with self.http.session.get(url) as response:
            response.raise_for_status()
            return await response.read()

    async def get_name(self, url: str) -> str:
        parser = urlparse(url)
        return os.path.basename(parser.path)

    async def request_upload_file(
        self,
        file_name: str,
        file_size: str,
        file_type: str,
        profile_id: str,
    ):
        data = {
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type,
            "profile_id": profile_id,
        }
        return await self.request("requestUploadFile", data)

    async def request_upload(
        self,
        file: str,
        file_type: str,
        file_name: Optional[str] = None,
        profile_id: Optional[str] = None,
    ):
        path = Path(file)
        if path.is_file():
            data = path.read_bytes()
            file_name = file_name if file_name else path.name
            file_size = path.stat().st_size

        elif file.startswith("http"):
            data = await self.get_bytes(file)
            file_name = file_name if file_name else await self.get_name(file)
            file_size = len(data)

        else:
            raise Exception(f"Can't find this file : {file}")

        request = await self.request_upload_file(file_name, file_size, file_type, profile_id)
        request: dict[str, str] = request["data"]

        file_id: str = request["file_id"]
        hash_file_request: str = request["hash_file_request"]
        server_url: str = request["server_url"]

        headers = {
            "auth": self.auth,
            "chunk-size": str(file_size),
            "file-id": file_id,
            "hash-file-request": hash_file_request,
            "content-length": str(file_size),
            "part-number": "1",
            "total-part": "1"
        }
        form = FormData()
        form.add_field(
            "file", data, filename=file_name, content_type="application/octet-stream"
        )
        async with self.http.session.post(server_url, data=form, headers=headers) as response:
            text = await response.text()
            hash_file_receive = loads(text)["data"]["hash_file_receive"]
            return {"file_id": file_id, "hash_file_receive": hash_file_receive}