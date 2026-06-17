USE bookstore_local;
GO

DECLARE @adminId UNIQUEIDENTIFIER = NEWID();
DECLARE @fictionId UNIQUEIDENTIFIER = NEWID();
DECLARE @bookId UNIQUEIDENTIFIER = NEWID();

IF NOT EXISTS (SELECT 1 FROM dbo.user_accounts WHERE email = 'admin@bookstore.local')
BEGIN
    INSERT INTO dbo.user_accounts (id, email, password_hash, role, is_active, created_at, updated_at)
    VALUES (@adminId, 'admin@bookstore.local', 'dev-password-hash-placeholder', 'admin', 1, SYSUTCDATETIME(), SYSUTCDATETIME());
END

IF NOT EXISTS (SELECT 1 FROM dbo.categories WHERE name = 'Fiction')
BEGIN
    INSERT INTO dbo.categories (id, name, description, status, created_at, updated_at)
    VALUES (@fictionId, 'Fiction', 'Fiction titles', 'active', SYSUTCDATETIME(), SYSUTCDATETIME());
END

IF NOT EXISTS (SELECT 1 FROM dbo.books WHERE title = 'Sample Book')
BEGIN
    INSERT INTO dbo.books (id, title, publish_date, price, description, status, category_id, created_at, updated_at)
    SELECT @bookId, 'Sample Book', CAST('2024-01-01' AS DATE), 19.99, 'Seed sample book', 'published', c.id, SYSUTCDATETIME(), SYSUTCDATETIME()
    FROM dbo.categories c
    WHERE c.name = 'Fiction';
END
GO
