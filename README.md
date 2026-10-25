# Проект

## Описание

Проект содержит функции для обработки банковских операций.

В проекте реализованы:

- маскирование номеров банковских карт и счетов;
- фильтрация и сортировка операций;
- генераторы для работы с банковскими транзакциями;
- декоратор для логирования работы функций;
- чтение банковских операций из JSON-файла;
- чтение финансовых операций из CSV- и Excel-файлов;
- получение суммы транзакции в рублях;
- конвертация USD и EUR в RUB через Exchange Rates Data API;
- тестирование функциональности с использованием `pytest`, `Mock` и `patch`.

Данные банковских операций могут храниться в JSON-, CSV- и Excel-файлах. Для работы с CSV и Excel используется модуль `src.file_reader`.

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

## Настройка переменных окружения

Для работы функции конвертации валют необходим API-ключ сервиса Exchange Rates Data API.

Создайте в корне проекта файл `.env` и добавьте в него переменную:

```env
EXCHANGE_RATES_API_KEY=ваш_api_ключ
```

Файл `.env` добавлен в `.gitignore` и не должен попадать в репозиторий.

В проекте также используется файл `.env.example`, содержащий шаблон необходимых переменных окружения без секретных значений:

```env
EXCHANGE_RATES_API_KEY=
```

## Структура проекта

```text
python-project/
├── data/
│   └── operations.json
├── src/
│   ├── decorators.py
│   ├── external_api.py
│   ├── file_reader.py
│   ├── generators.py
│   ├── masks.py
│   ├── processing.py
│   ├── utils.py
│   └── widget.py
├── test/
│   ├── test_decorators.py
│   ├── test_external_api.py
│   ├── test_file_reader.py
│   ├── test_generators.py
│   ├── test_masks.py
│   ├── test_processing.py
│   ├── test_utils.py
│   └── test_widget.py
├── transactions.csv
├── transactions_excel.xlsx
├── .env.example
├── pyproject.toml
└── poetry.lock
```

## Чтение операций из JSON

Модуль `src.utils` содержит функцию `read_json_file`, которая принимает путь к JSON-файлу и возвращает список словарей с банковскими операциями.

Если файл отсутствует, пустой, содержит некорректный JSON или содержит данные не в виде списка, функция возвращает пустой список.

Пример использования:

```python
from src.utils import read_json_file

transactions = read_json_file("data/operations.json")

print(transactions[0])
```


## Чтение операций из CSV и Excel

Модуль `src.file_reader` содержит функции для считывания финансовых операций из CSV- и Excel-файлов. Обе функции принимают путь к файлу в качестве аргумента и возвращают список словарей с транзакциями.

### Функция `read_csv_file`

Функция `read_csv_file` считывает финансовые операции из CSV-файла. Для разбора строк используется `csv.DictReader`, поэтому каждая операция представлена словарем.

Пример использования:

```python
from src.file_reader import read_csv_file

transactions = read_csv_file("transactions.csv")

print(transactions[0])
```

### Функция `read_xlsx_file`

Функция `read_xlsx_file` считывает финансовые операции из Excel-файла с помощью библиотеки `pandas` и преобразует данные в список словарей.

Пример использования:

```python
from src.file_reader import read_xlsx_file

transactions = read_xlsx_file("transactions_excel.xlsx")

print(transactions[0])
```

## Конвертация валют

Модуль `src.external_api` содержит функцию `transaction_amount`, которая принимает словарь с данными о транзакции и возвращает сумму операции в рублях в виде `float`.

Для операций в RUB сумма возвращается без обращения к внешнему API.

Для операций в USD и EUR выполняется запрос к Exchange Rates Data API для конвертации суммы в рубли.

Пример использования:

```python
from src.external_api import transaction_amount

transaction = {
    "operationAmount": {
        "amount": "10",
        "currency": {
            "code": "USD",
        },
    }
}

amount_in_rubles = transaction_amount(transaction)

print(amount_in_rubles)
```

## Модуль `generators`

Модуль `generators` содержит функции-генераторы для обработки банковских транзакций.

### Функция `filter_by_currency`

Функция `filter_by_currency` принимает список словарей с транзакциями и код валюты.

Функция возвращает итератор, который поочередно выдает транзакции с указанной валютой.

Пример использования:

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")

for _ in range(2):
    print(next(usd_transactions))
```

### Функция `transaction_descriptions`

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

### Функция `card_number_generator`

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

## Декоратор `log`

В проекте реализован модуль `decorators`, содержащий декоратор `log` для логирования выполнения функций.

Декоратор позволяет отслеживать:

- начало выполнения функции;
- успешное завершение функции;
- результат выполнения;
- возникшие исключения;
- входные позиционные и именованные аргументы функции;
- окончание выполнения функции.

Если параметр `filename` не указан, сообщения выводятся в консоль.

Если параметр `filename` указан, сообщения записываются в соответствующий файл.

Пример использования:

```python
from src.decorators import log


@log(filename="mylog.txt")
def add(x: int, y: int) -> int:
    return x + y


add(1, 2)
```

Пример успешного лога:

```text
add started
add ok
add result: 3
add finished
```

При возникновении исключения в лог записывается тип ошибки и входные параметры функции:

```text
add error: TypeError. Inputs: (1, '2'), {}
```

## Тестирование

Для тестирования проекта используется библиотека `pytest`.

Запуск всех тестов:

```bash
poetry run pytest
```

Для проверки покрытия кода тестами используется `pytest-cov`:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Для создания HTML-отчета покрытия:

```bash
poetry run pytest --cov=src --cov-report=html
```

HTML-отчет создается в директории:

```text
htmlcov/
```

Директория `htmlcov/` добавлена в `.gitignore` и не должна попадать в репозиторий.

Тесты для чтения JSON-файла и конвертации валют используют `Mock` и `patch`, поэтому не зависят от реального файла, доступности внешнего API и действующего API-ключа.

## Проверка качества кода

В проекте используются следующие инструменты:

- Black — форматирование кода;
- isort — сортировка импортов;
- Flake8 — проверка соответствия PEP 8;
- mypy — статическая проверка типов.

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

## Документация

Дополнительную информацию по проекту можно получить по электронной почте: [brakshaev7@bk.ru](mailto:brakshaev7@bk.ru).

## Лицензия

Проект распространяется под лицензией MIT.