import sqlite3
import yaml
import pandas as pd

from src.screener.filters import (
    filter_roe,
    filter_debt_equity,
    filter_interest_coverage,
    filter_positive_fcf,
    filter_revenue_growth,
    filter_pat_growth,
    filter_opm,
    filter_pe,
    filter_pb,
    filter_dividend,
    filter_market_cap,
    filter_net_profit,
    filter_eps_growth,
    filter_asset_turnover,
    filter_sales,
)

DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


class ScreenerEngine:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        query = """
        WITH latest_prices AS (
            SELECT sp.company_id,
                   sp.close_price
            FROM stock_prices sp
            INNER JOIN (
                SELECT company_id,
                       MAX(date) AS latest_date
                FROM stock_prices
                GROUP BY company_id
            ) latest
            ON sp.company_id = latest.company_id
            AND sp.date = latest.latest_date
        )
        SELECT
            f.company_id,
            f.year,
            c.company_name,
            s.broad_sector,
            p.sales,
            p.net_profit,
            f.return_on_equity_pct AS roe,
            f.debt_to_equity AS debt_equity,
            f.interest_coverage,
            f.asset_turnover,
            f.free_cash_flow_cr AS free_cash_flow,
            f.operating_profit_margin_pct AS opm,
            f.earnings_per_share,
            f.book_value_per_share,
            f.dividend_payout_ratio_pct,
            lp.close_price,
            CASE
                WHEN f.earnings_per_share IS NOT NULL
                     AND f.earnings_per_share != 0
                THEN lp.close_price / f.earnings_per_share
            END AS pe_ratio,
            CASE
                WHEN f.book_value_per_share IS NOT NULL
                     AND f.book_value_per_share != 0
                THEN lp.close_price / f.book_value_per_share
            END AS pb_ratio
        FROM financial_ratios f
        LEFT JOIN companies c
            ON f.company_id = c.id
        LEFT JOIN profitandloss p
            ON f.company_id = p.company_id
            AND f.year = p.year
        LEFT JOIN sectors s
            ON f.company_id = s.company_id
        LEFT JOIN latest_prices lp
            ON f.company_id = lp.company_id
        """

        df = pd.read_sql(query, self.conn)

        return df

    def load_config(self):

        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)

        return config

    def apply_filters(self, df, rules):

        if "roe_min" in rules:
            df = filter_roe(df, rules["roe_min"])

        if "de_max" in rules:
            df = filter_debt_equity(df, rules["de_max"])

        if "fcf_positive" in rules:
            if rules["fcf_positive"]:
                df = filter_positive_fcf(df)

        if "revenue_cagr_5yr_min" in rules:
            df = filter_revenue_growth(
                df,
                rules["revenue_cagr_5yr_min"]
            )

        if "pat_cagr_5yr_min" in rules:
            df = filter_pat_growth(
                df,
                rules["pat_cagr_5yr_min"]
            )

        if "opm_min" in rules:
            df = filter_opm(df, rules["opm_min"])

        if "pe_max" in rules:
            df = filter_pe(df, rules["pe_max"])

        if "pb_max" in rules:
            df = filter_pb(df, rules["pb_max"])

        if "dividend_yield_min" in rules:
            df = filter_dividend(
                df,
                rules["dividend_yield_min"]
            )

        if "interest_coverage_min" in rules:
            df = filter_interest_coverage(
                df,
                rules["interest_coverage_min"]
            )

        if "market_cap_min" in rules:
            df = filter_market_cap(
                df,
                rules["market_cap_min"]
            )

        if "net_profit_min" in rules:
            df = filter_net_profit(
                df,
                rules["net_profit_min"]
            )

        if "eps_cagr_5yr_min" in rules:
            df = filter_eps_growth(
                df,
                rules["eps_cagr_5yr_min"]
            )

        if "asset_turnover_min" in rules:
            df = filter_asset_turnover(
                df,
                rules["asset_turnover_min"]
            )

        if "sales_min" in rules:
            df = filter_sales(
                df,
                rules["sales_min"]
            )

        return df

    def run(self, screener_name):

        config = self.load_config()

        if screener_name not in config:
            raise ValueError(f"{screener_name} not found")

        df = self.load_data()

        rules = config[screener_name]

        result = self.apply_filters(df, rules)

        result = result.sort_values(
            by="roe",
            ascending=False
        )

        return result

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    engine = ScreenerEngine()

    result = engine.run("quality_compounder")

    print(result.head())

    engine.close()
