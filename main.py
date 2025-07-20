import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Отримуємо токен з змінних оточення
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7974946517:AAEnAdGn4svTzfia2djygBTwSWYP2SHK8nw")
APPROVER_ID = 8142520596
CHANNEL_USERNAME = "@fiveleagues"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Бот активний. Очікую новини.")
    
    # Тестове повідомлення одразу після команди /start
    news_text = "🔥 ТЕСТОВА НОВИНА: УЄФА підтвердила новий формат Ліги чемпіонів."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Підтвердити", callback_data="approve"),
         InlineKeyboardButton("❌ Відхилити", callback_data="reject")]
    ])
    
    context.bot.send_message(
        chat_id=APPROVER_ID,
        text=news_text,
        reply_markup=keyboard
    )

def handle_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "approve":
        context.bot.send_message(chat_id=CHANNEL_USERNAME, text=query.message.text)
        query.edit_message_text("✅ Опубліковано.")
    elif query.data == "reject":
        query.edit_message_text("❌ Відхилено.")

def main():
    # Створюємо Updater (старий синтаксис)
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Додаємо обробники
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_approval))
    
    # Запускаємо бота
    logger.info("Бот запущений...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
