import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    CallbackQueryHandler
)

BOT_TOKEN = "7974946517:AAEnAdGn4svTzfia2djygBTwSWYP2SHK8nw"
APPROVER_ID = 8142520596
CHANNEL_USERNAME = "@fiveleagues"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний. Очікую новини.")


async def send_news_for_approval(context: ContextTypes.DEFAULT_TYPE):
    news_text = "🔥 УЄФА підтвердила новий формат Ліги чемпіонів."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Підтвердити", callback_data="approve"),
         InlineKeyboardButton("❌ Відхилити", callback_data="reject")]
    ])
    await context.bot.send_message(
        chat_id=APPROVER_ID,
        text=news_text,
        reply_markup=keyboard
    )


async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "approve":
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=query.message.text)
        await query.edit_message_text("✅ Опубліковано.")
    elif query.data == "reject":
        await query.edit_message_text("❌ Відхилено.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_approval))

    app.job_queue.run_once(send_news_for_approval, 5)

    print("Бот запущено.")
    app.run_polling()


if __name__ == "__main__":
    main()
