import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"
OUTPUT_FILE = "output/load_audit.csv"


def main():
    conn = sqlite3.connect(DB_PATH)

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "sectors",
        "stock_prices",
        "financial_ratios",
        "peer_groups"
    ]

    audit_data = []

    for table in tables:
        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        audit_data.append({
            "table_name": table,
            "rows_loaded": count,
            "status": "SUCCESS"
        })

    conn.close()

    audit_df = pd.DataFrame(audit_data)

    os.makedirs("output", exist_ok=True)

    audit_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 50)
    print("Load Audit Generated Successfully")
    print("=" * 50)
    print(audit_df)


if __name__ == "__main__":
    main()