import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = "db/nifty100.db"
CAPITAL_ALLOCATION_PATH = "output/capital_allocation.csv"


def free_cash_flow(operating_cashflow, investing_cashflow):
    return (operating_cashflow or 0) + (investing_cashflow or 0)


def cfo_pat_ratio(cfo, pat):
    if not pat:
        return None
    return cfo / pat


def cfo_quality_label(ratio):
    if ratio is None:
        return None
    if ratio > 1:
        return "High Quality"
    if ratio >= 0.5:
        return "Moderate"
    return "Accrual Risk"


def capex_intensity(investing_cashflow, sales):
    if not sales:
        return None
    return abs(investing_cashflow) / sales * 100


def capex_intensity_label(value):
    if value is None:
        return None
    if value < 3:
        return "Asset Light"
    if value <= 8:
        return "Moderate"
    return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    if not operating_profit:
        return None
    return fcf / operating_profit * 100


def sign_label(value):
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat=None):
    signs = (sign_label(cfo), sign_label(cfi), sign_label(cff))

    if signs == ("+", "-", "-") and cfo_pat is not None and cfo_pat > 1:
        return "Shareholder Returns"
    if signs == ("+", "-", "-"):
        return "Reinvestor"
    if signs == ("+", "+", "-"):
        return "Liquidating Assets"
    if signs == ("-", "+", "+"):
        return "Distress Signal"
    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"
    if signs == ("+", "+", "+"):
        return "Cash Accumulator"
    if signs == ("-", "-", "-"):
        return "Pre-Revenue"
    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Other"


def generate_capital_allocation(output_path=CAPITAL_ALLOCATION_PATH):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        c.company_id,
        c.year,
        c.operating_activity,
        c.investing_activity,
        c.financing_activity,
        p.net_profit
    FROM cashflow c
    LEFT JOIN profitandloss p
        ON c.company_id = p.company_id
        AND c.year = p.year
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df = df.rename(
        columns={
            "operating_activity": "operating_cashflow",
            "investing_activity": "investing_cashflow",
            "financing_activity": "financing_cashflow",
        }
    )
    df["cfo_pat_ratio"] = df.apply(
        lambda row: cfo_pat_ratio(row["operating_cashflow"], row["net_profit"]),
        axis=1,
    )
    df["cfo_sign"] = df["operating_cashflow"].apply(sign_label)
    df["cfi_sign"] = df["investing_cashflow"].apply(sign_label)
    df["cff_sign"] = df["financing_cashflow"].apply(sign_label)
    df["pattern_label"] = df.apply(
        lambda row: capital_allocation_pattern(
            row["operating_cashflow"],
            row["investing_cashflow"],
            row["financing_cashflow"],
            row["cfo_pat_ratio"],
        ),
        axis=1,
    )

    columns = [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df[columns].to_csv(output_path, index=False)
    return df[columns]


if __name__ == "__main__":
    result = generate_capital_allocation()
    print(f"Generated {CAPITAL_ALLOCATION_PATH}")
    print(result["pattern_label"].value_counts().to_string())
