from rubigram import Client, filters
from rubigram.types import Update
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("main")


class Bot:
    STATUS: bool = True
    ADMIN: str = "" # Sender ID of User ADMIN
    TOKEN: str = "" # Bot TOKEN


MEDIA_TYPES = {
    "Image": "send_photo",
    "Gif": "send_gif",
    "Video": "send_video",
    "Music": "send_music",
    "Voice": "send_voice",
    "File": "send_file",
}

client = Client(Bot.TOKEN)


@client.on_message(filters.command(["active", "disable"], "") & filters.group & filters.sender_id(Bot.ADMIN))
async def on_and_off_bot(_, update: Update):
    text = update.text
    if text == "active" and not Bot.STATUS:
        Bot.STATUS = True
        return await update.reply("Bot is `active`")
    elif text == "disable" and Bot.STATUS:
        Bot.STATUS = False
        return await update.reply("Bot is `disable`")


@client.on_message(filters.group & filters.sender_id(Bot.ADMIN) & filters.text & ~filters.file)
async def copy_message(_, update: Update):
    message = update.new_message
    if Bot.STATUS and message:
        await update.delete()
        await client.send_message(
            update.chat_id,
            update.text,
            reply_to_message_id=message.reply_to_message_id,
            metadata=update.new_message.metadata.as_dict() if message.metadata else None
        )


@client.on_message(filters.file & filters.sender_id(Bot.ADMIN))
async def copy_media(_, update: Update):
    message = update.new_message
    if not Bot.STATUS or not message:
        return

    await update.delete()

    metadata = message.metadata
    file = message.file

    method_name = MEDIA_TYPES.get(file.file_type)
    if not method_name:
        return

    send_method = getattr(client, method_name, None)
    if not send_method:
        return
    try:
        await send_method(
            update.chat_id,
            file.file_id,
            update.text,
            reply_to_message_id=message.reply_to_message_id,
            metadata=metadata.as_dict()
        )
    except:
        pass


client.run()
