-- create the schema if connected to the DB

USE [master]
GO
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'PCP_POC_DB')
BEGIN
    CREATE DATABASE [PCP_POC_DB]
END;


