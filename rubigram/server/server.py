#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiohttp.web import Application, AppRunner, RouteTableDef, TCPSite, Request, json_response
import asyncio
import logging
import rubigram


logger = logging.getLogger(__name__)


class Server:
    """
    Initialize a new webhook server.

    Parameters:
        client (rubigram.Client):
            The bot client that will process updates.

        url (str):
            Public URL where your server is accessible.
            Example: "https://bot.example.com" or "https://123.456.789.0:8443"

        set_endpoints (bool, default: True):
            If True, automatically calls update_bot_endpoints() for all
            endpoint types on server startup.

        host (str, default: "0.0.0.0"):
            Host interface to bind the server to.
            Use "0.0.0.0" to accept connections from any interface.

        port (int, default: 8000):
            Port number to listen on.

    Note:
        - The URL must be accessible from the internet
        - HTTPS is recommended for production
        - Port should be open in firewall
    """

    def __init__(
        self,
        client: "rubigram.Client",
        url: str,
        set_endpoints: bool = True,
        host: str = "0.0.0.0",
        port: int = 8000
    ):
        self.client = client
        self.url = url
        self.set_endpoints = set_endpoints
        self.host = host
        self.port = port

        self.app = Application()
        self.routes = RouteTableDef()

        self.runner = None
        self.site = None


    async def setup(self):
        """
        Setup webhook endpoints with Rubika.

        Registers all UpdateEndpointType endpoints with Rubika API.
        Each endpoint type gets its own URL path.

        Example endpoints:
            - https://example.com/RECEIVE_UPDATE
            - https://example.com/ANOTHER_ENDPOINT_TYPE
            - etc.
        """
        if self.set_endpoints:
            for i in rubigram.enums.UpdateEndpointType:
                type = i.value
                url = f"{self.url}/{type}"
                res = await self.client.update_bot_endpoints(url, type)
                logger.info("Endpoint set for %s: %s", type, res.get("status"))

    async def process_update(self, data: dict):
        """
        Process incoming update data.

        Parses raw update JSON and dispatches to appropriate handlers.

        Parameters:
            data (dict): Raw update data from Rubika.

        Note:
            - Handles both regular updates and inline messages
            - Logs processing errors
        """

        if "update" in data:
            update = rubigram.types.Update.parse(data["update"], self.client)
        else:
            update = rubigram.types.InlineMessage.parse(
                data["inline_message"], self.client
            )

        await self.client.dispatcher.dispatch(update)

    def receive_data(self):
        """
        Create request handler for webhook endpoints.

        Returns an async function that:
            1. Parses JSON request body
            2. Logs received data
            3. Processes the update
            4. Returns JSON response

        Returns:
            Callable: aiohttp request handler function.
        """
        async def wrapper(request: Request):
            try:
                data = await request.json()
                logger.debug("Receive data: %s", data)
                await self.process_update(data)
                return json_response({"status": "OK", "data": data})
            except Exception as error:
                logger.error("Error processing update: %s", error)
                return json_response({"status": "ERROR", "error": error})
        return wrapper

    def setup_routes(self):
        """
        Setup URL routes for all endpoint types.

        Creates POST routes for each UpdateEndpointType value.
        Routes are in the format: "/{ENDPOINT_TYPE}"

        Example:
            - POST /RECEIVE_UPDATE
            - POST /ANOTHER_ENDPOINT_TYPE
        """

        """
        Start the webhook server.

        This method:
        1. Sets up webhook endpoints with Rubika (if enabled)
        2. Configures routes
        3. Starts the aiohttp server
        4. Begins listening for requests
        """
        for i in rubigram.enums.UpdateEndpointType:
            handler = self.receive_data()
            self.routes.post("/{}".format(i.value))(handler)
        self.app.add_routes(self.routes)

    async def start(self):
        await self.client.start()
        await self.setup()
        self.setup_routes()
        self.runner = AppRunner(self.app)
        await self.runner.setup()
        self.site = TCPSite(self.runner, self.host, self.port)
        await self.site.start()

    async def stop(self):
        await self.client.stop()
        await self.runner.cleanup()

    async def run(self):
        await self.start()
        logger.info(
            "Start Server | url=%s | host=%s | port=%s", self.url, self.host, self.port
        )
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()
            logger.info(
                "Shutdown Server | url=%s | host=%s | port=%s", self.url, self.host, self.port
            )

    def run_server(self):
        """
        Run the server (blocking version).

        Convenience method that runs the server in the main thread.
        Handles KeyboardInterrupt for graceful shutdown.

        Example:
            server = Server(client, "https://example.com")
            server.run_server()  # Blocks here until Ctrl+C
        """
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            pass