import pandas as pd

df = pd.read_excel(
    "data/raw/core/profitandloss.xlsx",
    header=1
)

df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
)

duplicates = df[
    (df["company_id"] == "ADANIPORTS") &
    (df["year"] == "Mar 2024")
]

print(duplicates)