#### Quick Note on Migration Scripts:
* Always include both up and down scripts
* Script in format YYYY-MM-DD-{name}.{up/down}.sql
* Do not include transaction, application will execute in transaction
* Recommend always using IF EXISTS/IF NOT EXISTS
* DB is MySQL


# Developer's Note

## Gotcha's with Mysql Connector
Mysql Connector for python is stupid when it comes to executing multiple statements.
cursor.execute can only handle one statement unless multi=True is specified in
the function call - however MYSQL's own documentation does not recommend it

"If multi is set to True, execute() is able to execute multiple statements specified in the operation string. It returns an iterator that enables processing the result of each statement. However, using parameters does not work well in this case, and it is usually a good idea to execute each statement on its own."
- https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

## General Notes
Be careful of return types, opening a connection with dictionary=True will return results as 
dictionary rather than default tuple. This is currently used in some but not all functions in
db_utils.py. 
