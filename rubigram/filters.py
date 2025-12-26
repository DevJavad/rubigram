#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from __future__ import annotations
import re
from typing import Callable, Optional, Union
from rubigram.types import Update, InlineMessage
import rubigram


CUSTOM_FILTER_NAME = "CustomFilter"
URL_PATTERN = re.compile(
    r"(?:(?:https?|ftp):\/\/)?(?:www\.)?[a-z0-9]+(?:[.\-][a-z0-9]+)*\.[a-z]{2,}(?:\/[^\s]*)?",
    re.IGNORECASE
)
USERNAME_PATTERN = re.compile(r"@[A-Za-z0-9_]{3,32}")


class Filter:
    """
    Asynchronous filter for processing updates in Rubigram.

    This class provides a flexible way to create and combine filters for
    message handling. Filters can be logically combined using AND (&),
    OR (|), and NOT (~) operators.

    Parameters:
        func (callable):
            An async function that takes (client, update) as arguments
            and returns a boolean.

    Example:
    .. code-block:: python
        async def my_filter(client, update):
            return update.text == "hello"

        filter_obj = Filter(my_filter)
        result = await filter_obj(client, update)
    """

    __slots__ = ("func",)

    def __init__(self, func):
        self.func = func

    async def __call__(self, client, update):
        """
        Execute the filter.

        Parameters:
            client (rubigram.Client):
                The client instance.
            update (Update | InlineMessage):
                The update to check.

        Returns:
            bool: True if the filter matches, False otherwise.
        """
        return await self.func(client, update)

    def __and__(self, other):
        """
        Create a new filter that is the logical AND of two filters.

        Parameters:
            other (Filter):
                Another filter to combine with.

        Returns:
            Filter: A new filter that returns True only if both filters match.

        Example:
        .. code-block:: python
            combined = text & private  # Matches text messages in private chats
        """
        async def func(client, update):
            return await self(client, update) and await other(client, update)
        return Filter(func)

    def __or__(self, other):
        """
        Create a new filter that is the logical OR of two filters.

        Parameters:
            other (Filter):
                Another filter to combine with.

        Returns:
            Filter: A new filter that returns True if either filter matches.

        Example:
        .. code-block:: python
            combined = text | file  # Matches text OR file messages
        """
        async def func(client, update):
            return await self(client, update) or await other(client, update)
        return Filter(func)

    def __invert__(self):
        """
        Create a new filter that is the logical NOT of this filter.

        Returns:
            Filter: A new filter that returns True when the original returns False.

        Example:
        .. code-block:: python
            not_text = ~text  # Matches non-text messages
        """
        async def func(client, update):
            return not await self(client, update)
        return Filter(func)


def create(func: Callable, name: Optional[str] = None, **kwargs) -> Filter:
    """
    **Create a custom Rubigram filter.**
        `filters.create(my_filter_func)`

    Custom filters let you control which updates your handlers receive.

    Args:
        func (`Callable`):
            Async function that takes (filter, client, update) and returns bool.

        name (`Optional[str]`):
            Filter class name. Defaults to 'CustomFilter'.

        **kwargs: Extra parameters accessible inside the filter.

    Returns:
        Filter: A custom filter instance.

    Example:
    .. code-block:: python

        from rubigram import filters

        async def is_admin(client, update):
            return update.chat_id in ADMIN_IDS

        admin = filters.create(is_admin)

        @client.on_message(admin)
        async def handle_admin(client, update):
            await update.reply(text="Admin command received!")
    """
    return type(
        name or func.__name__ or CUSTOM_FILTER_NAME,
        (Filter,),
        {"__call__": func, **kwargs}
    )()


async def gif_filter(client, update: "Update") -> bool:
    message = update.new_message
    if not message:
        return False
    file = message.file
    if not file:
        return False
    return bool(file.size and file.size < 1024 * 1024)


async def caption_filter(client, update: "Update") -> bool:
    message = update.new_message
    if not message:
        return False
    file = message.file
    return bool(file and update.new_message.text)


async def reply_filter(client, update: "Update") -> bool:
    message = update.new_message
    return bool(message and getattr(message, "reply_to_message_id", None))


async def text_filter(client, update: "Update") -> bool:
    """
    Filter for text messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains text, False otherwise.
    """
    return bool(getattr(update, "text", None))


async def file_filter(client, update: "Update") -> bool:
    """
    Filter for file messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains a file, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "file", None))


async def live_filter(client, update: "Update") -> bool:
    """
    Filter for live location messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains live location, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "live_location", None))


async def poll_filter(client, update: "Update") -> bool:
    """
    Filter for poll messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains a poll, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "poll", None))


async def contact_filter(client, update: "Update") -> bool:
    """
    Filter for contact messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains contact information, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "contact_message", None))


async def sticker_filter(client, update: "Update") -> bool:
    """
    Filter for sticker messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains a sticker, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "sticker", None))


async def location_filter(client, update: "Update") -> bool:
    """
    Filter for location messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains a location, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "location", None))


async def forward_filter(client, update: "Update") -> bool:
    """
    Filter for forwarded messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message is forwarded, False otherwise.
    """
    message = update.new_message
    return bool(message and getattr(message, "forwarded_from", None))


async def edited_filter(client, update: "Update") -> bool:
    """
    Filter for edited messages.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message is edited, False otherwise.
    """
    return bool(update.updated_message)


async def group_filter(client, update: Union["Update", "InlineMessage"]) -> bool:
    """
    Filter for group chats.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update | InlineMessage): The update to check.

    Returns:
        bool: True if the chat is a group, False otherwise.

    Note:
        Group chat IDs start with "g0".
    """
    return update.chat_id.startswith("g0")


async def channel_filter(client, update: Union["Update", "InlineMessage"]) -> bool:
    """
    Filter for channel chats.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update | InlineMessage): The update to check.

    Returns:
        bool: True if the chat is a channel, False otherwise.

    Note:
        Channel chat IDs start with "c0".
    """
    return update.chat_id.startswith("c0")


async def private_filter(client, update: Union["Update", "InlineMessage"]) -> bool:
    """
    Filter for private chats.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update | InlineMessage): The update to check.

    Returns:
        bool: True if the chat is private, False otherwise.

    Note:
        Private chat IDs start with "b0".
    """
    return update.chat_id.startswith("b0")


def file_type_filter(type: str):
    """
    Create a filter for specific file types.

    Parameters:
        type (str):
            The file type to filter for (e.g., "Gif", "Image", "Video").

    Returns:
        Filter: A filter that matches messages with the specified file type.

    Example:
    .. code-block:: python
        gif_filter = file_type_filter("Gif")
        # Equivalent to using the pre-defined `gif` filter
    """
    async def wrapper(client, update: Update):
        message = update.new_message
        file = message.file or None
        return bool(file and file.file_type == type)
    return Filter(wrapper)


def forwarded_filter(type: str):
    """
    Create a filter for messages forwarded from specific sources.

    Parameters:
        type (str):
            The source type ("Bot", "User", "Channel").

    Returns:
        Filter: A filter that matches messages forwarded from the specified source.

    Example:
    .. code-block:: python
        from_bot = forwarded_filter("Bot")
        # Matches messages forwarded from bots
    """
    async def wrapper(client, update: Update):
        message = update.new_message
        forwarded = message.forwarded_from or None
        return bool(forwarded and forwarded.type_from == type)
    return Filter(wrapper)


async def url_filter(client, update: Update) -> bool:
    """
    Filter for messages containing URLs.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message text contains a URL, False otherwise.
    """
    text = update.text or ""
    if not text:
        return False
    return bool(URL_PATTERN.search(text))


async def hyperlink_filter(client, update: Update):
    """
    Filter for messages with clickable hyperlinks.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains hyperlink metadata, False otherwise.

    Note:
        Checks for "Link" type in message metadata, not plain text URLs.
    """
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Link":
            return True
    return False


async def mention_filter(client, update: Update):
    """
    Filter for messages containing mentions.

    Parameters:
        client (rubigram.Client): The client instance.
        update (Update): The update to check.

    Returns:
        bool: True if the message contains user mentions, False otherwise.
    """
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "MentionText":
            return True
    return False


async def text_bold_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Bold":
            return True
    return False


async def text_mono_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Mono":
            return True
    return False


async def text_quote_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Quote":
            return True
    return False


async def text_italic_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Italic":
            return True
    return False


async def text_strike_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Strike":
            return True
    return False


async def text_spoiler_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Spoiler":
            return True
    return False


async def text_underline_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    if not message:
        return False
    metadata = message.metadata
    if not metadata:
        return False
    for i in metadata.meta_data_parts:
        if i.type == "Underline":
            return True
    return False


async def metadata_filter(client, update: "Update"):
    message = update.new_message or update.updated_message
    return bool(message and message.metadata)


async def username_filter(client, update: "Update"):
    return bool(USERNAME_PATTERN.search(update.text or ""))


# Pre-defined filter instances for common use cases
username = Filter(username_filter)

metadata = Filter(metadata_filter)

text_bold = Filter(text_bold_filter)

text_mono = Filter(text_mono_filter)

text_quote = Filter(text_quote_filter)

text_italic = Filter(text_italic_filter)

text_strike = Filter(text_strike_filter)

text_spoiler = Filter(text_spoiler_filter)

text_underline = Filter(text_underline_filter)

caption = Filter(caption_filter)

reply = Filter(reply_filter)

url = Filter(url_filter)
"""Filter for messages containing URLs in text."""

hyperlink = Filter(hyperlink_filter)
"""Filter for messages with clickable hyperlinks."""

mention = Filter(mention_filter)
"""Filter for messages containing user mentions."""

text = Filter(text_filter)
"""Filter for text messages."""

file = Filter(file_filter)
"""Filter for file messages."""

live = Filter(live_filter)
"""Filter for live location messages."""

poll = Filter(poll_filter)
"""Filter for poll messages."""

contact = Filter(contact_filter)
"""Filter for contact messages."""

sticker = Filter(sticker_filter)
"""Filter for sticker messages."""

location = Filter(location_filter)
"""Filter for location messages."""

forward = Filter(forward_filter)
"""Filter for forwarded messages."""

edited = Filter(edited_filter)
"""Filter for edited messages."""

group = Filter(group_filter)
"""Filter for group chats."""

channel = Filter(channel_filter)
"""Filter for channel chats."""

private = Filter(private_filter)
"""Filter for private chats."""

gif = Filter(gif_filter)
"""Filter for GIF file messages."""

photo = file_type_filter("Image")
"""Filter for image file messages."""

video = file_type_filter("Video")
"""Filter for video file messages."""

music = file_type_filter("Music")
"""Filter for music/audio file messages."""

voice = file_type_filter("Voice")
"""Filter for voice message files."""

document = file_type_filter("File")
"""Filter for document file messages."""

forwarded_bot = forwarded_filter("Bot")
"""Filter for messages forwarded from bots."""

forwarded_user = forwarded_filter("User")
"""Filter for messages forwarded from users."""

forwarded_channel = forwarded_filter("Channel")
"""Filter for messages forwarded from channels."""


def command(
    command: Union[str, list[str]],
    prefix:  Union[str, list[str]] = "/",
    case_sensitive: bool = False,
    start_with: bool = False
) -> bool:
    """
    Create a filter for command messages.

    Parameters:
        command (str | list[str]):
            The command(s) to match (without prefix).
        prefix (str | list[str], optional):
            The prefix(es) to use. Defaults to "/".
        case_sensitive (bool, optional):
            Whether the match should be case-sensitive. Defaults to False.

    Returns:
        Filter: A filter that matches command messages.

    Example:
    .. code-block:: python
        start_cmd = command("start")
        # Matches "/start"

        multi_cmd = command(["start", "help"], prefix=["/", "!"])
        # Matches "/start", "/help", "!start", "!help"
    """
    commands = command if isinstance(command, list) else [command]
    prefixs = prefix if isinstance(prefix, list) else [prefix]

    if not case_sensitive:
        commands = [c.lower() for c in commands]

    command_list = tuple(p + c for p in prefixs for c in commands)

    async def wrapper(client, update: Update):
        if update.text is None:
            return False

        text = update.text if case_sensitive else update.text.lower()
        return any(text.startswith(c) if start_with else text == c for c in command_list)

    return Filter(wrapper)


def chat(chat_id: Union[str, list[str]]) -> bool:
    """
    Create a filter for specific chat IDs.

    Parameters:
        chat_id (str | list[str]):
            The chat ID(s) to match.

    Returns:
        Filter: A filter that matches messages from specific chats.

    Example:
    .. code-block:: python
        specific_chat = chat("b0123456789")
        # Matches messages from chat ID "b0123456789"

        multiple_chats = chat(["b0123456789", "g0987654321"])
        # Matches messages from either chat
    """
    async def wrapper(client, update: Union["Update", "InlineMessage"]):
        chat_ids = chat_id if isinstance(chat_id, list) else [chat_id]
        return update.chat_id in chat_ids
    return Filter(wrapper)


def regex(
    pattern: Union[str, list[str]],
    flags: int = re.IGNORECASE
) -> bool:
    """
    Create a filter for messages matching regular expressions.

    Parameters:
        pattern (str | list[str]):
            The regex pattern(s) to match.
        flags (int, optional):
            Regex flags. Defaults to re.IGNORECASE.

    Returns:
        Filter: A filter that matches messages based on regex patterns.

    Example:
    .. code-block:: python
        hello_filter = regex(r"^hello.*")
        # Matches messages starting with "hello"

        number_filter = regex([r"\d+", r"number"])
        # Matches messages containing digits or the word "number"
    """
    patterns = pattern if isinstance(pattern, list) else [pattern]
    compiled_patterns = [re.compile(p, flags) for p in patterns]

    async def wrapper(client, update: Union["Update", "InlineMessage"]):
        text = getattr(update, "text", None)
        if not text:
            return False
        return any(p.search(text) for p in compiled_patterns)

    return Filter(wrapper)


def button(
    button_id: Union[str, list[str]],
    prefix: Union[str, list[str]] = "",
    case_sensitive: bool = False
) -> bool:
    """
    Create a filter for inline button clicks.

    Parameters:
        button_id (str | list[str]):
            The button ID(s) to match.
        prefix (str | list[str], optional):
            Prefix(es) for button IDs. Defaults to "".
        case_sensitive (bool, optional):
            Whether the match should be case-sensitive. Defaults to False.

    Returns:
        Filter: A filter that matches inline button clicks.

    Note:
        Only works with InlineMessage updates.

    Example:
    .. code-block:: python
        vote_btn = button("vote_yes", prefix="poll_")
        # Matches button with ID "poll_vote_yes"
    """
    button_ids = button_id if isinstance(button_id, list) else [button_id]
    prefixs = prefix if isinstance(prefix, list) else [prefix]

    if not case_sensitive:
        button_ids = [b.lower() for b in button_ids]

    button_id_list = tuple(p + b for p in prefixs for b in button_ids)

    async def wrapper(client, update: "InlineMessage"):
        btn_id = update.aux_data.button_id if case_sensitive else update.aux_data.button_id.lower()
        return any(btn_id.startswith(b) for b in button_id_list)
    return Filter(wrapper)


def state(
    state: Union[str, list[str]],
    prefix: Union[str, list[str]] = "",
    case_sensitive: bool = False
) -> bool:
    """
    Create a filter based on user conversation state.

    Parameters:
        state (str | list[str]):
            The state value(s) to match.
        prefix (str | list[str], optional):
            Prefix(es) for state values. Defaults to "".
        case_sensitive (bool, optional):
            Whether the match should be case-sensitive. Defaults to False.

    Returns:
        Filter: A filter that matches when the user is in a specific state.

    Example:
    .. code-block:: python
        waiting_state = state("waiting_for_name")
        # Matches when user's state is "waiting_for_name"
    """
    states = state if isinstance(state, list) else [state]
    prefixs = prefix if isinstance(prefix, list) else [prefix]

    if not case_sensitive:
        states = [s.lower() for s in states]

    state_list = tuple(p + s for p in prefixs for s in states)

    async def wrapper(client: "rubigram.Client", update: Union["Update", "InlineMessage"]):
        stmt = client.state(update.chat_id)
        data = await stmt.get()
        return data.get("state") in state_list
    return Filter(wrapper)


def sender_id(sender_id: Union[str, list[str]]) -> bool:
    sender_ids = sender_id if isinstance(sender_id, list) else [sender_id]

    async def wrapper(client, update: "Update"):
        message = update.new_message or update.updated_message
        return bool(message and message.sender_id in sender_ids)
    return Filter(wrapper)