from pathlib import Path
from typing import Any

from src.file_reader import read_csv_file, read_xlsx_file
from src.processing import filter_by_state, sort_by_date
from src.search import search_transactions
from src.utils import read_json_file
from src.widget import get_date, mask_account_card

BASE_DIR = Path(__file__).resolve().parent

JSON_PATH = BASE_DIR / "data" / "operations.json"
CSV_PATH = BASE_DIR / "transactions.csv"
XLSX_PATH = BASE_DIR / "transactions_excel.xlsx"

FILE_NAMES = {
    "1": "JSON",
    "2": "CSV",
    "3": "XLSX",
}

VALID_STATES = (
    "EXECUTED",
    "CANCELED",
    "PENDING",
)


def load_transactions(file_type: str) -> list[dict]:
    """Загружает транзакции из выбранного файла."""
    if file_type == "1":
        return read_json_file(str(JSON_PATH))

    if file_type == "2":
        return read_csv_file(str(CSV_PATH))

    if file_type == "3":
        return read_xlsx_file(str(XLSX_PATH))

    return []


def get_currency_code(transaction: dict[str, Any]) -> str:
    """Возвращает код валюты транзакции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})

        if isinstance(currency, dict):
            return str(currency.get("code", ""))

    return str(transaction.get("currency_code", ""))


def get_amount(transaction: dict[str, Any]) -> str:
    """Возвращает сумму транзакции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        return str(operation_amount.get("amount", ""))

    return str(transaction.get("amount", ""))


def ask_yes_no(question: str) -> bool:
    """Получает от пользователя ответ Да или Нет."""
    while True:
        answer = input(question).strip().lower()

        if answer in ("да", "д"):
            return True

        if answer in ("нет", "н"):
            return False

        print("Введите 'Да' или 'Нет'.")


def show_main_menu() -> None:
    """Выводит главное меню программы."""
    print("Привет! Добро пожаловать в программу " "работы с банковскими транзакциями.")
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")


def get_file_type() -> str:
    """Получает от пользователя тип файла."""
    while True:
        file_type = input("\nВаш выбор: ").strip()

        if file_type in FILE_NAMES:
            return file_type

        print("Введите 1, 2 или 3.")


def get_state() -> str:
    """Получает от пользователя статус операции."""
    while True:
        state = input("\nВведите статус операции " "(EXECUTED, CANCELED, PENDING): ").strip().upper()

        if state in VALID_STATES:
            return state

        print(f"Статус операции '{state}' недоступен.")


def remove_transactions_without_state(
    transactions: list[dict],
) -> list[dict]:
    """Удаляет операции, у которых отсутствует поле state."""
    return [transaction for transaction in transactions if "state" in transaction]


def filter_transactions_by_state(
    transactions: list[dict],
) -> list[dict]:
    """Запрашивает статус и фильтрует транзакции."""
    state = get_state()

    valid_transactions = remove_transactions_without_state(transactions)

    return filter_by_state(
        valid_transactions,
        state,
    )


def get_sort_order() -> bool:
    """Определяет направление сортировки по дате."""
    while True:
        order = input("По возрастанию или по убыванию? ").strip().lower()

        if order in (
            "по возрастанию",
            "возрастанию",
            "возрастание",
        ):
            return False

        if order in (
            "по убыванию",
            "убыванию",
            "убывание",
        ):
            return True

        print("Введите 'по возрастанию' " "или 'по убыванию'.")


def sort_transactions(
    transactions: list[dict],
) -> list[dict]:
    """При необходимости сортирует операции по дате."""
    should_sort = ask_yes_no("\nОтсортировать операции по дате? Да/Нет: ")

    if not should_sort:
        return transactions

    descending = get_sort_order()

    return sort_by_date(
        transactions,
        descending=descending,
    )


def filter_rub_transactions(
    transactions: list[dict],
) -> list[dict]:
    """При необходимости оставляет только операции в рублях."""
    rub_only = ask_yes_no("\nВыводить только рублевые транзакции? Да/Нет: ")

    if not rub_only:
        return transactions

    return [transaction for transaction in transactions if get_currency_code(transaction) == "RUB"]


def filter_transactions_by_description(
    transactions: list[dict],
) -> list[dict]:
    """При необходимости выполняет поиск по описанию."""
    should_search = ask_yes_no("\nОтфильтровать транзакции " "по слову в описании? Да/Нет: ")

    if not should_search:
        return transactions

    search_string = input("Введите строку для поиска: ").strip()

    return search_transactions(
        transactions,
        search_string,
    )


def print_transaction(
    transaction: dict[str, Any],
) -> None:
    """Выводит информацию об одной транзакции."""
    date = str(transaction.get("date", ""))
    description = str(transaction.get("description", ""))

    sender = str(transaction.get("from", ""))
    recipient = str(transaction.get("to", ""))

    amount = get_amount(transaction)
    currency = get_currency_code(transaction)

    print(f"{get_date(date)} {description}")

    if sender:
        print(f"{mask_account_card(sender)} -> " f"{mask_account_card(recipient)}")
    else:
        print(mask_account_card(recipient))

    print(f"Сумма: {amount} {currency}")
    print()


def print_transactions(
    transactions: list[dict],
) -> None:
    """Выводит итоговый список транзакций."""
    print("\nРаспечатываю итоговый список транзакций...")

    if not transactions:
        print("Не найдено ни одной транзакции, " "подходящей под условия.")
        return

    print(f"\nВсего банковских операций " f"в выборке: {len(transactions)}\n")

    for transaction in transactions:
        print_transaction(transaction)


def main() -> None:
    """Запускает основную логику программы."""
    show_main_menu()

    file_type = get_file_type()
    transactions = load_transactions(file_type)

    print(f"\nДля обработки выбран " f"{FILE_NAMES[file_type]}-файл.")

    if not transactions:
        print("В файле нет транзакций.")
        return

    transactions = filter_transactions_by_state(transactions)

    transactions = sort_transactions(transactions)

    transactions = filter_rub_transactions(transactions)

    transactions = filter_transactions_by_description(transactions)

    print_transactions(transactions)


if __name__ == "__main__":
    main()
