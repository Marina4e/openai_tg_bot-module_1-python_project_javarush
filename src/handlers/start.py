from telegram import Update
from telegram.ext import ContextTypes
from src.settings.utils import load_messages_for_bot


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_messages_for_bot("main")
    if not text or text.startswith("Файл") or text.startswith("Помилка"):
        text = "Файл resources/main.txt не найден или не читается."
    await update.message.reply_text(text)
