import logging
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram import BotCommand

from src.settings.config import TG_BOT_API_KEY
from src.handlers.start import start
from src.handlers.random_fact import (
    random_fact,
    random_fact_more_callback,
    random_fact_end_callback,
)
from src.handlers.gpt_chat import (
    gpt_conv_handler,
    end_gpt_chat_callback,
)
from src.handlers.talks import talk_conv_handler
from src.handlers.quiz import quiz_conv_handler
from src.handlers.resume import resume_conv_handler, end_resume_callback

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.exception("Unhandled exception while handling update:", exc_info=context.error)


# --- Установка меню команд ---
async def set_commands(app):
    commands = [
        BotCommand("start", "Головне меню бота"),
        BotCommand("random", "Дізнатись випадковий факт 🧠"),
        BotCommand("gpt", "Задати питання ChatGPT 🤖"),
        BotCommand("talk", "Поговорити з відомою особистістю 👤"),
        BotCommand("quiz", "Перевірити свої знання ❓"),
        BotCommand("resume", "Допомога з резюме ✍️"),
    ]
    await app.bot.set_my_commands(commands)


def main():
    app = ApplicationBuilder().token(TG_BOT_API_KEY).build()

    # --- Команди ---
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_fact))

    # --- Conversations ---
    app.add_handler(quiz_conv_handler, group=0)  # приоритет квиза
    app.add_handler(talk_conv_handler)
    app.add_handler(gpt_conv_handler, group=1)  # ниже приоритет GPT-чата
    app.add_handler(resume_conv_handler)

    # --- Callback-кнопки для RandomFact ---
    app.add_handler(CallbackQueryHandler(random_fact_more_callback, pattern="^more_fact$"))
    app.add_handler(CallbackQueryHandler(random_fact_end_callback, pattern="^end$"))

    # --- Callback-кнопка для GPT-чата ---
    app.add_handler(CallbackQueryHandler(end_gpt_chat_callback, pattern="^end_gpt$"))
    app.add_handler(CallbackQueryHandler(end_resume_callback, pattern="^resume_end$"))

    app.add_error_handler(error_handler)

    # --- Commands before start ---
    app.post_init = set_commands

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
