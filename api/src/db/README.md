Quick Note on Migration Scripts:
* Always include both up and down scripts
* Script in format YYYY-MM-DD-{name}.{up/down}.sql
* Do not include transaction, application will execute in transaction
* Recommend always using IF EXISTS/IF NOT EXISTS
* DB is MySQL