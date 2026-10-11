from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(
    filename: str | Path | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логирует начало и конец выполнения функции.

    Логирует результат выполнения или возникшие ошибки.
    """

    def write_log(message: str) -> None:
        """Выводит сообщение в консоль или записывает его в файл."""
        if filename:
            with open(filename, "a") as file:
                file.write(message + "\n")
        else:
            print(message)

    def my_decorator(function: Callable[P, R]) -> Callable[P, R]:
        """Оборачивает функцию для логирования ее выполнения."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Выполняет функцию и логирует результат или исключение."""
            message = f"{function.__name__} started"
            write_log(message)
            try:
                result = function(*args, **kwargs)
                message = f"{function.__name__} ok"
                write_log(message)
                message = f"{function.__name__} result: {result}"
                write_log(message)
                return result
            except Exception as error:
                message = f"{function.__name__} error: {type(error).__name__}. Inputs: {args}, {kwargs}"
                write_log(message)
                raise
            finally:
                message = f"{function.__name__} finished"
                write_log(message)

        return wrapper

    return my_decorator


# @log(filename="mylog.txt")
# def my_function(x, y):
#    return x + y


# if __name__ == "__main__":
#    my_function(1, 2)
#    my_function(1, "2")
