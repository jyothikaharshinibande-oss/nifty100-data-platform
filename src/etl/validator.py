import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"
OUTPUT_FILE = "output/validation_failures.csv"


def run_query(conn, query):
    return pd.read_sql_query(query, conn)


def main():

    conn = sqlite3.connect(DB_PATH)

    failures = []

    print("=" * 60)
    print("DATA QUALITY VALIDATION")
    print("=" * 60)

    # -------------------------
    # DQ-01 : Duplicate Company ID
    # -------------------------
    dq1 = run_query(conn, """
        SELECT id, COUNT(*) AS total
        FROM companies
        GROUP BY id
        HAVING COUNT(*) > 1
    """)

    print("\nDQ-01 : Duplicate Company ID")
    print(dq1)

    if not dq1.empty:
        dq1["rule"] = "DQ-01"
        failures.append(dq1)

    # -------------------------
    # DQ-02 : Duplicate Company-Year
    # -------------------------
    dq2 = run_query(conn, """
        SELECT company_id,
               year,
               COUNT(*) AS total
        FROM profitandloss
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
    """)

    print("\nDQ-02 : Duplicate Company-Year")
    print(dq2)

    if not dq2.empty:
        dq2["rule"] = "DQ-02"
        failures.append(dq2)

    # -------------------------
    # DQ-03 : Foreign Keys
    # -------------------------
    print("\nDQ-03 : Foreign Key Check")

    fk = conn.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()

    print(fk)

    # -------------------------
    # DQ-04 : Balance Sheet Check
    # -------------------------

    dq4 = run_query(conn, """
    SELECT company_id,
           year,
           total_assets,
           total_liabilities
    FROM balancesheet
    WHERE ABS(total_assets-total_liabilities)>1
    """)

    print("\nDQ-04 : Balance Sheet")

    print(dq4)

    if not dq4.empty:
        dq4["rule"] = "DQ-04"
        failures.append(dq4)

    # -------------------------
    # DQ-05 : Positive Sales
    # -------------------------

    dq5 = run_query(conn, """
    SELECT company_id,
           year,
           sales
    FROM profitandloss
    WHERE sales<=0
    """)

    print("\nDQ-05 : Positive Sales")

    print(dq5)

    if not dq5.empty:
        dq5["rule"] = "DQ-05"
        failures.append(dq5)
        

    # -------------------------
    # DQ-06 : Missing Profit Before Tax
    # -------------------------
    dq6 = run_query(conn, """
    SELECT company_id,
       year,
       profit_before_tax
    FROM profitandloss
    WHERE profit_before_tax IS NULL
    """)

    print("\nDQ-06 : Missing Profit Before Tax")
    print(dq6)

    if not dq6.empty:
        dq6["rule"] = "DQ-06"
        failures.append(dq6)

    # -------------------------
    # DQ-07 : Missing Assets/Liabilities
    # -------------------------

    dq7 = run_query(conn, """
    SELECT company_id,
       year,
       total_assets,
       total_liabilities
    FROM balancesheet
    WHERE total_assets IS NULL
    OR total_liabilities IS NULL
    """)

    print("\nDQ-07 : Missing Balance Sheet Values")
    print(dq7)

    if not dq7.empty:
        dq7["rule"] = "DQ-07"
        failures.append(dq7)
    # -------------------------
    # DQ-08 : Duplicate Company Name
    # -------------------------

    dq8 = run_query(conn, """
    SELECT company_name,
       COUNT(*) AS total
    FROM companies
    GROUP BY company_name
    HAVING COUNT(*) > 1
    """)

    print("\nDQ-08 : Duplicate Company Name")
    print(dq8)

    if not dq8.empty:
        dq8["rule"] = "DQ-08"
        failures.append(dq8)
    
    # -------------------------
    # DQ-09 : Invalid Year Format
    # -------------------------

    dq9 = run_query(conn, """
    SELECT
        company_id,
        year
    FROM profitandloss
    WHERE year NOT LIKE 'Mar %'
    AND year NOT LIKE 'Dec %'
    AND year NOT LIKE 'Jun %'
    AND year NOT LIKE 'Sep %'
    AND year <> 'TTM'
    """)

    print("\nDQ-09 : Invalid Year Format")
    print(dq9)

    if not dq9.empty:
        dq9["rule"] = "DQ-09"
        failures.append(dq9)

    # -------------------------
    # DQ-10 : Missing Balance Sheet Record
    # -------------------------

    dq10 = run_query(conn, """
    SELECT
        p.company_id,
        p.year
    FROM profitandloss p
    LEFT JOIN balancesheet b
    ON p.company_id = b.company_id
    AND p.year = b.year
    WHERE b.company_id IS NULL
    AND p.year <> 'TTM'
    """)

    print("\nDQ-10 : Missing Balance Sheet Record")
    print(dq10)

    if not dq10.empty:
        dq10["rule"] = "DQ-10"
        failures.append(dq10)
    
        
    # -------------------------
    # DQ-11 : Invalid Website URL
    # -------------------------

    dq11 = run_query(conn, """
    SELECT id,
           company_name,
           website
    FROM companies
    WHERE website IS NULL
       OR website NOT LIKE 'http%'
    """)

    print("\nDQ-11 : Invalid Website URL")
    print(dq11)

    if not dq11.empty:
        dq11["rule"] = "DQ-11"
        failures.append(dq11)

    # -------------------------
    # DQ-12 : Missing Cash Flow Record
    # -------------------------

    dq12 = run_query(conn, """
    SELECT
        p.company_id,
        p.year
    FROM profitandloss p
    LEFT JOIN cashflow c
    ON p.company_id = c.company_id
    AND p.year = c.year
    WHERE c.company_id IS NULL
    AND p.year <> 'TTM'
    """)

    print("\nDQ-12 : Missing Cash Flow Record")
    print(dq12)

    if not dq12.empty:
        dq12["rule"] = "DQ-12"
        failures.append(dq12)

    # -------------------------
    # DQ-13 : Negative EPS
    # -------------------------

    dq13 = run_query(conn, """
    SELECT
        company_id,
        year,
        net_profit,
        eps
    FROM profitandloss
    WHERE net_profit > 0
    AND eps < 0
    """)

    print("\nDQ-13 : Negative EPS")
    print(dq13)

    if not dq13.empty:
        dq13["rule"] = "DQ-13"
        failures.append(dq13)

    # -------------------------
    # DQ-14 : Missing Stock Prices
    # -------------------------

    dq14 = run_query(conn, """
    SELECT c.id AS company_id
    FROM companies c
    LEFT JOIN stock_prices s
    ON c.id = s.company_id
    WHERE s.company_id IS NULL
    """)

    print("\nDQ-14 : Missing Stock Prices")
    print(dq14)

    if not dq14.empty:
        dq14["rule"] = "DQ-14"
        failures.append(dq14)

    # -------------------------
    # DQ-15 : Missing Financial Ratios
    # -------------------------

    dq15 = run_query(conn, """
    SELECT
        p.company_id,
        p.year
    FROM profitandloss p
    LEFT JOIN financial_ratios f
    ON p.company_id = f.company_id
    AND p.year = f.year
    WHERE f.company_id IS NULL
    AND p.year <> 'TTM'
    """)

    print("\nDQ-15 : Missing Financial Ratios")
    print(dq15)

    if not dq15.empty:
        dq15["rule"] = "DQ-15"
        failures.append(dq15)

    # -------------------------
    # DQ-16 : Missing Company Name
    # -------------------------

    dq16 = run_query(conn, """
    SELECT id,
           company_name
    FROM companies
    WHERE company_name IS NULL
       OR TRIM(company_name) = ''
    """)

    print("\nDQ-16 : Missing Company Name")
    print(dq16)

    if not dq16.empty:
        dq16["rule"] = "DQ-16"
        failures.append(dq16)

    # -------------------------
    # Save Validation Report
    # -------------------------

    os.makedirs("output", exist_ok=True)

    if failures:
        final_df = pd.concat(failures, ignore_index=True)
    else:
        final_df = pd.DataFrame()

    final_df.to_csv(OUTPUT_FILE, index=False)

    conn.close()

    print("\nValidation Completed")
    print(f"Generated -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()