"""
Your Python version should be 3.12, 3.13, 3.14
"""

from rubigram import Client, filters
from rubigram.rubino import Rubino
from rubigram.state import Storage
from rubigram.types import Update
from database import connect, disconnect
from database.models import Users
from buttons import user_count
from config import token, database, admin, auth
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")
storage = Storage()
client = Client(token, storage=storage)
rubino = Rubino(auth)


@client.on_started_bot(filters.private)
async def new_start(client: Client, update: Update):
    user_id = update.chat_id
    await Users.get_or_create(user_id=user_id)
    info = await client.get_chat(user_id)
    await client.send_message(user_id, "**Hi, {}**\n\nSend /help command to get bot guide.".format(info.full_name))


@client.on_message(filters.command("start") & filters.private)
async def start_bot(clientr: Client, update: Update):
    user_id = update.chat_id
    await Users.get_or_create(user_id=user_id)
    info = await client.get_chat(user_id)
    await client.send_message(user_id, "**Hi, {}**\n\nSend /help command to get bot guide.".format(info.full_name))


@client.on_message(filters.command("help"))
async def help_command(client: Client, update: Update):
    await update.reply("Send a rubino link to download for you:")


@client.on_message(filters.regex(r"https?://(?:www\.)?rubika\.ir/(?:post|p)/([A-Za-z0-9_-]+)(?:[/?][^\s]*)?"))
async def rubino_downloader(client: Client, update: Update):
    wait_message = await update.reply("⌛️")
    data = await rubino.get_post_by_share_link(update.new_message.text)
    try:
        await wait_message.delete()
        await update.reply_video(data["data"]["post"]["full_file_url"], "**Downloaded By:** @Rubigram")
    except Exception as error:
        logger.error(str(error))
        await wait_message.edit("Error to download your post\n\n{}".format(error))


@client.on_message(filters.command(["users", "user"], ["/", ""], True) & filters.chat(admin))
async def get_users(client: Client, update: Update):
    users = await Users.all().count()
    keypad = user_count(users)
    await update.reply("**Hi Admin**\nID: ||{}||".format(admin), inline_keypad=keypad)


@client.on_start()
async def start(client):
    logger.info("start bot ....")
    await rubino.start()
    await connect(database)


@client.on_stop()
async def stop(client):
    logger.info("stop bot ....")
    await rubino.stop()
    await disconnect()

client.run()