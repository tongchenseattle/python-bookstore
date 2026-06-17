USE bookstore_local;
GO

IF OBJECT_ID(N'dbo.user_accounts', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.user_accounts (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        email NVARCHAR(255) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        role NVARCHAR(20) NOT NULL,
        is_active BIT NOT NULL DEFAULT 1,
        created_at DATETIME2 NOT NULL,
        updated_at DATETIME2 NOT NULL
    );
END
GO

IF OBJECT_ID(N'dbo.categories', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.categories (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        name NVARCHAR(120) NOT NULL UNIQUE,
        description NVARCHAR(1000) NULL,
        status NVARCHAR(20) NOT NULL,
        created_at DATETIME2 NOT NULL,
        updated_at DATETIME2 NOT NULL
    );
END
GO

IF OBJECT_ID(N'dbo.books', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.books (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        title NVARCHAR(200) NOT NULL,
        publish_date DATE NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        description NVARCHAR(4000) NULL,
        status NVARCHAR(20) NOT NULL,
        category_id UNIQUEIDENTIFIER NOT NULL,
        concurrency_version ROWVERSION NOT NULL,
        created_at DATETIME2 NOT NULL,
        updated_at DATETIME2 NOT NULL,
        CONSTRAINT FK_books_categories FOREIGN KEY (category_id) REFERENCES dbo.categories(id)
    );
END
GO

IF OBJECT_ID(N'dbo.carts', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.carts (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        user_id UNIQUEIDENTIFIER NULL,
        session_id NVARCHAR(128) NOT NULL,
        status NVARCHAR(20) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        created_at DATETIME2 NOT NULL,
        updated_at DATETIME2 NOT NULL,
        CONSTRAINT FK_carts_users FOREIGN KEY (user_id) REFERENCES dbo.user_accounts(id)
    );
END
GO

IF OBJECT_ID(N'dbo.cart_items', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.cart_items (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        cart_id UNIQUEIDENTIFIER NOT NULL,
        book_id UNIQUEIDENTIFIER NOT NULL,
        quantity INT NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        line_total DECIMAL(10,2) NOT NULL,
        CONSTRAINT FK_cart_items_carts FOREIGN KEY (cart_id) REFERENCES dbo.carts(id),
        CONSTRAINT FK_cart_items_books FOREIGN KEY (book_id) REFERENCES dbo.books(id)
    );
END
GO

IF OBJECT_ID(N'dbo.pseudo_orders', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.pseudo_orders (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        order_number NVARCHAR(64) NOT NULL UNIQUE,
        user_id UNIQUEIDENTIFIER NOT NULL,
        cart_id UNIQUEIDENTIFIER NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status NVARCHAR(20) NOT NULL,
        confirmed_at DATETIME2 NOT NULL,
        CONSTRAINT FK_pseudo_orders_users FOREIGN KEY (user_id) REFERENCES dbo.user_accounts(id),
        CONSTRAINT FK_pseudo_orders_carts FOREIGN KEY (cart_id) REFERENCES dbo.carts(id)
    );
END
GO

IF OBJECT_ID(N'dbo.pseudo_order_items', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.pseudo_order_items (
        id UNIQUEIDENTIFIER PRIMARY KEY,
        pseudo_order_id UNIQUEIDENTIFIER NOT NULL,
        book_id UNIQUEIDENTIFIER NOT NULL,
        title_snapshot NVARCHAR(200) NOT NULL,
        unit_price_snapshot DECIMAL(10,2) NOT NULL,
        quantity INT NOT NULL,
        line_total DECIMAL(10,2) NOT NULL,
        CONSTRAINT FK_pseudo_order_items_orders FOREIGN KEY (pseudo_order_id) REFERENCES dbo.pseudo_orders(id)
    );
END
GO
