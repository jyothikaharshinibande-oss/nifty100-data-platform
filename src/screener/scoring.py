import pandas as pd


def normalize(series):

    series = series.fillna(0)

    minimum = series.min()
    maximum = series.max()

    if minimum == maximum:
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return ((series - minimum) /
            (maximum - minimum)) * 100


def calculate_composite_score(df):

    score = pd.DataFrame(index=df.index)

    score["roe"] = normalize(df["roe"])

    score["opm"] = normalize(df["opm"])

    score["fcf"] = normalize(df["free_cash_flow"])

    score["asset"] = normalize(df["asset_turnover"])

    # Lower debt is better
    score["de"] = 100 - normalize(df["debt_equity"])

    score["icr"] = normalize(
        df["interest_coverage"]
    )

    df["composite_quality_score"] = (

        score["roe"] * 0.25 +

        score["opm"] * 0.20 +

        score["fcf"] * 0.20 +

        score["asset"] * 0.15 +

        score["de"] * 0.10 +

        score["icr"] * 0.10

    ).round(2)

    return df