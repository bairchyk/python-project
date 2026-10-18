from unittest.mock import Mock, patch

import pytest

from src.external_api import API_URL, transaction_amount


def test_transaction_amount_rub() -> None:
    """Проверяет возврат суммы операции в рублях."""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "code": "RUB",
            },
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = transaction_amount(transaction)

    assert result == 1000.50
    assert isinstance(result, float)
    mock_get.assert_not_called()


@pytest.mark.parametrize(
    "currency",
    ["USD", "EUR"],
)
def test_transaction_amount_foreign_currency(currency: str) -> None:
    """Проверяет конвертацию USD и EUR в рубли через API."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": currency,
            },
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {
        "result": 8500.25,
    }

    with patch(
        "src.external_api.os.getenv",
        return_value="test_api_key",
    ):
        with patch(
            "src.external_api.requests.get",
            return_value=mock_response,
        ) as mock_get:
            result = transaction_amount(transaction)

    assert result == 8500.25
    assert isinstance(result, float)

    mock_get.assert_called_once_with(
        API_URL,
        headers={"apikey": "test_api_key"},
        params={
            "amount": 100.0,
            "from": currency,
            "to": "RUB",
        },
        timeout=10,
    )

    mock_response.raise_for_status.assert_called_once_with()


def test_transaction_amount_unsupported_currency() -> None:
    """Проверяет обработку неподдерживаемой валюты."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "GBP",
            },
        }
    }

    with pytest.raises(ValueError):
        transaction_amount(transaction)
