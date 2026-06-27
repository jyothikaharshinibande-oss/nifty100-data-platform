import sqlite3
from pathlib import Path
import pandas as pd

# ==========================
# Database Path
# ==========================

DATABASE = "db/nifty100.db"

# ==========================
# Excel Folder Paths
# ==========================

CORE_PATH = Path("data/raw/core")
SUPPLEMENTARY_PATH = Path("data/raw/supplementary")

# ==========================
# Files having headers in 2nd row
# ==========================

HEADER_ROW_2 = {
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "profitandloss.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}

# ==========================
# Excel File -> Table Mapping
# ==========================

TABLE_MAPPING = {

    "companies.xlsx": "companies",

    "profitandloss.xlsx": "profitandloss",

    "balancesheet.xlsx": "balancesheet",

    "cashflow.xlsx": "cashflow",

    "analysis.xlsx": "analysis",

    "documents.xlsx": "documents",

    "prosandcons.xlsx": "prosandcons",

    "sectors.xlsx": "sectors",

    "stock_prices.xlsx": "stock_prices",

    "financial_ratios.xlsx": "financial_ratios",

    "peer_groups.xlsx": "peer_groups"

    # market_cap.xlsx intentionally skipped
}


# ==========================
# Read Excel
# ==========================

def read_excel(file_path):

    if file_path.name in HEADER_ROW_2:

        df = pd.read_excel(
            file_path,
            header=1
        )

    else:

        df = pd.read_excel(file_path)

    return df


# ==========================
# Load Table
# ==========================

def load_table(conn, table_name, df):

    # ----------------------
    # Normalize column names
    # ----------------------

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    before = len(df)

    # ----------------------
    # Remove duplicate rows
    # ----------------------

    if table_name == "profitandloss":

        df = df.drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )

    else:

        df = df.drop_duplicates()

    after = len(df)

    print(f"Removed {before-after} duplicate rows")

    # ----------------------
    # Load into SQLite
    # ----------------------

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"✅ {table_name:<20} {after} rows loaded")


# ==========================
# Main Function
# ==========================

def main():

    conn = sqlite3.connect(DATABASE)

    conn.execute("PRAGMA foreign_keys = ON")

    # ----------------------
    # Collect all Excel files
    # ----------------------

    excel_files = []

    excel_files.extend(CORE_PATH.glob("*.xlsx"))

    excel_files.extend(SUPPLEMENTARY_PATH.glob("*.xlsx"))

    print("=" * 60)

    print(f"Found {len(excel_files)} Excel files")

    print("=" * 60)

    for file in excel_files:

        print()

        print(f"Processing : {file}")

        if file.name not in TABLE_MAPPING:

            print(f"⚠ Skipping {file.name}")

            continue

        df = read_excel(file)

        print(f"Shape : {df.shape}")

        load_table(
            conn,
            TABLE_MAPPING[file.name],
            df
        )

    conn.commit()

    conn.close()

    print()

    print("=" * 60)

    print("Database Load Completed Successfully")

    print("=" * 60)


# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":

    main()