from pathlib import Path

import pandas as pd

from src.file_reader import read_csv_file, read_xlsx_file


def test_read_csv_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"

    csv_file.write_text(
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;"
        "Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации\n"
        "3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;"
        "Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту\n"
        "593027;CANCELED;2023-07-22T05:02:01Z;30368;Shilling;TZS;"
        "Visa 1959232722494097;Visa 6804119550473710;Перевод с карты на карту\n",
        encoding="utf-8",
    )

    result = read_csv_file(str(csv_file))

    assert result == [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": "29740",
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
        {
            "id": "593027",
            "state": "CANCELED",
            "date": "2023-07-22T05:02:01Z",
            "amount": "30368",
            "currency_name": "Shilling",
            "currency_code": "TZS",
            "from": "Visa 1959232722494097",
            "to": "Visa 6804119550473710",
            "description": "Перевод с карты на карту",
        },
    ]


def test_read_xlsx_file(tmp_path: Path) -> None:
    excel_file = tmp_path / "test.xlsx"

    data = pd.DataFrame(
        [
            {
                "id": 650703,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
            {
                "id": 3598919,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            },
            {
                "id": 593027,
                "state": "CANCELED",
                "date": "2023-07-22T05:02:01Z",
                "amount": 30368,
                "currency_name": "Shilling",
                "currency_code": "TZS",
                "from": "Visa 1959232722494097",
                "to": "Visa 6804119550473710",
                "description": "Перевод с карты на карту",
            },
        ]
    )

    data.to_excel(excel_file, index=False)

    result = read_xlsx_file(str(excel_file))

    assert result == [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 593027,
            "state": "CANCELED",
            "date": "2023-07-22T05:02:01Z",
            "amount": 30368,
            "currency_name": "Shilling",
            "currency_code": "TZS",
            "from": "Visa 1959232722494097",
            "to": "Visa 6804119550473710",
            "description": "Перевод с карты на карту",
        },
    ]
