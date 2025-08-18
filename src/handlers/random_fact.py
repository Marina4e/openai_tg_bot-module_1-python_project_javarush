from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.open_api.client import OpenAiClient
from src.settings.utils import load_messages_for_bot
from src.settings.config import PATH_TO_RESOURCES
import logging

logger = logging.getLogger(__name__)
client = OpenAiClient()


def _keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Хочу ще факт", callback_data="more_fact")],
            [InlineKeyboardButton("Закінчити", callback_data="end")],
        ]
    )


async def _send_random_fact(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет картинку + новый факт в чат `chat_id`."""
    # Картинка (без завала, если файла нет)
    try:
        with open(PATH_TO_RESOURCES / "images" / "random.png", "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
    except Exception as e:
        logger.warning("Не удалось отправить random.png: %s", e)

    # Промпт
    prompt = load_messages_for_bot("random")
    if not prompt or prompt.startswith(("Файл", "Помилка")):
        prompt = "Give me one short surprising fun fact."

    answer = None
    try:
        answer = await client.ask(prompt)
    except Exception as e:
        logger.error("OpenAI error in random_fact: %s", e)

    if not answer:
        answer = "Факт: У равликів є до 14 000 зубів. 🐌"

    await context.bot.send_message(chat_id=chat_id, text=answer, reply_markup=_keyboard())


# ===== Handlers =====

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /random."""
    chat_id = update.effective_chat.id
    await _send_random_fact(chat_id, context)


async def random_fact_more_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Кнопка 'Хочу ще факт'."""
    q = update.callback_query
    await q.answer()
    # Убираем старую клавиатуру, чтобы не кликали повторно
    try:
        await q.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass
    chat_id = update.effective_chat.id
    await _send_random_fact(chat_id, context)


async def random_fact_end_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Кнопка 'Закінчити' — (/start)."""
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
