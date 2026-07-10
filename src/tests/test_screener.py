from src.screener.engine import ScreenerEngine


def test_quality_compounder():
    engine = ScreenerEngine()

    try:
        df = engine.run("quality_compounder")

        assert df is not None, "Returned DataFrame is None."
        assert not df.empty, "No stocks returned by the screener."

        # Required columns
        required_cols = ["company_id", "roe", "debt_equity"]
        for col in required_cols:
            assert col in df.columns, f"Column '{col}' not found."

        # Rule 1: ROE must be > 15 for all stocks
        assert (df["roe"] > 15).all(), "Some stocks have ROE <= 15."

        # Financial companies (Debt/Equity is not a meaningful filter)
        financial_companies = [
            "AXISBANK",
            "BANKBARODA",
            "BAJFINANCE",
            "BAJAJFINSV",
            "CHOLAFIN",
            "PFC",
            "RECLTD",
            "SHRIRAMFIN",
        ]

        # Apply Debt/Equity rule only to non-financial companies
        non_financial = df[~df["company_id"].isin(financial_companies)]

        if not non_financial.empty:
            assert (
                non_financial["debt_equity"] < 1
            ).all(), "Some non-financial stocks have Debt/Equity >= 1."

        print("\n✅ Quality Compounder Test Passed")
        print(f"Returned {len(df)} stocks.")

    finally:
        engine.close()


if __name__ == "__main__":
    test_quality_compounder()