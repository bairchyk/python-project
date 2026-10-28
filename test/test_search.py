from src.search import count_transactions_by_category, search_transactions


def test_search_transactions_finds_matching_descriptions() -> None:
    transactions = [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2", "description": "Открытие вклада"},
        {"id": "3", "description": "Перевод с карты на карту"},
    ]

    result = search_transactions(transactions, "Перевод")

    assert result == [transactions[0], transactions[2]]


def test_search_transactions_is_case_insensitive() -> None:
    transactions = [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2", "description": "Открытие вклада"},
    ]

    result = search_transactions(transactions, "ПЕРЕВОД")

    assert result == [transactions[0]]


def test_search_transactions_returns_empty_list_when_nothing_found() -> None:
    transactions = [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2", "description": "Открытие вклада"},
    ]

    result = search_transactions(transactions, "Покупка")

    assert result == []


def test_search_transactions_ignores_transaction_without_description() -> None:
    transactions = [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2"},
    ]

    result = search_transactions(transactions, "Перевод")

    assert result == [transactions[0]]


def test_search_transactions_treats_special_characters_as_text() -> None:
    transactions = [
        {"id": "1", "description": "Комиссия 1.5%"},
        {"id": "2", "description": "Комиссия 15%"},
    ]

    result = search_transactions(transactions, "1.5%")

    assert result == [transactions[0]]


def test_count_transactions_by_category() -> None:
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
    ]
    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод с карты на карту",
    ]

    result = count_transactions_by_category(transactions, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Перевод с карты на карту": 1,
    }


def test_count_transactions_by_category_includes_zero_for_missing_category() -> None:
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    categories = [
        "Перевод организации",
        "Оплата мобильной связи",
    ]

    result = count_transactions_by_category(transactions, categories)

    assert result == {
        "Перевод организации": 1,
        "Оплата мобильной связи": 0,
    }


def test_count_transactions_by_category_ignores_other_categories() -> None:
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]

    result = count_transactions_by_category(
        transactions,
        ["Открытие вклада"],
    )

    assert result == {"Открытие вклада": 1}


def test_count_transactions_by_category_with_empty_transactions() -> None:
    result = count_transactions_by_category(
        [],
        ["Перевод организации", "Открытие вклада"],
    )

    assert result == {
        "Перевод организации": 0,
        "Открытие вклада": 0,
    }
