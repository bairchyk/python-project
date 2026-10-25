from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from src.file_reader import read_csv_file, read_xlsx_file


def test_read_csv_file() -> None:
    expected = [
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
    ]

    mock_reader = Mock(return_value=expected)

    with patch("builtins.open", mock_open()):
        with patch("src.file_reader.csv.DictReader", mock_reader):
            result = read_csv_file("transactions.csv")

    assert result == expected


def test_read_xlsx_file(tmp_path: Path) -> None:
    expected = [
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
    ]

    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = expected

    with patch("builtins.open", mock_open()):
        with patch("src.file_reader.pd.read_excel", return_value=mock_dataframe):
            result = read_xlsx_file("transactions_excel.xlsx")

    assert result == expected
