from pathlib import Path
import os
from dotenv import load_dotenv

# Путь к .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Загружаем .env
load_dotenv(ENV_PATH)

# Папка с ресурсами
PATH_TO_RESOURCES = BASE_DIR / "src" / "resources"

# Ключи из окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TG_BOT_API_KEY = os.getenv("TG_BOT_API_KEY")

# Проверка, чтобы не запускать проект без ключей
if OPENAI_API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY не найден в окружении. Проверь файл .env")

if TG_BOT_API_KEY is None:
    raise RuntimeError("TG_BOT_API_KEY не найден в окружении. Проверь файл .env")
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("telegram_bot")
