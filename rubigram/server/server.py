from aiohttp.web import Application, AppRunner, RouteTableDef, TCPSite, Request, json_response
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Server:
    def __init__(
        self,
        client: "rubigram.Client",
        host: str = "0.0.0.0",
        port: int = 8000
    ):
        self.client = client
        self.host = host
        self.port = port

        self.app = Application()
        self.routes = RouteTableDef()

        self.app.on_startup.append(self.client.startup)
        self.app.on_cleanup.append(self.client.cleanup)

        self.runner = None
        self.site = None

    async def process_update(self, data: dict):
        if "inline_message" in data:
            update = rubigram.types.InlineMessage.parse(
                data["inline_message"], self.client
            )
        else:
            update = rubigram.types.Update.parse(data["update"], self.client)

        await self.client.dispatcher(update)

    def receive_data(self):
        async def wrapper(request: Request):
            try:
                data = await request.json()
                logger.debug("DATA RECEIVE(data=%s)", data)
                await self.process_update(data)
                return json_response({"status": "OK", "data": data})
            except Exception as error:
                logger.error("DATA RECEIVE(error=%s)", error)
                return json_response({"status": "ERROR", "errcor": error})
        return wrapper

    def setup_routes(self):
        for i in rubigram.enums.UpdateEndpointType:
            handler = self.receive_data()
            self.routes.post("/{}".format(i.value))(handler)
        self.app.add_routes(self.routes)

    async def start(self):
        self.setup_routes()
        self.runner = AppRunner(self.app)
        await self.runner.setup()
        self.site = TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        logger.info("SERVER START(address=%s)", self.client.webhook)

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()
            logger.info("SERVER STOP")

    async def run(self):
        await self.start()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()

    def run_server(self):
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            pass