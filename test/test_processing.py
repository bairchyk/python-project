from test.test_cases import FILTER_STATE_CASES, SORT_BY_DATE_CASES

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("state, expected_ids", FILTER_STATE_CASES)
def test_filter_by_state(
    operations: list[dict],
    state: str,
    expected_ids: list[int],
) -> None:
    result = filter_by_state(operations, state)

    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_default(operations: list[dict]) -> None:
    result = filter_by_state(operations)

    assert [operation["id"] for operation in result] == [
        41428829,
        939719570,
    ]


@pytest.mark.parametrize("descending, expected_dates", SORT_BY_DATE_CASES)
def test_sort_by_date(
    operations: list[dict],
    descending: bool,
    expected_dates: list[str],
) -> None:
    result = sort_by_date(operations, descending)

    assert [operation["date"] for operation in result] == expected_dates


def test_sort_by_date_same_dates() -> None:
    operations = [
        {"id": 1, "date": "2024-01-01T10:00:00"},
        {"id": 2, "date": "2024-01-01T10:00:00"},
        {"id": 3, "date": "2023-01-01T10:00:00"},
    ]

    result = sort_by_date(operations)

    assert result == [
        {"id": 1, "date": "2024-01-01T10:00:00"},
        {"id": 2, "date": "2024-01-01T10:00:00"},
        {"id": 3, "date": "2023-01-01T10:00:00"},
    ]


def test_sort_by_date_nonstandard_format() -> None:
    operations = [
        {"id": 1, "date": "2024-01-03"},
        {"id": 2, "date": "2024-01-01"},
        {"id": 3, "date": "2024-01-02"},
    ]

    result = sort_by_date(operations)

    assert [operation["id"] for operation in result] == [1, 3, 2]


def test_sort_by_date_empty_list() -> None:
    assert sort_by_date([]) == []
