import re
from collections import Counter


def search_transactions(transactions: list[dict], search_string: str) -> list[dict]:
    """Возвращает транзакции, в описании которых найдена заданная строка."""
    result = []

    for transaction in transactions:
        description = transaction.get("description", "")

        if re.search(search_string, description, flags=re.IGNORECASE):
            result.append(transaction)

    return result


def count_transactions_by_category(transactions: list[dict], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    descriptions = [
        transaction.get("description", "")
        for transaction in transactions
        if transaction.get("description", "") in categories
    ]

    counter = Counter(descriptions)

    return {category: counter[category] for category in categories}
