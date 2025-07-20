import logging
import os
import telegram
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Команда /start
async def start(update, context):
    await update.message.reply_text("Привіт! Я бот, що публікує футбольні новини.")

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
