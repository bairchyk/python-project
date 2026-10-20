import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def transaction_amount(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    operation_amount = transaction["operationAmount"]

    amount = float(operation_amount["amount"])
    currency = operation_amount["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency in {"USD", "EUR"}:
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")

        headers = {"apikey": api_key or ""}

        params = {
            "amount": amount,
            "from": currency,
            "to": "RUB",
        }

        response = requests.get(
            API_URL,
            headers=headers,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        return float(data["result"])

    raise ValueError(f"Неподдерживаемая валюта: {currency}")
