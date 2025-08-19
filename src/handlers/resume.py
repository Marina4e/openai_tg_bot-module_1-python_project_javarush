from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.settings.config import PATH_TO_RESOURCES

ASK_EDUCATION, ASK_EXPERIENCE, ASK_SKILLS = range(3)


async def start_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = PATH_TO_RESOURCES / "images" / "resume.jpg"

    with open(image_path, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption="👋 Давайте створимо резюме!")

    await update.message.reply_text("✍️ Спершу розкажіть про вашу **освіту**:")
    return ASK_EDUCATION


async def ask_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["education"] = update.message.text
    await update.message.reply_text("📌 Чудово! Тепер розкажіть про ваш **досвід роботи**:")
    return ASK_EXPERIENCE


async def ask_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text
    await update.message.reply_text("💡 Добре! А тепер перерахуйте ваші **навички** (через кому):")
    return ASK_SKILLS


async def generate_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["skills"] = update.message.text

    education = context.user_data.get("education", "—")
    experience = context.user_data.get("experience", "—")
    skills = context.user_data.get("skills", "—")

    resume_text = (
        "📄 *Ваше резюме:*\n\n"
        f"*Освіта:* {education}\n"
        f"*Досвід роботи:* {experience}\n"
        f"*Навички:* {skills}\n\n"
        "✅ Ви можете скопіювати це та використати як шаблон для резюме."
    )

    # Кнопка завершення
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Головне меню", callback_data="resume_end")]
    ])

    await update.message.reply_text(resume_text, parse_mode="Markdown", reply_markup=keyboard)
    return ConversationHandler.END


async def end_resume_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Закінчити та повернутись у меню"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Резюме завершено. Введіть /start щоб повернутись у головне меню.")


# --- ConversationHandler ---
resume_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("resume", start_resume)],
    states={
        ASK_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_experience)],
        ASK_EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_skills)],
        ASK_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_resume)],
    },
    fallbacks=[],
)
