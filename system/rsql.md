# rsql - Modern SQL Interface

`rsql` is a modern, feature-rich command-line SQL interface for querying databases, files, and cloud services. It provides a unified SQL experience across 20+ data sources with syntax highlighting and smart completions.

## Key Features

- Universal SQL interface for databases, files, and cloud services
- Supports 20+ databases and file formats
- Multiple output formats (ASCII, JSON, CSV, HTML, Markdown, etc.)
- Automatic compression handling (Gzip, Brotli, Bzip2, LZ4, XZ, Zstd)
- Rich interactive experience with syntax highlighting
- Cross-platform (Linux, macOS, Windows)

## Installation

```bash
# Linux/macOS (recommended)
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/theseus-rs/rsql/releases/latest/download/rsql_cli-installer.sh | sh

# Homebrew
brew install rsql

# Windows
irm https://github.com/theseus-rs/rsql/releases/latest/download/rsql_cli-installer.ps1 | iex

# Cargo
cargo install rsql_cli
```

## Connection URLs

### Databases

```bash
# PostgreSQL
rsql --url "postgresql://user:pass@localhost:5432/mydb"

# MySQL/MariaDB
rsql --url "mysql://user:pass@localhost:3306/mydb"

# SQLite
rsql --url "sqlite://path/to/database.db"

# DuckDB (in-memory analytics)
rsql --url "duckdb://"
rsql --url "duckdb://path/to/database.duckdb"

# SQL Server
rsql --url "mssql://user:pass@localhost:1433/mydb"

# ClickHouse
rsql --url "clickhouse://user:pass@localhost:9000/mydb"

# Snowflake
rsql --url "snowflake://user:pass@account.snowflakecomputing.com/mydb"
```

### File Formats

```bash
# CSV
rsql --url "csv://path/to/data.csv"
rsql --url "csv://https://example.com/data.csv"

# JSON
rsql --url "json://path/to/data.json"

# Parquet
rsql --url "parquet://path/to/data.parquet"

# Excel
rsql --url "excel://path/to/data.xlsx"

# Arrow
rsql --url "arrow://path/to/data.arrow"

# Avro
rsql --url "avro://path/to/data.avro"

# XML
rsql --url "xml://path/to/data.xml"

# YAML
rsql --url "yaml://path/to/data.yaml"
```

### Cloud/Remote Sources

```bash
# S3
rsql --url "s3://bucket/path/to/file.parquet"

# HTTP/HTTPS
rsql --url "https://example.com/data.csv"

# FlightSQL
rsql --url "flightsql://host:port"
```

## Command-Line Options

```bash
# Execute query directly
rsql --url "postgresql://localhost/mydb" --query "SELECT version()"
rsql --url "csv://data.csv" -q "SELECT * FROM data WHERE value > 100"

# Output formats
rsql --url "duckdb://" --format json -q "SELECT 1 as num"
rsql --url "sqlite://db.sqlite" --format csv -q "SELECT * FROM users"
rsql --url "postgresql://localhost/mydb" --format html -q "SELECT * FROM orders"

# Available formats: ascii (default), csv, json, html, markdown, xml, yaml

# Execute SQL from file
rsql --url "postgresql://localhost/mydb" --file queries.sql

# Interactive mode (default when no query specified)
rsql --url "postgresql://localhost/mydb"

# Note: rsql uses standard SQL only - psql meta-commands (\l, \dt, \d) are NOT supported
```

## Environment Variables

```bash
# PostgreSQL compatibility
export PGHOST=localhost
export PGPORT=5432
export PGUSER=myuser
export PGPASSWORD=mypassword
export PGDATABASE=mydb

# Then connect without full URL
rsql --url "postgresql://"
```

## Practical Examples

### Query CSV Files

```bash
# Query local CSV
rsql --url "csv://sales.csv" -q "SELECT product, SUM(amount) as total FROM sales GROUP BY product"

# Query remote CSV
rsql --url "csv://https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv" \
  -q "SELECT Country, MAX(Confirmed) as max_cases FROM data WHERE Country LIKE 'United%' GROUP BY Country"
```

### In-Memory Analytics with DuckDB

```bash
# Load and analyze multiple files
rsql --url "duckdb://" -q "
  CREATE TABLE sales AS SELECT * FROM 'sales_*.parquet';
  SELECT region, SUM(revenue) FROM sales GROUP BY region;
"

# Join CSV and Parquet files
rsql --url "duckdb://" -q "
  SELECT c.name, s.total
  FROM 'customers.csv' c
  JOIN 'sales.parquet' s ON c.id = s.customer_id
"
```

### Database Migrations

```bash
# Export PostgreSQL to Parquet
rsql --url "postgresql://localhost/source_db" \
  --format parquet \
  -q "SELECT * FROM large_table" > large_table.parquet

# Import Parquet to DuckDB
rsql --url "duckdb://analytics.db" \
  -q "CREATE TABLE large_table AS SELECT * FROM 'large_table.parquet'"
```

### JSON Data Analysis

```bash
# Query nested JSON
rsql --url "json://data.json" -q "
  SELECT
    json_extract(data, '$.user.name') as name,
    json_extract(data, '$.user.age') as age
  FROM data
  WHERE json_extract(data, '$.user.active') = true
"
```

### Excel Reports

```bash
# Analyze Excel spreadsheet
rsql --url "excel://report.xlsx" -q "
  SELECT
    Department,
    COUNT(*) as employees,
    AVG(Salary) as avg_salary
  FROM Sheet1
  GROUP BY Department
"
```

## Output Formatting

```bash
# ASCII table (default)
rsql --url "sqlite://db.sqlite" -q "SELECT * FROM users LIMIT 5"

# JSON for API responses
rsql --url "postgresql://localhost/api_db" \
  --format json \
  -q "SELECT id, name, email FROM users WHERE active = true"

# CSV for data export
rsql --url "mysql://localhost/mydb" \
  --format csv \
  -q "SELECT * FROM orders WHERE date >= '2024-01-01'" > orders_2024.csv

# HTML for reports
rsql --url "duckdb://" \
  --format html \
  -q "SELECT * FROM 'monthly_report.parquet'" > report.html

# Markdown for documentation
rsql --url "sqlite://stats.db" \
  --format markdown \
  -q "SELECT metric, value FROM statistics"
```

## Compressed File Support

```bash
# Automatically handles compressed files
rsql --url "csv://data.csv.gz"       # Gzip
rsql --url "json://data.json.br"     # Brotli
rsql --url "parquet://data.parquet.bz2"  # Bzip2
rsql --url "csv://data.csv.lz4"      # LZ4
rsql --url "json://data.json.xz"     # XZ
rsql --url "csv://data.csv.zst"      # Zstd
```

## Tips and Tricks

### Aliases for Common Queries

```bash
# Add to ~/.bashrc or ~/.zshrc
alias rsql-csv='rsql --url "csv://"'
alias rsql-json='rsql --url "json://"'
alias rsql-duck='rsql --url "duckdb://"'
alias rsql-local='rsql --url "postgresql://localhost/mydb"'
```

### Pipeline Integration

```bash
# Pipe data through rsql
cat data.csv | rsql --url "csv://-" -q "SELECT * WHERE value > 100"

# Chain with other tools
rsql --url "postgresql://localhost/db" --format json -q "SELECT * FROM users" | jq '.[] | .email'

# Generate reports
rsql --url "duckdb://" --format markdown -q "
  SELECT date, revenue, expenses
  FROM 'financial_*.parquet'
  ORDER BY date DESC
" | pandoc -o report.pdf
```

### Quick Data Exploration

```bash
# Get schema information
rsql --url "parquet://data.parquet" -q "DESCRIBE SELECT * FROM data"

# Sample data
rsql --url "csv://large_file.csv" -q "SELECT * FROM data LIMIT 10"

# Basic statistics
rsql --url "json://data.json" -q "
  SELECT
    COUNT(*) as count,
    MIN(value) as min,
    MAX(value) as max,
    AVG(value) as avg
  FROM data
"
```

## Supported Data Sources

### Databases
- PostgreSQL
- MySQL / MariaDB
- SQLite
- DuckDB
- SQL Server (MSSQL)
- ClickHouse
- CockroachDB
- Redshift
- Snowflake
- LibSQL
- Apache Datafusion
- Google BigQuery

### File Formats
- CSV
- JSON / JSONL
- Parquet
- Arrow / Arrow IPC
- Avro
- Excel (XLSX/XLS)
- XML
- YAML
- ORC

### Cloud/Remote
- S3
- FlightSQL
- HTTP/HTTPS endpoints

## More Information

- GitHub: https://github.com/theseus-rs/rsql
- Documentation: https://theseus-rs.github.io/rsql/rsql_cli/book/