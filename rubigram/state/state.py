#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .storage import Storage
import logging


logger = logging.getLogger(__name__)


class State:
    """
    Convenience wrapper for managing individual user conversation states.

    This class provides a user-specific interface to the Storage class,
    simplifying state management for individual users in conversation flows.
    It automatically handles user identification and delegates operations
    to the underlying storage system.

    Parameters:
        storage (Storage):
            The storage instance where states are persisted.
        user_id (str):
            Unique identifier for the user (typically chat_id).

    Attributes:
        storage (Storage): Reference to the storage backend.
        user_id (str): The user identifier for this state instance.

    Example:
    .. code-block:: python
        # Get a State instance for a specific user
        user_state = State(storage, user_id="b0123456789")

        # Set the user's state with additional data
        await user_state.set(
            state="collecting_name",
            attempts=2,
            last_prompt="Please enter your full name:"
        )

        # Retrieve the user's current state
        current_state = await user_state.get()

        # Clear the user's state (e.g., after conversation completion)
        await user_state.delete()
    """

    def __init__(
        self,
        storage: "Storage",
        user_id: str
    ):
        self.storage = storage
        self.user_id = user_id

    async def set(self, state: str, **kwargs):
        """
        Set or update the conversation state for this user.

        Parameters:
            state (str):
                The conversation state identifier (e.g., "awaiting_input",
                "processing_data", "completed").
            **kwargs:
                Arbitrary key-value data to store with the state.

        Returns:
            bool: True if the state was successfully set.

        Note:
            This method overwrites any existing state for this user.
            Use `get()` first if you need to preserve existing data.

        Example:
        .. code-block:: python
            await user_state.set(
                state="collecting_payment",
                amount=10000,
                currency="IRT",
                invoice_id="inv_12345"
            )
        """
        await self.storage.set_state(self.user_id, state, **kwargs)

    async def get(self):
        """
        Retrieve the current conversation state and data for this user.

        Returns:
            Optional[dict]: The stored state data if found, None otherwise.
            Structure: {"state": str, "data": dict}

        Example:
        .. code-block:: python
            data = await user_state.get()
            if data:
                current_state = data["state"]  # e.g., "awaiting_confirmation"
                user_data = data["data"]       # Additional stored data
        """
        return await self.storage.get_state(self.user_id)

    async def delete(self):
        """
        Remove the conversation state for this user from storage.

        Returns:
            bool: True if the state was deleted, False if it didn't exist.

        Example:
        .. code-block:: python
            # Reset user's conversation
            await user_state.delete()

            # Or after completing a workflow
            if workflow_completed:
                await user_state.delete()
        """
        await self.storage.delete_state(self.user_id)