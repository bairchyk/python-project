card_info = input()


def get_mask_card_number(card_number: str) -> str:
    #Функция маскирует номер банковской карты.
    if len(card_number) != 16:
        return "Invalid card number"

    masked_card = card_number[:6] + "******" + card_number[12:]

    return (
        masked_card[:4]
        + " "
        + masked_card[4:8]
        + " "
        + masked_card[8:12]
        + " "
        + masked_card[12:]
    )


def get_mask_account(account_number: str) -> str:
    #Функция маскирует номер банковского счета.
    if len(account_number) < 4:
        return "Invalid account number"

    return "**" + account_number[-4:]


def mask_account_card(card_info: str) -> str:
    #Функция маскирует номер карты или счета в зависимости от типа.
    name, number = card_info.rsplit(" ", 1)

    if name == "Счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return name + " " + masked_number


print(mask_account_card(card_info))


date_input = input()


def get_date(date_input: str) -> str:
    #Функция преобразует дату в формат ДД.ММ.ГГГГ.
    date_separated = date_input.split("-")

    return (
        date_separated[2][:2]
        + "."
        + date_separated[1]
        + "."
        + date_separated[0]
    )


print(get_date(date_input))