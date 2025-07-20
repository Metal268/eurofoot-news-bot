import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import asyncio
import requests

# === Налаштування ===
BOT_TOKEN = "7974946517:AAEnAdGn4svTzfia2djygBTwSWYP2SHK8nw"
CHANNEL_USERNAME = "@fiveleagues"
APPROVER_ID = 8142520596  # Твій Telegram user ID

# === Логи ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Структура для зберігання черг на підтвердження ===
pending_posts = {}

# === Функція: надсилання посту адміну на затвердження ===
async def send_for_approval(bot: Bot, text: str, photo_url: str | None = None):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Опублікувати", callback_data="approve"),
         InlineKeyboardButton("❌ Відхилити", callback_data="reject")]
    ])
    if photo_url:
        message = await bot.send_photo(
            chat_id=APPROVER_ID,
            photo=photo_url,
            caption=text,
            reply_markup=keyboard
        )
    else:
        message = await bot.send_message(
            chat_id=APPROVER_ID,
            text=text,
            reply_markup=keyboard
        )
    pending_posts[message.message_id] = {
        "text": text,
        "photo": photo_url
    }

# === Обробник підтвердження/відхилення ===
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = pending_posts.get(query.message.message_id)
    if not data:
        await query.edit_message_reply_markup(reply_markup=None)
        return

    if query.data == "approve":
        if data["photo"]:
            await context.bot.send_photo(chat_id=CHANNEL_USERNAME, photo=data["photo"], caption=data["text"])
        else:
            await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=data["text"])
        await query.edit_message_caption(caption=f"✅ Опубліковано:\n\n{data['text']}")
    elif query.data == "reject":
        await query.edit_message_caption(caption="❌ Відхилено.")
    pending_posts.pop(query.message.message_id, None)

# === Функція: імітація отримання новини (приклад) ===
async def post_news_periodically(app: Application):
    await asyncio.sleep(10)  # Затримка перед першим запуском
    while True:
        # ❗ Тут має бути твій реальний парсер або API-джерело
        fake_news = {
            "text": "🔴 Арсенал підписав Ноні Мадуеке! Контракт на 5 років, сума — £52 млн.",
            "photo": "https://pbs.twimg.com/media/ExamplePhoto.jpg"
        }
        await send_for_approval(app.bot, text=fake_news["text"], photo_url=fake_news["photo"])
        await asyncio.sleep(3600)  # Очікування перед наступною новиною

# === Старт / help ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот працює. Новини будуть надходити на затвердження.")

# === Запуск ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Фонове завдання для новин
    app.job_queue.run_once(lambda _: asyncio.create_task(post_news_periodically(app)), when=1)

    app.run_polling()

if __name__ == "__main__":
    main()
