# Data Model: Pseudo Bookstore Platform

## Entity: UserAccount

- Description: Authenticated principal for admin and checkout submission.
- Fields:
  - id (uuid, primary key)
  - email (string, unique, required)
  - password_hash (string, required)
  - role (enum: admin, shopper, required)
  - is_active (boolean, default true)
  - created_at (datetime, required)
  - updated_at (datetime, required)
- Validation:
  - email must be valid format.
  - role must be one of defined enum values.
- State transitions:
  - active -> inactive (administrative disable)

## Entity: Category

- Description: Book grouping used for storefront navigation and admin organization.
- Fields:
  - id (uuid, primary key)
  - name (string, unique, required, 1..120 chars)
  - description (string, optional, max 1000 chars)
  - status (enum: active, inactive, required)
  - created_at (datetime, required)
  - updated_at (datetime, required)
- Validation:
  - name required and unique.
  - cannot be deleted when linked books exist.
- State transitions:
  - active <-> inactive

## Entity: Book

- Description: Catalog item visible on storefront when published.
- Fields:
  - id (uuid, primary key)
  - title (string, required, 1..200 chars)
  - publish_date (date, required)
  - price (decimal(10,2), required)
  - description (string, optional, max 4000 chars)
  - status (enum: draft, published, archived, required)
  - category_id (uuid, foreign key -> Category.id, required)
  - concurrency_version (rowversion or integer token, required)
  - created_at (datetime, required)
  - updated_at (datetime, required)
- Validation:
  - price must be >= 0.00 and normalized to two decimals.
  - category_id must reference existing category.
  - only status=published is visible in public storefront.
- State transitions:
  - draft -> published
  - published -> archived
  - archived -> draft (optional admin restore)

## Entity: Cart

- Description: Shopper basket before pseudo order submission.
- Fields:
  - id (uuid, primary key)
  - user_id (uuid, nullable; set once user authenticates for checkout)
  - session_id (string, required for unauthenticated cart continuity)
  - status (enum: active, converted, expired)
  - subtotal (decimal(10,2), required)
  - created_at (datetime, required)
  - updated_at (datetime, required)
- Validation:
  - cart must have at least one item before checkout attempt.
- State transitions:
  - active -> converted
  - active -> expired

## Entity: CartItem

- Description: Individual selected book and quantity in cart.
- Fields:
  - id (uuid, primary key)
  - cart_id (uuid, foreign key -> Cart.id, required)
  - book_id (uuid, foreign key -> Book.id, required)
  - quantity (integer, required, min 1)
  - unit_price (decimal(10,2), snapshot at add time)
  - line_total (decimal(10,2), derived)
- Validation:
  - quantity must be positive integer.
  - book must be published for public cart add.

## Entity: PseudoOrder

- Description: Mock checkout record created after authenticated submit.
- Fields:
  - id (uuid, primary key)
  - order_number (string, unique, required)
  - user_id (uuid, foreign key -> UserAccount.id, required)
  - cart_id (uuid, foreign key -> Cart.id, required)
  - total_amount (decimal(10,2), required)
  - status (enum: confirmed)
  - confirmed_at (datetime, required)
- Validation:
  - created only from authenticated checkout submit.
  - total_amount must equal sum of order line totals.

## Entity: PseudoOrderItem

- Description: Snapshot line items at order confirmation.
- Fields:
  - id (uuid, primary key)
  - pseudo_order_id (uuid, foreign key -> PseudoOrder.id, required)
  - book_id (uuid, required)
  - title_snapshot (string, required)
  - unit_price_snapshot (decimal(10,2), required)
  - quantity (integer, required)
  - line_total (decimal(10,2), required)

## Relationships

- Category 1 -> many Book
- Cart 1 -> many CartItem
- UserAccount 1 -> many Cart (optional before auth, required by checkout submit)
- Cart 1 -> 0..1 PseudoOrder
- PseudoOrder 1 -> many PseudoOrderItem

## Derived/Computed Rules

- Cart.subtotal = sum(CartItem.line_total)
- CartItem.line_total = quantity \* unit_price
- PseudoOrder.total_amount = sum(PseudoOrderItem.line_total)

## Non-Functional Data Constraints

- All monetary fields use decimal(10,2).
- Timestamps stored in UTC.
- Concurrency token required on Book updates to enforce optimistic locking.
