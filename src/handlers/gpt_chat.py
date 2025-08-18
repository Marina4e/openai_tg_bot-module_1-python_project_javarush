from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from src.open_api.client import OpenAiClient
from src.settings.config import PATH_TO_RESOURCES
from src.settings.utils import load_messages_for_bot
import logging

logger = logging.getLogger(__name__)
client = OpenAiClient()

ASKING = 1


def _chat_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для GPT-чата"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Напиши питання", callback_data="ask_gpt")],
        [InlineKeyboardButton("❌ Закінчити чат", callback_data="end_gpt")],
    ])


async def start_gpt_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт GPT-чата командою /gpt"""
    caption = "Обери дію нижче 👇"

    try:
        with open(PATH_TO_RESOURCES / "images" / "gpt.png", "rb") as photo:
            await update.message.reply_photo(
                photo, caption=caption, reply_markup=_chat_keyboard()
            )
    except Exception as e:
        logger.warning("Не вдалося відправити gpt.png: %s", e)
        await update.message.reply_text(caption, reply_markup=_chat_keyboard())

    return ASKING


async def ask_gpt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Реакция на кнопку 'Напиши питання'"""
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✍️ Напиши своє питання ChatGPT у чаті нижче:")
    return ASKING


async def handle_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відповіді ChatGPT на повідомлення користувача"""
    user_text = update.message.text

    try:
        reply = await client.ask(user_text)
    except Exception as e:
        logger.error("OpenAI error: %s", e)
        reply = "Вибач, зараз я не можу відповісти."

    await update.message.reply_text(reply, reply_markup=_chat_keyboard())
    return ASKING


async def end_gpt_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершення GPT-чата командою /end"""
    text = load_messages_for_bot("main")
    if not text or text.startswith("Файл"):
        text = "Привіт! (файл resources/main.txt не знайдено або не прочитався)"
    await update.message.reply_text(text)
    return ConversationHandler.END


async def end_gpt_chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершення GPT-чата кнопкою 'Закінчити чат'"""
    q = update.callback_query
    await q.answer()

    try:
        await q.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    chat_id = update.effective_chat.id
    text = load_messages_for_bot("main")
    if not text or text.startswith("Файл"):
        text = "Привіт! (файл resources/main.txt не знайдено або не прочитався)"
    await context.bot.send_message(chat_id=chat_id, text=text)
    return ConversationHandler.END


# --- ConversationHandler для GPT-чата ---
gpt_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("gpt", start_gpt_chat)],  # запуск /gpt
    states={
        ASKING: [
            CallbackQueryHandler(ask_gpt_callback, pattern="^ask_gpt$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gpt_message),
        ],
    },
    fallbacks=[CommandHandler("end", end_gpt_chat)],
)
