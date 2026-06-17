USE bookstore_local;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes WHERE name = 'IX_books_status_category'
)
BEGIN
    CREATE INDEX IX_books_status_category ON dbo.books (status, category_id);
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes WHERE name = 'IX_cart_items_cart_id'
)
BEGIN
    CREATE INDEX IX_cart_items_cart_id ON dbo.cart_items (cart_id);
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes WHERE name = 'IX_pseudo_orders_user_confirmed'
)
BEGIN
    CREATE INDEX IX_pseudo_orders_user_confirmed ON dbo.pseudo_orders (user_id, confirmed_at);
END
GO
