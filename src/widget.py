def get_mask_card_number(card_number: str) -> str:
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        return "Invalid card number"
    masked_card = card_number_str[:6] + "******" + card_number_str[12:]

    return masked_card[:4] + " " + masked_card[4:8] + " " + masked_card[8:12] + " " + masked_card[12:]


def get_mask_account(card_number: str) -> str:
    card_number_str = str(card_number)
    if len(card_number_str) < 4:
        return "Invalid card number"
    return "**" + card_number_str[-4:]