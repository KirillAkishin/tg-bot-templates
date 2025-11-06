-- example

SELECT 
    table_schema as schema,
    table_name as table,
    {},
    COUNT(table_catalog) as columns
FROM INFORMATION_SCHEMA.columns
GROUP BY table_schema, table_name
ORDER BY table_schema, table_name