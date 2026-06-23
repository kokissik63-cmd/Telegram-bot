main.py
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
GROUP_ID = -1003904422279

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

msg_to_user = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    # ЛС → ГРУППА
    if msg.chat.type == "private":

        forwarded = await context.bot.forward_message(
            chat_id=GROUP_ID,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id
        )

        msg_to_user[forwarded.message_id] = msg.chat_id

    # ГРУППА → ЛС
    elif msg.chat.type in ["group", "supergroup"]:

        if msg.reply_to_message:
            replied_id = msg.reply_to_message.message_id

            if replied_id in msg_to_user:
                user_id = msg_to_user[replied_id]

                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"💬 Ответ:\n\n{msg.text}"
                )

application.add_handler(MessageHandler(filters.ALL, handle))

@app.post(f"/{TOKEN}")
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.get("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
