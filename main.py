from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

TOKEN = "8825832204:AAHbHrkpybRJBu_HBiotjevPB58J6ZaJ_pA"
GROUP_ID = -1003904422279

msg_to_user = {}

def handle(update: Update, context: CallbackContext):
    msg = update.message
    if not msg:
        return

    # ЛС → ГРУППА
    if msg.chat.type == "private":

        forwarded = context.bot.forward_message(
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

                context.bot.send_message(
                    chat_id=user_id,
                    text="💬 Ответ:\n\n" + msg.text
                )

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.all, handle))

updater.start_polling()
updater.idle()
