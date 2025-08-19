from pathlib import Path
import os
from dotenv import load_dotenv

# Шлях до .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Загрузка .env
load_dotenv(ENV_PATH)

# Папка з ресурсами
PATH_TO_RESOURCES = BASE_DIR / "src" / "resources"

# Ключі з оточення
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TG_BOT_API_KEY = os.getenv("TG_BOT_API_KEY")

# Перевірка, щоб не запускати проект без ключів
if OPENAI_API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY не знайдено в оточенні. Перевір файл .env")

if TG_BOT_API_KEY is None:
    raise RuntimeError("TG_BOT_API_KEY не знайдено в оточенні. Перевір файл .env")
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("telegram_bot")
