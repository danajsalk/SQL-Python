# Using SQL with Python
<br>

## Summary
<br>
Accessing a SQL database is fairly easy with Python. Once SQL data is in Python, it is much easier to use for analyzing, reporting, or consuming into other projects. This folder has an example SQL to Python connection.

A sql to python connection uses
* server
* database
* query


## Creating Temp Tables
<br>
If you are using temp tables in your SQL queries, remember to use the phrase "SET NOCOUNT ON". See the example below. 

* When SET NOCOUNT is ON, the count (indicating the number of rows affected by a Transact-SQL statement) is not returned. When SET NOCOUNT is OFF, the count is returned. It is used with any SELECT, INSERT, UPDATE, DELETE statement.

* The setting of SET NOCOUNT is set at execute or run time and not at parse time.

* SET NOCOUNT ON improves stored procedure (SP) performance.

* Syntax: SET NOCOUNT { ON | OFF }

```
SET NOCOUNT ON

IF OBJECT_ID('tempdb.dbo.#table_name') IS NOT NULL
	DROP TABLE #table_name

CREATE TABLE #table_name (
	column_name1 INT PRIMARY KEY
	,column_name2 VARCHAR(50)
)

INSERT INTO #table_name

	VALUES (1, 'value1')
	, (2, 'value2')
```

```
SELECT
	*
FROM #table_name
```
