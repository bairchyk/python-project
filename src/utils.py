import json
from typing import Any


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список финансовых транзакций."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
