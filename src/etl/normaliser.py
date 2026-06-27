import re
import pandas as pd

def normalize_year(year):
    """
    Normalize different year formats to a 4-digit year.

    Examples:
        FY2024   -> 2024
        Mar 2023 -> 2023
        2023-24  -> 2024
        2024     -> 2024
    """

    if pd.isna(year):
        return None

    year = str(year).strip()

    # Handle financial year first
    fy_match = re.match(r"(\d{4})-(\d{2})$", year)
    if fy_match:
        start = int(fy_match.group(1))
        end = int(fy_match.group(2))
        return (start // 100) * 100 + end

    # Extract a normal 4-digit year
    match = re.search(r"(19|20)\d{2}", year)
    if match:
        return int(match.group())

    return None