from test.test_cases import (GET_DATE_CASES, GET_DATE_INVALID_CASES, MASK_ACCOUNT_CARD_CASES,
                             MASK_ACCOUNT_CARD_INVALID_CASES)

import pytest

from src.widget import get_date, get_date_withoutiso, mask_account_card


@pytest.mark.parametrize("card_info, expected", MASK_ACCOUNT_CARD_CASES)
def test_mask_account_card(card_info: str, expected: str) -> None:
    assert mask_account_card(card_info) == expected


@pytest.mark.parametrize("card_info", MASK_ACCOUNT_CARD_INVALID_CASES)
def test_mask_account_card_invalid(card_info: str) -> None:
    assert mask_account_card(card_info) == "Invalid input"


def test_mask_account_card_invalid_card_number() -> None:
    assert mask_account_card("Visa 1234") == "Visa Invalid card number"


def test_mask_account_card_invalid_account_number() -> None:
    assert mask_account_card("Счет 123") == "Счет Invalid account number"


@pytest.mark.parametrize("date_input, expected", GET_DATE_CASES)
def test_get_date(date_input: str, expected: str) -> None:
    assert get_date(date_input) == expected


@pytest.mark.parametrize("date_input", GET_DATE_INVALID_CASES)
def test_get_date_invalid(date_input: str) -> None:
    with pytest.raises(ValueError):
        get_date(date_input)


def test_get_date_withoutiso() -> None:
    assert get_date_withoutiso("2024-03-11T02:26:18") == "11.03.2024"
