from rubigram import Client, filters, types, Server
from rubigram.types import Update


CHAT: str = ""  # Group chat_id
ADMIN: str = ""  # Admin sender_id
WEBHOOK: str = ""  # Webhook Url
TOKEN: str = "BHHAB0IQJDMDKZWVHNKTJDGHCDZRHDQKDAPSHBVOUFXTKZXBNVFHPXULRIJQDXND"  # Bot token

client = Client(TOKEN)
server = Server(client)


@client.on_message(filters.text & filters.group)
async def copy_message(_, update: Update):
    if update.sender_id == ADMIN:
        await update.delete()
        await client.send_message(
            update.chat_id,
            update.text,
            reply_to_message_id=update.new_message.reply_to_message_id
        )


@client.on_message(filters.photo & filters.group)
async def copy_photo(_, update: Update):
    if update.sender_id == ADMIN:
        await update.delete()
        await client.send_photo(
            update.chat_id,
            update.new_message.file.file_id,
            update.text,
            reply_to_message_id=update.new_message.reply_to_message_id
        )


client.run()