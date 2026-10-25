# Реализована функция для считывания финансовых операций из CSV.
import csv
import os

import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "..", "transactions.csv")


def read_csv_file(file_path: str) -> list[dict[str, str]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


# print(read_csv_file(file_path))

excel_path = os.path.join(os.path.dirname(__file__), "..", "transactions_excel.xlsx")


def read_xlsx_file(excel_path: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    excel_data = pd.read_excel(excel_path)
    return excel_data.to_dict(orient="records")


# print(read_xlsx_file(excel_path))
