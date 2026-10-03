# Проект

## Описание

Проект содержит функции для обработки банковских операций.

Реализованы функции для работы с номерами банковских карт и счетов, а также для фильтрации и сортировки операций.

Также реализован модуль `generators` для работы с генераторами банковских транзакций.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/bairchyk/python-project.git
```

2. Перейдите в директорию проекта:

```bash
cd python-project
```

3. Установите зависимости:

```bash
poetry install
```

## Использование

Для запуска проекта активируйте виртуальное окружение Poetry:

```bash
poetry shell
```

После этого можно запускать необходимые Python-файлы или тесты проекта.

## Модуль generators

Модуль `generators` содержит функции-генераторы для обработки банковских транзакций.

### Функция filter_by_currency

Функция `filter_by_currency` принимает список словарей с транзакциями и код валюты.

Функция возвращает итератор, который поочередно выдает транзакции с указанной валютой.

Пример использования:

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")

for _ in range(2):
    print(next(usd_transactions))
```

### Функция transaction_descriptions

Функция-генератор `transaction_descriptions` принимает список словарей с транзакциями и поочередно возвращает описание каждой операции.

Пример использования:

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)

for _ in range(5):
    print(next(descriptions))
```

Пример результата:

```text
Перевод организации
Перевод со счета на счет
Перевод со счета на счет
Перевод с карты на карту
Перевод организации
```

### Функция card_number_generator

Функция-генератор `card_number_generator` генерирует номера банковских карт в заданном диапазоне.

Номера карт возвращаются в формате:

```text
XXXX XXXX XXXX XXXX
```

Пример использования:

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

Пример результата:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Проверка качества кода

В проекте используются инструменты:

* Black — форматирование кода;
* isort — сортировка импортов;
* Flake8 — проверка соответствия PEP 8;
* mypy — проверка аннотаций типов.

Запуск Black:

```bash
poetry run black src test
```

Запуск isort:

```bash
poetry run isort src test
```

Проверка Flake8:

```bash
poetry run flake8 src test
```

Проверка mypy:

```bash
poetry run mypy src
```

## Тестирование

Для тестирования проекта используется библиотека pytest.

Запуск всех тестов:

```bash
poetry run pytest
```

Для проверки покрытия кода тестами используется pytest-cov.

Запуск тестов с проверкой покрытия:

```bash
poetry run pytest --cov=src
```

Для создания отчета покрытия тестами в формате HTML:

```bash
poetry run pytest --cov=src --cov-report=html
```

HTML-отчет будет создан в папке:

```text
htmlcov
```

## Документация

Дополнительную информацию по проекту можно получить по электронной почте: [brakshaev7@bk.ru](mailto:brakshaev7@bk.ru).

## Лицензия

Проект распространяется под лицензией MIT.
