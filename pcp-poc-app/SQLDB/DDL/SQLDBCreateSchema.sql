USE [PCP_POC_DB]
DECLARE @schemaName NVARCHAR(128) = 'DPSN_DEMO'; -- Replace 'YourSchema' with the desired schema name

-- Check if the schema exists
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = @schemaName)
BEGIN
    -- If the schema does not exist, create it using dynamic SQL
    DECLARE @sql NVARCHAR(MAX) = N'CREATE SCHEMA ' + QUOTENAME(@schemaName) + N';';
    EXEC sp_executesql @sql;
END;