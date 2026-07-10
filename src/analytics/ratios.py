import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = "db/nifty100.db"
EDGE_CASE_LOG = "output/ratio_edge_cases.log"


def safe_divide(numerator, denominator, multiplier=1):
    if denominator is None or denominator == 0:
        return None
    return numerator / denominator * multiplier


def net_profit_margin(net_profit, sales):
    return safe_divide(net_profit, sales, 100)


def operating_profit_margin(operating_profit, sales):
    return safe_divide(operating_profit, sales, 100)


def opm_mismatch(computed_opm, source_opm, tolerance=1):
    if computed_opm is None or source_opm is None:
        return False
    return abs(computed_opm - source_opm) > tolerance


def return_on_equity(net_profit, equity, reserves=0):
    capital = (equity or 0) + (reserves or 0)
    if capital <= 0:
        return None
    return net_profit / capital * 100


def return_on_capital_employed(ebit, equity, reserves=0, borrowings=0):
    capital_employed = (equity or 0) + (reserves or 0) + (borrowings or 0)
    if capital_employed <= 0:
        return None
    return ebit / capital_employed * 100


def return_on_assets(net_profit, total_assets):
    return safe_divide(net_profit, total_assets, 100)


def debt_to_equity(borrowings, equity, reserves=0):
    if not borrowings:
        return 0

    capital = (equity or 0) + (reserves or 0)
    if capital <= 0:
        return None
    return borrowings / capital


def high_leverage_flag(de_ratio, broad_sector):
    if de_ratio is None:
        return False
    if str(broad_sector).lower() == "financials":
        return False
    return de_ratio > 5


def interest_coverage(operating_profit, other_income, interest):
    if not interest:
        return None
    return ((operating_profit or 0) + (other_income or 0)) / interest


def interest_coverage_label(icr):
    return "Debt Free" if icr is None else None


def icr_warning_flag(icr):
    return icr is not None and icr < 1.5


def net_debt(borrowings, investments):
    return (borrowings or 0) - (investments or 0)


def asset_turnover(sales, total_assets):
    return safe_divide(sales, total_assets)


def generate_ratio_edge_case_log(output_path=EDGE_CASE_LOG):
    conn = sqlite3.connect(DB_PATH)
    companies = pd.read_sql(
        """
        SELECT id AS company_id,
               company_name,
               roce_percentage AS source_roce,
               roe_percentage AS source_roe
        FROM companies
        """,
        conn,
    )
    ratios = pd.read_sql(
        "SELECT company_id, year, return_on_equity_pct AS computed_roe FROM financial_ratios",
        conn,
    )
    conn.close()

    ratios["fiscal_year"] = (
        ratios["year"].astype(str).str.extract(r"(\d{4})")[0].astype(float)
    )
    latest = (
        ratios.dropna(subset=["fiscal_year"])
        .sort_values(["company_id", "fiscal_year"])
        .drop_duplicates("company_id", keep="last")
    )
    report = companies.merge(
        latest[["company_id", "year", "computed_roe"]],
        on="company_id",
        how="left",
    )

    lines = [
        "Ratio Edge Case Log",
        "Category values: DATA_SOURCE_ISSUE, VERSION_DIFFERENCE, FORMULA_DISCREPANCY, DOCUMENTED_DECISION",
        "",
        "DOCUMENTED_DECISION: For analytics, computed financial_ratios.return_on_equity_pct is used. companies.roe_percentage is kept for display cross-check only.",
        "DOCUMENTED_DECISION: Financial-sector leverage warnings are suppressed because high balance-sheet leverage is structurally normal for banks/NBFCs/insurers.",
        "",
    ]

    anomalies = report[
        (report["source_roe"].notna())
        & (report["computed_roe"].notna())
        & ((report["source_roe"] - report["computed_roe"]).abs() > 5)
    ]

    if anomalies.empty:
        lines.append("No ROE source-vs-computed anomalies above 5 percentage points.")
    else:
        for row in anomalies.sort_values("company_id").itertuples(index=False):
            lines.append(
                "DATA_SOURCE_ISSUE | "
                f"{row.company_id} | {row.company_name} | {row.year} | "
                f"source_roe={row.source_roe} | computed_roe={row.computed_roe} | "
                "difference exceeds 5 percentage points; computed value retained for analytics."
            )

    missing = report[report["computed_roe"].isna()]
    if not missing.empty:
        lines.append("")
        for row in missing.sort_values("company_id").itertuples(index=False):
            lines.append(
                "FORMULA_DISCREPANCY | "
                f"{row.company_id} | {row.company_name} | latest computed ROE missing in financial_ratios."
            )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    path = generate_ratio_edge_case_log()
    print(f"Generated {path}")
