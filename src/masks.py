import logging

logger = logging.getLogger(__name__)


# Создаем хендлер для вывода в файл
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")

# Создаем форматер
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер банковской карты."""
    logger.info("Функция get_mask_card_number запущена")

    if len(card_number) != 16:
        logger.error("Некорректный номер карты: длина %s вместо 16", len(card_number))
        return "Invalid card number"

    masked_card = card_number[:6] + "******" + card_number[12:]
    logger.info("Операция маскирования карты выполнена успешно")
    return masked_card[:4] + " " + masked_card[4:8] + " " + masked_card[8:12] + " " + masked_card[12:]


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер банковского счета."""
    logger.info("Функция get_mask_account запущена")

    if len(account_number) < 4:
        logger.error(
            "Некорректный номер счета: длина %s",
            len(account_number),
        )
        return "Invalid account number"

    logger.info("Операция маскирования счета выполнена успешно")

    return "**" + account_number[-4:]
