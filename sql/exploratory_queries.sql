SELECT COUNT(*) AS total_companies
FROM companies;
SELECT broad_sector,
COUNT(*) AS total
FROM sectors
GROUP BY broad_sector
ORDER BY total DESC;
SELECT company_id,
COUNT(*) AS records
FROM profitandloss
GROUP BY company_id
ORDER BY records DESC;
SELECT company_id,
AVG(close_price) AS average_price
FROM stock_prices
GROUP BY company_id
ORDER BY average_price DESC
LIMIT 10;
SELECT company_id,
MAX(net_profit) AS highest_profit
FROM profitandloss
GROUP BY company_id
ORDER BY highest_profit DESC
LIMIT 10;
SELECT company_id,
MAX(total_assets) AS assets
FROM balancesheet
GROUP BY company_id
ORDER BY assets DESC
LIMIT 10;
SELECT company_name
FROM companies
WHERE website IS NULL;
SELECT company_id,
SUM(volume) AS total_volume
FROM stock_prices
GROUP BY company_id
ORDER BY total_volume DESC
LIMIT 10;
SELECT company_id,
AVG(return_on_equity_pct) AS avg_roe
FROM financial_ratios
GROUP BY company_id
ORDER BY avg_roe DESC
LIMIT 10;
SELECT company_id,
COUNT(*) AS reports
FROM documents
GROUP BY company_id
ORDER BY reports DESC;