from src.settings.config import PATH_TO_RESOURCES


def load_messages_for_bot(name: str) -> str:
    file_path = PATH_TO_RESOURCES / f"{name}.txt"
    try:
        with file_path.open(encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Файл {file_path} не найден."
    except Exception as e:
        return f"Помилка читання {file_path}: {e}"
