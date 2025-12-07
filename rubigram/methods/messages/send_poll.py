#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, Union
from rubigram.utils import AutoDelete
import rubigram


class SendPoll:
    async def send_poll(
        self: "rubigram.Client",
        chat_id: str,
        question: str,
        options: list[str],
        chat_keypad: Optional["rubigram.types.Keypad"] = None,
        inline_keypad: Optional["rubigram.types.Keypad"] = None,
        chat_keypad_type: Optional[
            Union[str, "rubigram.enums.ChatKeypadType"]
        ] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        auto_delete: Optional[int] = None
    ) -> "rubigram.types.UMessage":
        """
        **Send a poll to a chat.**
            `await client.send_poll(chat_id, question, options)`

        This method sends an interactive poll to the specified chat.
        Users can vote on the provided options and see real-time results.

        Args:
            chat_id (`str`):
                The ID of the chat where the poll will be sent.

            question (`str`):
                The poll question text.

            options (`list[str]`):
                List of answer options for the poll (minimum 2 options).

            chat_keypad (`Optional[rubigram.types.Keypad]`):
                Custom keyboard to show in the chat. Defaults to None.

            inline_keypad (`Optional[rubigram.types.Keypad]`):
                Inline keyboard to attach below the poll. Defaults to None.

            chat_keypad_type (`Optional[rubigram.enums.ChatKeypadType]`):
                Type of chat keypad (New, Remove). Defaults to None.

            disable_notification (`Optional[bool]`):
                If True, disables notification for the poll. Defaults to False.

            reply_to_message_id (`Optional[str]`):
                ID of the message to reply to. Defaults to None.

            auto_delete (`Optional[int]`):
                If set, the message will be automatically deleted after the specified number of seconds.

        Returns:
            rubigram.types.UMessage: The sent poll message object with client binding.

        Example:
        .. code-block:: python

            # Send a poll with multiple options
            await client.send_poll(
                chat_id=chat_id,
                question="What's your favorite programming language?",
                options=["Python", "JavaScript", "Java", "C++"],
                disable_notification=True
            )

        Note:
            - Polls must have at least 2 options
            - Users can only vote once per poll
            - Poll results are visible to all participants in real-time
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

        response = await self.request("sendPoll", data)
        message = rubigram.types.UMessage.parse(response, self)
        message.chat_id = chat_id

        if auto_delete and auto_delete > 0:
            AutoDelete.run(self, message, auto_delete)

        return message