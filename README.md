<p align="center">
  <img src="http://rubigram.ir/rubigram.jpg" alt="Rubigram" width="200"/>
</p>
<p align="center">
  <strong> Python library for rubika API</strong>
</p>
<p align="center">
  <a href="https://pypi.org/project/RubigramClient">
    <img src="https://img.shields.io/pypi/v/RubigramClient?style=flat-square" alt="PyPI">
  </a>
  <a href="http://rubigram.ir/doc">
    <img src="https://img.shields.io/badge/docs-online-blue?style=flat-square" alt="Documentation">
  </a>
</p>

# Rubigram
Rubigram is a powerful asynchronous Python framework for **building advanced bots on Rubika**, offering features like concurrent message handling, advanced filtering, and support for both webhooks and polling.


## Features
- Asynchronous and fast: handle multiple messages concurrently.
- Advanced filters for private chats, commands, and text messages.
- Easy message and media sending (text, images, videos, files).
- Support for both **webhooks** and **polling**.
- Interactive keyboards and buttons for better user engagement.
- Flexible integration with databases for storing settings and data.

## Start
```python
from rubigram import Client, filters
from rubigram.types import Update

client = Client("bot_token")

@client.on_message(filters.command("start"))
async def start(client: Client, update: Update):
    await update.reply("||Hello|| __from__ **Rubigram!**")    
    
client.run()
```

## Button and Keypad
```python
from rubigram import Client, filters
from rubigram.enums import ChatKeypadType
from rubigram.types import Update, Keypad, Button, KeypadRow

client = Client("bot_token")


@client.on_message(filters.photo)
async def start(client: Client, update: Update):
    button_1 = Button("send", "send Photo")
    button_2 = Button("save", "Save Photo")
    row = KeypadRow([button_1, button_2])
    keypad = Keypad([row])
    await update.reply(
        "Select your action:",
        chat_keypad=keypad,
        chat_keypad_type=ChatKeypadType.NEW
    )

client.run()
```

## Use webhook and Get inline button data
```python
from rubigram import Client, Server, filters
from rubigram.types import (
    Update,
    Button,
    Keypad,
    KeypadRow,
    InlineMessage
)


client = Client(token="bot_token")
server = Server(client, "webhook_url")


@client.on_message(filters.photo)
async def start(client: Client, update: Update):
    button_1 = Button("send", "send Photo")
    button_2 = Button("save", "Save Photo")
    row = KeypadRow([button_1, button_2])
    keypad = Keypad([row])
    await update.reply("Select your action:", inline_keypad=keypad)


@client.on_inline_message(filters.button(["send", "save"]))
async def inline_message(client: Client, message: InlineMessage):
    button_id = message.aux_data.button_id
    if button_id == "send":
        await message.answer("You clicked the send button")
    else:
        await message.answer("You clicked the save button")


@client.on_start()
async def start(client):
    print("Start bot ....")


@client.on_stop()
async def stop(client):
    print("Stop bot")


server.run_server()
```

## Auto state and save tmp data in cache
```python
from rubigram import Client, Storage, filters
from rubigram.types import Update


storage = Storage(ttl=120)
client = Client("bot_token", storage=storage) # You can leave the `storage` parametr empty


@client.on_message(filters.command("start") & filters.private)
async def start(client: Client, update: Update):
    state = client.state(update.chat_id)
    await state.set("name")
    await update.reply("Send your name:")


@client.on_message(filters.state("name") & filters.text & filters.private)
async def save_name(client: Client, update: Update):
    state = client.state(update.chat_id)
    await state.set("email", name=update.text)
    await update.reply("Send your Email:")


@client.on_message(filters.state("email") & filters.text & filters.private)
async def save_email(client: Client, update: Update):
    state = client.state(update.chat_id)
    data = await state.get()
    print(data)
    await state.delete()


client.run()
```


## Implementation of multiple programs
```python
from rubigram import Client
import asyncio

tokens = ["TOKEN_1", "TOKEN_2"]

async def main():
    for token in tokens:
        async with Client(token) as client:
            info = await client.get_me()
            print(info)

asyncio.run(main())
```

## Rubino
```python
from rubigram.rubino import Rubino
import asyncio


async def main():
    async with Rubino(auth="auth_account") as client:
        info = await client.get_my_profile_info()
        print(info)

asyncio.run(main())
```