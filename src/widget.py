from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Функция маскирует номер карты или счета в зависимости от типа."""

    if not card_info.strip():
        return "Invalid input"

    parts = card_info.rsplit(" ", 1)

    if len(parts) != 2:
        return "Invalid input"

    name, number = parts

    if name == "Счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return str(name + " " + masked_number)


def get_date_withoutiso(date_input: str) -> str:
    """Функция преобразует дату в формат ДД.ММ.ГГГГ. через split"""
    date_separated = date_input.split("-")

    return date_separated[2][:2] + "." + date_separated[1] + "." + date_separated[0]


def get_date(date_input: str) -> str:
    """Функция преобразует дату в формат ДД.ММ.ГГГГ. для ISO формата"""
    date = datetime.fromisoformat(date_input)
    return date.strftime("%d.%m.%Y")


if __name__ == "__main__":
    card_info = input()
    print(mask_account_card(card_info))

    date_input = input()
    print(get_date(date_input))
