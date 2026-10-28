import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_mask_card_number() -> None:
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_mask_card_number_short() -> None:
    assert get_mask_card_number("1234") == "Invalid card number"


def test_mask_card_number_long() -> None:
    assert get_mask_card_number("12345678901234567") == "Invalid card number"


def test_mask_card_number_empty() -> None:
    assert get_mask_card_number("") == "Invalid card number"


def test_mask_card_number_with_spaces() -> None:
    assert get_mask_card_number("7000 7922 8960 6361") == "Invalid card number"


def test_mask_card_number_wrong_type() -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(7000792289606361)  # type: ignore[arg-type]


def test_mask_account() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"


def test_mask_account_short() -> None:
    assert get_mask_account("123") == "Invalid account number"


def test_mask_account_empty() -> None:
    assert get_mask_account("") == "Invalid account number"


def test_mask_account_four_digits() -> None:
    assert get_mask_account("1234") == "**1234"


def test_mask_account_different_length() -> None:
    assert get_mask_account("123456789") == "**6789"


def test_mask_account_wrong_type() -> None:
    with pytest.raises(TypeError):
        get_mask_account(123)  # type: ignore[arg-type]
