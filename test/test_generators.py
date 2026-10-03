from test.test_cases import (CARD_NUMBER_GENERATORS_CASES, FILTER_BY_CURRENCY_CASES,
                             FILTER_BY_CURRENCY_FIRST_TWO_CASES, TRANSACTION_DESCRIPTIONS_CASES)

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected_ids",
    FILTER_BY_CURRENCY_CASES,
)
def test_filter_by_currency(
    transactions: list[dict],
    currency: str,
    expected_ids: list[int],
) -> None:
    result = list(filter_by_currency(transactions, currency))

    result_ids = [transaction["id"] for transaction in result]

    assert result_ids == expected_ids


@pytest.mark.parametrize(
    "currency, expected_ids",
    FILTER_BY_CURRENCY_FIRST_TWO_CASES,
)
def test_filter_by_currency_first_two(
    transactions: list[dict],
    currency: str,
    expected_ids: list[int],
) -> None:
    filtered_transactions = filter_by_currency(transactions, currency)

    result_ids = [next(filtered_transactions)["id"] for m in range(2)]

    assert result_ids == expected_ids


@pytest.mark.parametrize(
    "description, expected_description",
    TRANSACTION_DESCRIPTIONS_CASES,
)
def test_transaction_descriptions(
    transactions: list[dict],
    description: str,
    expected_description: list[str],
) -> None:
    descriptions_transactions = transaction_descriptions(transactions)

    result_description = [next(descriptions_transactions) for m in range(5)]

    assert result_description == expected_description


@pytest.mark.parametrize(
    "card_number_start, card_number_end, expected_card_numbers",
    CARD_NUMBER_GENERATORS_CASES,
)
def test_card_number_generator(
    card_number_start: int,
    card_number_end: int,
    expected_card_numbers: list[str],
) -> None:

    result_card_number = list(card_number_generator(card_number_start, card_number_end))

    assert result_card_number == expected_card_numbers
