import pandas as pd
from pathlib import Path

HEADER_ROW_2 = {
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "profitandloss.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}


def read_excel_file(file_path):
    filename = Path(file_path).name

    if filename in HEADER_ROW_2:
        return pd.read_excel(file_path, header=1)

    return pd.read_excel(file_path)


def read_all_files():

    datasets = {}

    raw_path = Path("data/raw")

    for file in raw_path.rglob("*.xlsx"):

        try:

            df = read_excel_file(file)

            datasets[file.stem] = df

            print(f"Loaded {file.name}")

            print(df.head())

            print(df.columns.tolist())

        except Exception as e:

            print(file.name, e)

    return datasets


if __name__ == "__main__":
    read_all_files()