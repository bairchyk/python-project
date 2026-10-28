import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


# Создаем хендлер для вывода в файл
file_handler = logging.FileHandler(
    "logs/utils.log",
    mode="w",
    encoding="utf-8",
)

# Создаем форматер
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список финансовых транзакций."""
    logger.info("Функция read_json_file запущена")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info("Операция выполнена успешно")

        if isinstance(data, list):
            return data

        return []

    except (FileNotFoundError, json.JSONDecodeError) as error:
        logger.error("Ошибка чтения файла %s: %s", file_path, error)
        return []
