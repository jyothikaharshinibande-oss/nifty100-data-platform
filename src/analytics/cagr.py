NORMAL = "NORMAL"
DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


def cagr(start_value, end_value, periods):
    if periods is None or periods <= 0:
        return None, INSUFFICIENT

    if start_value is None or end_value is None:
        return None, INSUFFICIENT

    if start_value == 0:
        return None, ZERO_BASE

    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    if end_value == 0:
        return None, DECLINE_TO_LOSS

    return ((end_value / start_value) ** (1 / periods) - 1) * 100, NORMAL


def cagr_for_window(rows, value_key, years):
    ordered = sorted(rows, key=lambda row: row["fiscal_year"])

    if len(ordered) < 2:
        return None, INSUFFICIENT

    latest = ordered[-1]
    start_year = latest["fiscal_year"] - years
    candidates = [
        row for row in ordered
        if row["fiscal_year"] <= start_year
    ]

    if not candidates:
        return None, INSUFFICIENT

    start = candidates[-1]
    periods = latest["fiscal_year"] - start["fiscal_year"]
    return cagr(start[value_key], latest[value_key], periods)
