PRAGMA foreign_keys = ON;

--------------------------------------------------------
-- Companies
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE,
    sector TEXT,
    industry TEXT,
    isin TEXT,
    bse_code TEXT,
    nse_code TEXT,
    website TEXT
);

--------------------------------------------------------
-- Profit & Loss
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    operating_profit REAL,
    operating_profit_margin REAL,
    net_profit REAL,
    eps REAL,
    tax_rate REAL,
    dividend REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Balance Sheet
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS balancesheet (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    year INTEGER,

    total_assets REAL,

    total_liabilities REAL,

    equity REAL,

    reserves REAL,

    borrowings REAL,

    cash REAL,

    investments REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Cash Flow
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS cashflow (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    year INTEGER,

    operating_cashflow REAL,

    investing_cashflow REAL,

    financing_cashflow REAL,

    net_cashflow REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Analysis
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS analysis (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    strengths TEXT,

    weaknesses TEXT,

    opportunities TEXT,

    threats TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Documents
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    document_name TEXT,

    document_url TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Pros & Cons
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS prosandcons (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    type TEXT,

    description TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Sectors
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS sectors (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    broad_sector TEXT,

    sub_sector TEXT,

    index_weight_pct REAL,

    market_cap_category TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Stock Prices
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_prices (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    date DATE,

    open_price REAL,

    high_price REAL,

    low_price REAL,

    close_price REAL,

    volume INTEGER,

    adjusted_close REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Financial Ratios
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id INTEGER,

    year INTEGER,

    net_profit_margin_pct REAL,

    operating_profit_margin_pct REAL,

    return_on_equity_pct REAL,

    debt_to_equity REAL,

    interest_coverage REAL,

    asset_turnover REAL,

    free_cash_flow_cr REAL,

    capex_cr REAL,

    earnings_per_share REAL,

    book_value_per_share REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

--------------------------------------------------------
-- Peer Groups
--------------------------------------------------------
CREATE TABLE IF NOT EXISTS peer_groups (

    id INTEGER PRIMARY KEY,

    peer_group_name TEXT,

    company_id INTEGER,

    is_benchmark BOOLEAN,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);