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
    HTTP webhook server for receiving Rubika Bot API updates.

    This class implements a web server that listens for incoming updates
    from Rubika and dispatches them to the client's handlers. It supports
    all update types defined in the API and integrates with the client's
    lifecycle management.

    Parameters:
        client (rubigram.Client):
            The bot client instance that will process updates.
        host (str, optional):
            Host address to bind the server to. Use "0.0.0.0" to listen
            on all interfaces. Defaults to "0.0.0.0".
        port (int, optional):
            Port number to listen on. Defaults to 8000.

    Attributes:
        client (rubigram.Client): The bot client instance.
        host (str): Server host address.
        port (int): Server port number.
        app (Application): aiohttp web application.
        routes (RouteTableDef): HTTP route definitions.
        runner (Optional[AppRunner]): aiohttp application runner.
        site (Optional[TCPSite]): TCP site for the server.

    Example:
    .. code-block:: python
        # Create client with webhook
        client = Client(
            token="YOUR_BOT_TOKEN",
            webhook="https://example.com/webhook"
        )

        # Create and start server
        server = Server(client, host="127.0.0.1", port=8080)

        # Run server (blocks until interrupted)
        server.run_server()

        # Or manage server lifecycle manually
        await server.start()
        # Server is now running...
        await server.stop()
    """

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
        """
        Parse and dispatch an incoming update.

        Parameters:
            data (dict):
                Raw JSON data received from Rubika API.

        Note:
            - For inline messages, creates an InlineMessage object
            - For other updates, creates an Update object
            - Dispatches the parsed update to client's handlers
            - Binds the client to the parsed object

        Example:
        .. code-block:: python
            # Manual processing (for testing)
            await server.process_update({
                "update": {
                    "chat_id": "b0123456789",
                    "new_message": {...}
                }
            })
        """
        if "inline_message" in data:
            update = rubigram.types.InlineMessage.parse(
                data["inline_message"], self.client
            )
        else:
            update = rubigram.types.Update.parse(data["update"], self.client)

        await self.client.dispatcher(update)

    def receive_data(self):
        """
        Create a request handler for incoming webhook data.

        Returns:
            callable: An async function that handles HTTP POST requests.

        Note:
            The handler:
            1. Parses JSON from request body
            2. Logs the received data
            3. Processes the update asynchronously
            4. Returns JSON response with status
            5. Catches and logs any processing errors
        """
        async def wrapper(request: Request):
            try:
                data = await request.json()
                logger.debug("Receive data from webhook, data=%s", data)
                await self.process_update(data)
                return json_response({"status": "OK", "data": data})
            except Exception as error:
                logger.error(
                    "Error receive data from webhook, error=%s", error)
                return json_response({"status": "ERROR", "errcor": error})
        return wrapper

    def setup_routes(self):
        """
        Configure HTTP routes for all update types.

        Creates POST endpoints for each update type defined in
        `rubigram.enums.UpdateEndpointType`. Each endpoint uses the
        same handler to receive and process updates.

        Note:
            Endpoint paths correspond to the enum values (e.g., "/newMessage",
            "/updateMessage", "/inlineMessage").
        """
        for i in rubigram.enums.UpdateEndpointType:
            handler = self.receive_data()
            self.routes.post("/{}".format(i.value))(handler)
        self.app.add_routes(self.routes)

    async def start(self):
        """
        Start the webhook server.

        This method:
        1. Sets up all routes
        2. Creates and configures the AppRunner
        3. Starts the TCP site
        4. Logs server startup information

        Note:
            Also triggers the client's startup handlers via the
            app.on_startup callback.

        Example:
        .. code-block:: python
            await server.start()
            print(f"Server running on {server.host}:{server.port}")
        """
        self.setup_routes()
        self.runner = AppRunner(self.app)
        await self.runner.setup()
        self.site = TCPSite(self.runner, self.host, self.port)
        await self.site.start()

    async def stop(self):
        """
        Stop the webhook server gracefully.

        This method:
        1. Cleans up the AppRunner
        2. Logs server shutdown
        3. Sets runner and site to None

        Note:
            Also triggers the client's cleanup handlers via the
            app.on_cleanup callback.

        Example:
        .. code-block:: python
            await server.stop()
            print("Server stopped")
        """
        if self.runner:
            await self.runner.cleanup()

    async def run(self):
        """
        Run the server indefinitely until interrupted.

        This method:
        1. Starts the server
        2. Waits on an event (blocks forever)
        3. Handles cancellation gracefully
        4. Ensures server is stopped on exit

        Note:
            Used internally by `run_server()`.
        """
        await self.start()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()

    def run_server(self, set_endpoint: bool = True):
        """
        Run the server in the main thread (blocking call).

        This method:
        1. Creates a new asyncio event loop
        2. Runs the server indefinitely
        3. Handles KeyboardInterrupt for graceful shutdown
        4. Closes the event loop on exit

        Example:
        .. code-block:: python
            # This blocks until Ctrl+C is pressed
            server.run_server()
        """
        self.client.set_new_endpoint = set_endpoint
        try:
            logger.info("Start server in %s", self.client.webhook)
            asyncio.run(self.run())
        except KeyboardInterrupt:
            logger.info("Stop server in %s", self.client.webhook)