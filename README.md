# Rubigram

Rubigram is a powerful asynchronous Python framework for **building advanced bots on Rubika**, offering features like concurrent message handling, advanced filtering, and support for both webhooks and polling.

<div align="center">
  <img src="http://rubigram.ir/rubigram.jpg" alt="Rubigram Logo" width="200"/>
</div>


## Features

- Asynchronous and fast: handle multiple messages concurrently.
- Advanced filters for private chats, commands, and text messages.
- Easy message and media sending (text, images, videos, files).
- Support for both **webhooks** and **polling**.
- Interactive keyboards and buttons for better user engagement.
- Flexible integration with databases for storing settings and data.


## Quick Example
```python
from rubigram import Client
from rubigram.types import Update

client = Client(token="...")

@client.on_message()
async def start(client: Client, update: Update):
    await update.reply(text="**Hi**, ||rubigram user||")

client.run()
```

## Reply and Edit message
```python
from rubigram import Client
from rubigram.types import Update

client = Client(token="...")

@client.on_message()
async def echo(client: Client, update: Update):
    message = await update.reply(text=f"Hi, {update.new_message.text}")
    await message.edit_text(text="message was edited")

client.run()
```

## Use webhook and run a server
```python
from rubigram import Client, Server, types, filters

client = Client(token="...", webhook="...")
server = Server(client, host="127.0.0.1", port=8080)


@client.on_message(filters.command("start"))
async def start(client: Client, update: types.Update):
    await update.reply("```import rubigram\n\nprint(rubigram.__version__)```")


@client.on_start()
async def start(client):
    print("start bot ....")


@client.on_stop()
async def stop(client):
    print("stop bot")


server.run_server()
```

## Filters
```python
from rubigram import Client, filters
from rubigram.types import Update

client = Client(token="...")


@client.on_message(filters.text)
async def text(client: Client, update: Update):
    await update.reply(text="message is text")


@client.on_message(filters.contact)
async def contact(client: Client, update: Update):
    await update.reply(text="message is contact")


@client.on_message(filters.edited)
async def edited(client: Client, update: Update):
    await update.reply(text="message is edited")


@client.on_message(filters.file)
async def file(client: Client, update: Update):
    await update.reply(text="message is efiledited")

client.run()
```

## Handlers
```python
from rubigram import Client

client = Client(token="...")

@client.on_message()
async def new_message():
    ...
    
@client.on_inline_message()
async def inline_message():
    ...
    
@client.on_update_message()
async def update_message():
    ...
    
@client.on_remove_message()
async def remove_message():
    ...
    
@client.on_started_bot()
async def start_bot():
    ...
    
@client.on_stopped_bot()
async def stop_bot():
    ...
    
@client.on_start()
async def start():
    ...

@client.on_stop()
async def stop():
    ...
```

## Contex Manager
```python
from rubigram import Client
import asyncio


async def main():
    async with Client(token="...") as client:
        data = await client.get_me()
        print(data.bot_id)

asyncio.run(main())
```

## Implementation of multiple programs
```python
from rubigram import Client
import asyncio

tokens = ["TOKEN_1", "TOKEN_2"]

async def main():
    for token in tokens:
        async with Client(token=token) as client:
            info = await client.get_me()
            print(info)

asyncio.run(main())
```

## Rubino
```python
from rubigram.rubino import Rubino
import asyncio


async def main():
    async with Rubino(auth="...") as client:
        info = await client.get_my_profile_info()
        print(info)

asyncio.run(main())
```