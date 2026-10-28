from typing import Any

import pytest

import main


def test_get_currency_code_from_json_transaction() -> None:
    transaction: dict[str, Any] = {
        "operationAmount": {
            "amount": "1000",
            "currency": {"code": "RUB"},
        }
    }

    assert main.get_currency_code(transaction) == "RUB"


def test_get_currency_code_from_csv_transaction() -> None:
    transaction: dict[str, Any] = {
        "amount": "1000",
        "currency_code": "USD",
    }

    assert main.get_currency_code(transaction) == "USD"


def test_get_amount_from_json_transaction() -> None:
    transaction: dict[str, Any] = {
        "operationAmount": {
            "amount": "1234.50",
            "currency": {"code": "RUB"},
        }
    }

    assert main.get_amount(transaction) == "1234.50"


def test_get_amount_from_csv_transaction() -> None:
    transaction: dict[str, Any] = {
        "amount": "5000",
        "currency_code": "RUB",
    }

    assert main.get_amount(transaction) == "5000"


def test_remove_transactions_without_state() -> None:
    transactions: list[dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},
        {"id": 3, "state": "CANCELED"},
    ]

    result = main.remove_transactions_without_state(transactions)

    assert result == [transactions[0], transactions[2]]


def test_get_file_type_returns_valid_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = iter(["7", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert main.get_file_type() == "2"


def test_get_state_converts_value_to_uppercase(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "executed")

    assert main.get_state() == "EXECUTED"


def test_ask_yes_no_returns_true(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "да")

    assert main.ask_yes_no("Вопрос: ") is True


def test_ask_yes_no_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")

    assert main.ask_yes_no("Вопрос: ") is False


def test_filter_rub_transactions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [
        {"currency_code": "RUB"},
        {"currency_code": "USD"},
        {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "RUB"},
            }
        },
    ]
    monkeypatch.setattr(main, "ask_yes_no", lambda _: True)

    result = main.filter_rub_transactions(transactions)

    assert result == [transactions[0], transactions[2]]


def test_filter_rub_transactions_returns_original_when_user_says_no(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [{"currency_code": "USD"}]
    monkeypatch.setattr(main, "ask_yes_no", lambda _: False)

    result = main.filter_rub_transactions(transactions)

    assert result == transactions


def test_filter_transactions_by_description(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    monkeypatch.setattr(main, "ask_yes_no", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: "организации")

    result = main.filter_transactions_by_description(transactions)

    assert result == [transactions[0]]


def test_filter_transactions_by_description_returns_original_when_no(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [{"description": "Открытие вклада"}]
    monkeypatch.setattr(main, "ask_yes_no", lambda _: False)

    result = main.filter_transactions_by_description(transactions)

    assert result == transactions


def test_sort_transactions_returns_original_when_user_says_no(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [
        {"date": "2023-01-01T00:00:00Z"},
        {"date": "2022-01-01T00:00:00Z"},
    ]
    monkeypatch.setattr(main, "ask_yes_no", lambda _: False)

    result = main.sort_transactions(transactions)

    assert result == transactions


def test_sort_transactions_calls_sort_by_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transactions: list[dict[str, Any]] = [
        {"id": 1},
        {"id": 2},
    ]
    expected: list[dict[str, Any]] = [
        {"id": 2},
        {"id": 1},
    ]

    monkeypatch.setattr(main, "ask_yes_no", lambda _: True)
    monkeypatch.setattr(main, "get_sort_order", lambda: True)
    monkeypatch.setattr(
        main,
        "sort_by_date",
        lambda operations, descending: expected,
    )

    result = main.sort_transactions(transactions)

    assert result == expected


def test_load_transactions_uses_csv_reader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected: list[dict[str, Any]] = [{"id": "1"}]
    monkeypatch.setattr(main, "read_csv_file", lambda _: expected)

    result = main.load_transactions("2")

    assert result == expected


def test_load_transactions_returns_empty_list_for_unknown_type() -> None:
    assert main.load_transactions("99") == []
