import sqlite3
import pandas as pd


def test_peer_percentiles():
    conn = sqlite3.connect("db/nifty100.db")

    try:
        query = """
        SELECT *
        FROM peer_percentiles
        WHERE metric = 'return_on_equity_pct'
        """

        df = pd.read_sql(query, conn)

        print(f"Rows found: {len(df)}")
        print(df.head())

        assert not df.empty, "No return_on_equity_pct data found."

        print("✅ Peer ranking table exists and contains ROE percentile data.")

    finally:
        conn.close()


if __name__ == "__main__":
    test_peer_percentiles()