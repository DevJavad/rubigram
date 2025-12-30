#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations

from typing import Optional, Union
from rubigram.utils import AutoDelete
import rubigram


class SendPoll:
    async def send_poll(
        self: rubigram.Client,
        chat_id: str,
        question: str,
        options: list[str],
        chat_keypad: Optional[rubigram.types.Keypad] = None,
        inline_keypad: Optional[rubigram.types.Keypad] = None,
        chat_keypad_type: Optional[Union[str, rubigram.enums.ChatKeypadType]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None,
        headers: Optional[dict] = None,
        proxy: Optional[str] = None,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        backoff: Optional[float] = None,
        max_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None
    ) -> rubigram.types.UMessage:
        """
        Send a poll to a chat on Rubika.

        This method allows you to create and send interactive polls with multiple
        options for users to vote on. Supports additional features like keyboards,
        notifications, reply functionality, and auto-deletion.

        Parameters:
            chat_id (str):
                The target chat ID where the poll will be sent.

            question (str):
                The poll question/title that users will see.

            options (list[str]):
                List of answer options for the poll.
                Must contain at least 2 options.

            chat_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach to the chat message.

            inline_keypad (Optional[rubigram.types.Keypad], default: None):
                Keypad to attach inline with the message.

            chat_keypad_type (Optional[Union[str, rubigram.enums.ChatKeypadType]], default: None):
                Type of chat keyboard (e.g., "New", "Remove", or enum value).

            disable_notification (bool, default: False):
                If True, sends the message silently.

            reply_to_message_id (Optional[str], default: None):
                ID of a message to reply to.

            auto_delete (Optional[int], default: None):
                Number of seconds after which the poll message will be automatically deleted.
                If None or 0, no auto-deletion will be scheduled.

            headers (Optional[dict], default: None):
                Optional HTTP headers for the request.

            proxy (Optional[str], default: None):
                Optional proxy URL to use for requests.

            retries (Optional[int], default: None):
                Number of retry attempts on request failure.

            delay (Optional[float], default: None):
                Initial delay between retries in seconds.

            backoff (Optional[float], default: None):
                Backoff multiplier applied after each retry.

            max_delay (Optional[float], default: None):
                Maximum delay between retries.

            timeout (Optional[float], default: None):
                Total request timeout in seconds.

            connect_timeout (Optional[float], default: None):
                Timeout for establishing the connection.

            read_timeout (Optional[float], default: None):
                Timeout for reading the response data.

        Returns:
            rubigram.types.UMessage:
                The message object representing the sent poll.

        Example:
        .. code-block:: python
            # Send a simple poll
            message = await client.send_poll(
                chat_id="123456",
                question="What's your favorite color?",
                options=["Red", "Blue", "Green", "Yellow"]
            )
            
            # Send a poll with reply and auto-deletion
            message = await client.send_poll(
                chat_id="123456",
                question="Best programming language?",
                options=["Python", "JavaScript", "Java", "C++"],
                reply_to_message_id="msg_789",
                auto_delete=300  # Delete after 5 minutes
            )
            
            # Send a poll silently with custom keypad
            from rubigram import types
            
            keypad = types.Keypad(rows=[[
                types.Button(
                    text="View Results",
                    action_type="Custom",
                    payload="view_poll_results"
                )
            ]])
            message = await client.send_poll(
                chat_id="123456",
                question="Weekly meeting time?",
                options=["9 AM", "2 PM", "4 PM", "6 PM"],
                disable_notification=True,
                inline_keypad=keypad
            )
            
            print(f"Poll sent with message ID: {message.message_id}")

        Note:
            - Polls are interactive and users can vote by tapping on options
            - Each option should be a clear, concise string
            - Minimum 2 options are required for a valid poll
            - Poll results are typically visible to all participants
            - Auto-deletion is scheduled asynchronously using `AutoDelete.run()`
            - The returned UMessage object has its `chat_id` attribute updated for consistency
            - Useful for surveys, voting, decision-making, and gathering user feedback
        """
        data = {
            "chat_id": chat_id,
            "question": question,
            "options": options
        }

        if chat_keypad:
            data["chat_keypad"] = chat_keypad.as_dict()
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.as_dict()
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type
        if disable_notification:
            data["disable_notification"] = disable_notification
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        response = await self.request(
            "sendPoll",
            data,
            headers,
            proxy,
            retries,
            delay,
            backoff,
            max_delay,
            timeout,
            connect_timeout,
            read_timeout
        )
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message