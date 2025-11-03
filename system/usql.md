
```bash
export USQL_SHOW_HOST_INFORMATION=false
usql "pg://postgres@127.0.0.1:5432/catsdb?sslmode=disable" -t -c "select * from ..." -A
```
