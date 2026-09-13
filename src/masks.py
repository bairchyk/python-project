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
