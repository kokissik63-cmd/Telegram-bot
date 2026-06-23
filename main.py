import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8825832204:AAHbHrkpybRJBu_HBiotjevPB58J6ZaJ_pA"
GROUP_ID = -1003904422279

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

msg_to_user = {}

# ======================
# ЛОГИКА БОТА
# ======================
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

# ======================
# WEB SERVER (Render)
# ======================
@app.route("/")
def home():
    return "Bot is running"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ======================
# START
# ======================
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()

        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    asyncio.run(run())
