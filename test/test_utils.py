from unittest.mock import Mock, mock_open, patch

from src.utils import read_json_file


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1}, {"id": 2}]',
)
def test_read_json_file_success(mock_file: Mock) -> None:
    """Проверяет успешное чтение JSON-файла."""
    result = read_json_file("operations.json")

    assert result == [{"id": 1}, {"id": 2}]

    mock_file.assert_called_once_with(
        "operations.json",
        "r",
        encoding="utf-8",
    )


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="",
)
def test_read_json_file_empty(_mock_file: Mock) -> None:
    """Проверяет чтение пустого JSON-файла."""
    assert read_json_file("empty.json") == []


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"id": 1}',
)
def test_read_json_file_not_list(_mock_file: Mock) -> None:
    """Проверяет JSON, содержащий не список."""
    assert read_json_file("not_list.json") == []


@patch(
    "builtins.open",
    side_effect=FileNotFoundError,
)
def test_read_json_file_not_found(_mock_file: Mock) -> None:
    """Проверяет отсутствие JSON-файла."""
    assert read_json_file("missing.json") == []
