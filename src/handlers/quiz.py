import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from src.open_api.client import OpenAiClient
from src.settings.config import PATH_TO_RESOURCES
from src.settings.utils import load_messages_for_bot

logger = logging.getLogger(__name__)
client = OpenAiClient()

# --- Стан ---
CHOOSING_TOPIC, ASKING_QUESTION, ANSWERING = range(3)

# --- Теми квізу ---
QUIZ_TOPICS = {
    "quiz_prog": "Програмування",
    "quiz_math": "Математика",
    "quiz_biology": "Біологія",
}


# --- Утиліта для файлів ---
def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.error(f"Помилка читання {path}: {e}")
        return ""


# Шлях до промпта
QUIZ_PROMPT_PATH = PATH_TO_RESOURCES / "prompts" / "quiz_prompt.txt"


def render_prompt(template: str, **values: str) -> str:
    """Підстановка тільки {question} та {user_answer}, не чіпаючи {answer} у тексті."""
    for k, v in values.items():
        template = template.replace("{" + k + "}", str(v))
    return template


# --- Клавіатури ---
def _topic_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐍 Програмування", callback_data="quiz_prog"),
            InlineKeyboardButton("📐 Математика", callback_data="quiz_math"),
        ],
        [InlineKeyboardButton("🧬 Біологія", callback_data="quiz_biology")],
        [InlineKeyboardButton("❌ Закінчити квіз", callback_data="quiz_end")],
    ])


def _quiz_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Ще питання", callback_data="quiz_more")],
        [InlineKeyboardButton("🔄 Змінити тему", callback_data="quiz_change")],
        [InlineKeyboardButton("❌ Закінчити квіз", callback_data="quiz_end")],
    ])


# --- Генерація питання через OpenAI ---
async def _generate_question(topic_key: str) -> str:
    sys_prompt = (
        "Ти створюєш дуже короткі й прості запитання українською мовою для квізу з теми "
        f"«{QUIZ_TOPICS.get(topic_key, 'Квіз')}». "
        "Питання має мати однозначну відповідь (бажано цифра або 1 слово). "
        "Лише саме питання, без пояснень."
    )
    question = await client.ask("Створи запитання", system_prompt=sys_prompt)
    return (question or "").strip()


# --- Обробники ---
async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    text = load_file(PATH_TO_RESOURCES / "messages" / "quiz.txt") or \
           "Ласкаво просимо до квізу! Оберіть тему нижче ⬇️"
    try:
        with open(PATH_TO_RESOURCES / "images" / "quiz.png", "rb") as photo:
            await update.effective_message.reply_photo(
                photo, caption=text, reply_markup=_topic_keyboard()
            )
    except Exception as e:
        logger.warning("Не вдалося надіслати quiz.png: %s", e)
        await update.effective_message.reply_text(text, reply_markup=_topic_keyboard())
    return CHOOSING_TOPIC


async def quiz_choose_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    topic_key = query.data
    context.user_data["quiz_topic"] = topic_key
    context.user_data["quiz_correct"] = 0

    question = await _generate_question(topic_key)
    context.user_data["quiz_question"] = question
    await query.message.reply_text(question)
    return ANSWERING


async def quiz_more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    topic_key = context.user_data.get("quiz_topic", "")
    if not topic_key:
        await query.message.reply_text("Будь ласка, обери тему:", reply_markup=_topic_keyboard())
        return CHOOSING_TOPIC

    question = await _generate_question(topic_key)
    context.user_data["quiz_question"] = question
    await query.message.reply_text(question)
    return ANSWERING


async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = (update.message.text or "").strip()
    question = context.user_data.get("quiz_question", "")

    # читаем шаблон из файла quiz_prompt.txt
    raw_prompt = load_file(QUIZ_PROMPT_PATH)
    if not raw_prompt:
        await update.message.reply_text("⚠️ Помилка: файл quiz_prompt.txt порожній або відсутній.")
        return CHOOSING_TOPIC

    sys_prompt = render_prompt(raw_prompt, question=question, user_answer=user_answer)

    result = (await client.ask("Перевір", system_prompt=sys_prompt) or "").strip()

    correct_count = context.user_data.get("quiz_correct", 0)

    if result.startswith("Правильно"):
        correct_count += 1
        context.user_data["quiz_correct"] = correct_count
        if correct_count >= 2:
            await update.message.reply_text("Правильно!\n\nВи виграли! Кінець квізу 🎉")
            main_text = load_messages_for_bot("main")
            await update.message.reply_text(main_text, parse_mode="Markdown")
            context.user_data.clear()
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                f"{result}\n\n✅ Правильних відповідей: {correct_count}",
                reply_markup=_quiz_keyboard()
            )
            return ASKING_QUESTION
    else:
        await update.message.reply_text(
            result,
            reply_markup=_topic_keyboard()
        )
        context.user_data.clear()
        return CHOOSING_TOPIC


async def quiz_change_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Обери нову тему:", reply_markup=_topic_keyboard())
    return CHOOSING_TOPIC


async def quiz_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    correct_count = context.user_data.get("quiz_correct", 0)
    await query.message.reply_text(f"Квіз завершено!\n\n✅ Правильних відповідей: {correct_count}")
    main_text = load_messages_for_bot("main")
    await query.message.reply_text(main_text, parse_mode="Markdown")
    context.user_data.clear()
    return ConversationHandler.END


# --- Хендлер квізу ---
quiz_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz_start)],
    states={
        CHOOSING_TOPIC: [
            CallbackQueryHandler(quiz_end, pattern="^quiz_end$"),
            CallbackQueryHandler(quiz_choose_topic, pattern=r"^quiz_(prog|math|biology)$"),
        ],
        ASKING_QUESTION: [
            CallbackQueryHandler(quiz_more, pattern="^quiz_more$"),
            CallbackQueryHandler(quiz_change_topic, pattern="^quiz_change$"),
            CallbackQueryHandler(quiz_end, pattern="^quiz_end$"),
        ],
        ANSWERING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_answer),
            CallbackQueryHandler(quiz_end, pattern="^quiz_end$"),
        ],
    },
    fallbacks=[CallbackQueryHandler(quiz_end, pattern="^quiz_end$")],
    allow_reentry=True,
)
