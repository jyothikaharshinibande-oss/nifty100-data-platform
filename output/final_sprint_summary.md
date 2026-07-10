# Nifty100 Data Platform - Final Sprint Output Summary

Generated on: 2026-07-09

## Final Artifacts

- `db/nifty100.db`
- `db/schema.sql`
- `output/load_audit.csv`
- `output/validation_failures.csv`
- `output/capital_allocation.csv`
- `output/ratio_edge_cases.log`
- `output/screener_output.xlsx`
- `output/peer_comparison.xlsx`

## SQLite Checks

- companies: 92 rows
- profitandloss: 1263 rows
- balancesheet: 1312 rows
- cashflow: 1187 rows
- stock_prices: 5520 rows
- financial_ratios: 1184 rows
- peer_groups: 56 rows across 11 peer groups
- peer_percentiles: 560 rows
- PRAGMA foreign_key_check: 0 rows

## Screener Output

`output/screener_output.xlsx` contains 6 sheets:

- quality_compounder: 22 companies
- value_pick: 2 companies
- growth_accelerator: 18 companies
- dividend_champion: 30 companies
- debt_free_blue_chip: 2 companies
- turnaround_watch: 31 companies

Quality Compounder top companies:

- INDIGO
- ASIANPAINT
- TCS
- NESTLEIND
- IRCTC

## Peer Output

`output/peer_comparison.xlsx` contains 11 sheets:

- Automobiles
- Consumer Finance
- FMCG
- IT Services
- Life Insurance
- Oil & Gas
- Pharmaceuticals
- Power & Utilities
- Private Banks
- Public Sector Banks
- Steel

Peer percentile spot checks:

- IT Services ROE: TCS has the highest ROE and the highest ROE percentile.
- FMCG ROE: NESTLEIND has the highest ROE and the highest ROE percentile.

## Test Result

- Pytest: 5 passed

Note: the project currently contains 5 collected tests, not the 35+ Sprint 1 tests or 20 Sprint 2 KPI tests described in the sprint brief.

## Data Quality Exceptions

`output/validation_failures.csv` was generated. Remaining DQ exception counts:

- DQ-05: 1 positive-sales issue
- DQ-10: 85 missing balance-sheet records
- DQ-11: 1 invalid/missing website
- DQ-12: 22 missing cash-flow records
- DQ-13: 1 negative EPS issue
- DQ-15: 99 missing financial-ratio records

These are source-data coverage issues, not report-generation failures.

## Known Gaps Against Sprint Brief

- Radar chart PNGs were not generated because `matplotlib` is not installed in the current virtual environment.
- `value_pick` and `debt_free_blue_chip` return fewer than the requested 5 companies with the exact configured thresholds.
- The available test suite is smaller than the requested sprint test coverage.
