"""
filters.py

Reusable filtering functions for the financial screener.
"""

import pandas as pd
import numpy as np


def apply_min_filter(df, column, value):
    """
    Keep rows where column >= value.
    """
    if value is None or column not in df.columns:
        return df

    return df[df[column] >= value]


def apply_max_filter(df, column, value):
    """
    Keep rows where column <= value.
    """
    if value is None or column not in df.columns:
        return df

    return df[df[column] <= value]


def filter_debt_equity(df, max_de):
    """
    Debt/Equity filter.

    Companies in Financial sector are skipped
    because D/E is not meaningful for banks/NBFCs.
    """

    if max_de is None:
        return df

    if "broad_sector" not in df.columns:
        return apply_max_filter(df, "debt_equity", max_de)

    financial_df = df[
        df["broad_sector"].str.lower() == "financials"
    ]

    non_financial_df = df[
        df["broad_sector"].str.lower() != "financials"
    ]

    non_financial_df = non_financial_df[
        non_financial_df["debt_equity"] <= max_de
    ]

    return pd.concat(
        [financial_df, non_financial_df],
        ignore_index=True
    )


def filter_interest_coverage(df, min_icr):
    """
    Interest Coverage filter.

    Debt Free companies always pass.
    """

    if min_icr is None:
        return df

    if "interest_coverage" not in df.columns:
        return df

    temp = df.copy()

    temp["interest_coverage"] = temp["interest_coverage"].replace(
        "Debt Free",
        np.inf
    )

    temp["interest_coverage"] = pd.to_numeric(
        temp["interest_coverage"],
        errors="coerce"
    )

    return temp[
        temp["interest_coverage"] >= min_icr
    ]


def filter_positive_fcf(df):
    """
    Keep only companies having positive Free Cash Flow.
    """

    if "free_cash_flow" not in df.columns:
        return df

    return df[
        df["free_cash_flow"] > 0
    ]


def filter_market_cap(df, minimum):
    """
    Minimum market capitalization.
    """

    return apply_min_filter(
        df,
        "market_cap",
        minimum
    )


def filter_sales(df, minimum):
    """
    Minimum sales.
    """

    return apply_min_filter(
        df,
        "sales",
        minimum
    )


def filter_eps_growth(df, minimum):
    """
    EPS CAGR filter.
    """

    return apply_min_filter(
        df,
        "eps_cagr_5yr",
        minimum
    )


def filter_pat_growth(df, minimum):
    """
    PAT CAGR filter.
    """

    return apply_min_filter(
        df,
        "pat_cagr_5yr",
        minimum
    )


def filter_revenue_growth(df, minimum):
    """
    Revenue CAGR filter.
    """

    return apply_min_filter(
        df,
        "revenue_cagr_5yr",
        minimum
    )


def filter_dividend(df, minimum):
    """
    Dividend Yield filter.
    """

    return apply_min_filter(
        df,
        "dividend_yield",
        minimum
    )


def filter_pb(df, maximum):
    """
    Price to Book filter.
    """

    return apply_max_filter(
        df,
        "pb_ratio",
        maximum
    )


def filter_pe(df, maximum):
    """
    Price to Earnings filter.
    """

    return apply_max_filter(
        df,
        "pe_ratio",
        maximum
    )


def filter_roe(df, minimum):
    """
    ROE filter.
    """

    return apply_min_filter(
        df,
        "roe",
        minimum
    )


def filter_opm(df, minimum):
    """
    Operating Profit Margin.
    """

    return apply_min_filter(
        df,
        "opm",
        minimum
    )


def filter_asset_turnover(df, minimum):
    """
    Asset Turnover filter.
    """

    return apply_min_filter(
        df,
        "asset_turnover",
        minimum
    )


def filter_net_profit(df, minimum):
    """
    Net Profit filter.
    """

    return apply_min_filter(
        df,
        "net_profit",
        minimum
    )