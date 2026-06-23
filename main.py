from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8825832204:AAHbHrkpybRJBu_HBiotjevPB58J6ZaJ_pA"
GROUP_ID = -1003904422279

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

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle))

app.run_polling()
