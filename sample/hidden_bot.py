from rubigram import Client, filters, types, Server


CHAT: str = "" # Group chat_id
ADMIN: str = "" # Admin sender_id
WEBHOOK: str = "" # Webhook Url
TOKEN: str = "" # Bot token

client = Client(TOKEN, WEBHOOK)
server = Server(client)


@client.on_message(filters.text)
async def copy_message(_, update: types.Update):
    if update.new_message.sender_id == ADMIN:
        chat_id = update.chat_id
        await client.send_message(chat_id, update.text, reply_to_message_id=update.new_message.reply_to_message_id)
        await client.delete_messages(chat_id, update.message_id)

server.run_server()