from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


def test_log_returns_result() -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(1, 2)

    assert result == 3


def test_log_console(capsys: CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    add(1, 2)

    captured = capsys.readouterr()

    assert "add started" in captured.out
    assert "add ok" in captured.out
    assert "add result: 3" in captured.out
    assert "add finished" in captured.out


def test_log_console_error(capsys: CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    with pytest.raises(TypeError):
        add(1, "2")  # type: ignore[arg-type]

    captured = capsys.readouterr()

    assert "add started" in captured.out
    assert "TypeError" in captured.out
    assert "Inputs: (1, '2'), {}" in captured.out
    assert "add finished" in captured.out


def test_log_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test_log.txt"

    @log(filename=log_file)
    def add(x: int, y: int) -> int:
        return x + y

    add(1, 2)

    content = log_file.read_text()

    assert "add started" in content
    assert "add ok" in content
    assert "add result: 3" in content
    assert "add finished" in content
