-- Creates the local SQL Server database for bookstore development.
IF DB_ID(N'bookstore_local') IS NULL
BEGIN
    CREATE DATABASE bookstore_local;
END
GO
