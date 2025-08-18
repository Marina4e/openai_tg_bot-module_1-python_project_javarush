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

logger = logging.getLogger(__name__)
client = OpenAiClient()

# --- Стани ---
CHOOSING, TALKING = range(2)

PERSONS = {
    "ukrainka": {
        "name": "Леся Українка",
        "photo": PATH_TO_RESOURCES / "images" / "L_ukrainka.png",
        "prompt": PATH_TO_RESOURCES / "prompts" / "talk_ukrainka.txt",
    },
    "curie": {
        "name": "Марія Кюрі",
        "photo": PATH_TO_RESOURCES / "images" / "M_curie.png",
        "prompt": PATH_TO_RESOURCES / "prompts" / "talk_curie.txt",
    },
    "tesla": {
        "name": "Нікола Тесла",
        "photo": PATH_TO_RESOURCES / "images" / "N_tesla.png",
        "prompt": PATH_TO_RESOURCES / "prompts" / "talk_tesla.txt",
    },
}


def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Помилка читання {path}: {e}")
        return ""


def _talk_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Ставити питання", callback_data="ask_person")],
        [InlineKeyboardButton("❌ Закінчити", callback_data="end_talk")],
    ])


# --- Команда /talk ---
async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускаем вибір персонажа"""
    text = load_file(PATH_TO_RESOURCES / "messages" / "talk.txt")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📖 Леся Українка", callback_data="choose_ukrainka"),
            InlineKeyboardButton("🧠 Марія Кюрі", callback_data="choose_curie"),
        ],
        [InlineKeyboardButton("🔬 Нікола Тесла", callback_data="choose_tesla")],
    ])
    try:
        with open(PATH_TO_RESOURCES / "images" / "talk.png", "rb") as photo:
            await update.message.reply_photo(photo, caption=text, reply_markup=keyboard)
    except Exception as e:
        logger.warning("Не вдалося відправити talk.png: %s", e)
        await update.message.reply_text(text, reply_markup=keyboard)

    return CHOOSING


async def choose_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    person_key = query.data.replace("choose_", "")
    person = PERSONS[person_key]

    prompt_text = load_file(person["prompt"])
    context.user_data["talk_prompt"] = prompt_text
    context.user_data["talk_person"] = person_key

    with open(person["photo"], "rb") as photo:
        await query.message.reply_photo(
            photo,
            caption=f"Ви обрали: *{person['name']}*.\n\nОбери дію нижче 👇",
            parse_mode="Markdown",
            reply_markup=_talk_keyboard(),
        )

    return TALKING


async def ask_person_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✍️ Напиши своє питання для обраної особистості:")
    return TALKING


async def talk_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    system_prompt = context.user_data.get("talk_prompt", "")

    reply = await client.ask(user_text, system_prompt=system_prompt)

    await update.message.reply_text(
        reply,
        reply_markup=_talk_keyboard(),
    )
    return TALKING


async def talk_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    from src.handlers.start import start

    context.user_data.pop("talk_prompt", None)
    context.user_data.pop("talk_person", None)

    await start(update, context)
    return ConversationHandler.END


talk_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("talk", talk_start),
        CallbackQueryHandler(talk_start, pattern="^talk_start$"),
    ],
    states={
        CHOOSING: [CallbackQueryHandler(choose_person, pattern="^choose_")],
        TALKING: [
            CallbackQueryHandler(ask_person_callback, pattern="^ask_person$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, talk_message),
            CallbackQueryHandler(talk_end, pattern="^end_talk$"),
        ],
    },
    fallbacks=[CallbackQueryHandler(talk_end, pattern="^end_talk$")],
)
