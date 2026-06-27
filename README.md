# Nifty100 Data Platform

## Overview

This project builds a complete ETL pipeline for Nifty100 company financial data.

The pipeline performs:

- Read Excel files
- Normalize data
- Load into SQLite
- Run Data Quality Checks
- Generate Audit Reports
- Execute SQL Analytics

---

## Project Structure

```
nifty100-data-platform
│
├── data/
│   └── raw/
│
├── db/
│   ├── nifty100.db
│   └── schema.sql
│
├── output/
│   ├── load_audit.csv
│   └── validation_failures.csv
│
├── sql/
│   └── exploratory_queries.sql
│
├── src/
│   └── etl/
│
├── tests/
│
└── README.md
```

---

## ETL Workflow

1. Read Excel Files

2. Normalize Data

3. Load SQLite Database

4. Validate Data

5. Generate Audit Report

6. Execute SQL Analytics

---

## Technologies

- Python
- Pandas
- SQLite
- Pytest
- SQL

---

## Run

Create Database

```
python -m src.etl.db_loader
```

Run Validation

```
python -m src.etl.validator
```

Run Complete ETL

```
python -m src.etl.loader
```

Run Tests

```
python -m pytest
```

---

## Outputs

Database

```
db/nifty100.db
```

Audit

```
output/load_audit.csv
```

Validation

```
output/validation_failures.csv
```

---

## Author

Jyothika Harshini