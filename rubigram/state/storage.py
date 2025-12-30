#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from aiocache import Cache
from aiocache.serializers import JsonSerializer
import logging


logger = logging.getLogger(__name__)


class Storage:
    """
    Asynchronous storage for managing user conversation states.

    This class provides a simple key-value storage using aiocache to persist
    user conversation states and associated data. States are stored with
    configurable TTL (time-to-live) and automatically serialized to JSON.

    Parameters:
        ttl (int, optional):
            Time-to-live for stored states in seconds. After this time,
            states are automatically evicted from cache. Defaults to 3600
            (1 hour).

    Attributes:
        cache (Cache):
            The underlying aiocache instance configured for memory storage
            with JSON serialization.

    Example:
    .. code-block:: python
        # Create storage with custom TTL
        storage = Storage(ttl=7200)  # 2 hours TTL

        # Set user state with additional data
        await storage.set_state(
            user_id="b0123456789",
            state="waiting_for_name",
            name="John",
            age=25
        )

        # Get user state
        state_data = await storage.get_state("b0123456789")
        # Returns: {"state": "waiting_for_name", "data": {"name": "John", "age": 25}}

        # Delete user state
        await storage.delete_state("b0123456789")
    """

    def __init__(self, ttl: int = 3600):
        self.cache = Cache(
            Cache.MEMORY,
            serializer=JsonSerializer(),
            ttl=ttl
        )

    async def set_state(self, user_id: str, state: str, **kwargs):
        """
        Set or update a user's conversation state with optional data.

        Parameters:
            user_id (str):
                Unique identifier for the user (typically chat_id).
            state (str):
                The conversation state identifier (e.g., "waiting_for_name",
                "collecting_data").
            **kwargs:
                Arbitrary key-value pairs to store alongside the state.

        Returns:
            bool: True if the state was successfully set.

        Note:
            The state is stored with the key format: "state:{user_id}"
            Example: "state:b0123456789"

        Example:
        .. code-block:: python
            await storage.set_state(
                user_id="b0123456789",
                state="collecting_preferences",
                language="fa",
                theme="dark",
                step=3
            )
        """
        payload = {"state": state, "data": kwargs}
        return await self.cache.set("state:{}".format(user_id), payload)

    async def get_state(self, user_id: str):
        """
        Retrieve a user's conversation state and associated data.

        Parameters:
            user_id (str):
                Unique identifier for the user.

        Returns:
            Optional[dict]: The stored state data if found, None otherwise.
            Structure: {"state": str, "data": dict}

        Example:
        .. code-block:: python
            data = await storage.get_state("b0123456789")
            if data:
                current_state = data["state"]  # e.g., "waiting_for_name"
                user_data = data["data"]       # e.g., {"name": "John"}
        """
        await self.cache.get("state:{}".format(user_id))

    async def delete_state(self, user_id: str):
        """
        Delete a user's conversation state from storage.

        Parameters:
            user_id (str):
                Unique identifier for the user.

        Returns:
            bool: True if the state was deleted, False if it didn't exist.

        Example:
        .. code-block:: python
            # Clear user's conversation state
            await storage.delete_state("b0123456789")
        """
        await self.cache.delete("state:{}".format(user_id))