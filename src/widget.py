from datetime import datetime


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер банковской карты."""
    if len(card_number) != 16:
        return "Invalid card number"

    masked_card = card_number[:6] + "******" + card_number[12:]

    return masked_card[:4] + " " + masked_card[4:8] + " " + masked_card[8:12] + " " + masked_card[12:]


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер банковского счета."""
    if len(account_number) < 4:
        return "Invalid account number"

    return "**" + account_number[-4:]


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
