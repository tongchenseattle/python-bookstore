# Research: Pseudo Bookstore Platform

## Decision 1: API framework for Python services

- Decision: Use FastAPI for both app-api and app-resourceAccess-api.
- Rationale: Strong request/response validation, OpenAPI generation, async support, and good fit for contract-first API development.
- Alternatives considered:
  - Flask: lighter, but requires more manual wiring for schema validation and API docs.
  - Django REST Framework: powerful, but heavier than needed for a focused layered service architecture.

## Decision 2: Data access strategy for local SQL Server

- Decision: Use SQLAlchemy ORM + Alembic migrations with SQL Server via ODBC driver.
- Rationale: Mature Python stack for SQL Server, controlled migrations, and clear repository abstraction in app-resourceAccess-api.
- Alternatives considered:
  - Raw SQL with pyodbc only: less abstraction and harder maintainability for evolving entities.
  - Tortoise ORM: weaker SQL Server ecosystem support compared to SQLAlchemy.

## Decision 3: Authentication boundary for public and admin flows

- Decision: Keep browsing/cart public, require sign-in for checkout submit and all admin routes.
- Rationale: Matches clarified requirements; balances friction and auditability while protecting mutable operations.
- Alternatives considered:
  - Full guest checkout: lower friction but weaker order traceability.
  - Sign-in before cart: stricter security but hurts storefront conversion.

## Decision 4: Frontend SSR and session strategy

- Decision: Use Next.js App Router SSR for storefront and admin pages with server-side session enforcement on protected routes.
- Rationale: Aligns with required SSR behavior and improves access control consistency for admin and checkout.
- Alternatives considered:
  - CSR-only frontend: weaker initial page performance and less robust route protection.
  - Static generation for all pages: unsuitable for protected/admin routes and dynamic catalog state.

## Decision 5: Concurrency and catalog integrity

- Decision: Use optimistic concurrency token/version on Book updates and block Category delete when linked books exist.
- Rationale: Prevents silent overwrite and preserves referential correctness in admin workflows.
- Alternatives considered:
  - Last-write-wins: simpler but loses edit safety.
  - Hard delete cascade for category -> books: unacceptable for catalog safety and admin clarity.

## Decision 6: Observability baseline

- Decision: Enforce structured JSON logs with propagated correlation ID header across app-ui -> app-api -> app-resourceAccess-api.
- Rationale: Satisfies constitution observability requirement and supports troubleshooting cross-service flows.
- Alternatives considered:
  - Per-service local logs without correlation: insufficient for end-to-end tracing.
  - Full distributed tracing stack from day one: valuable later, but heavy for initial pseudo-bookstore scope.

## Decision 7: Testing strategy by layer

- Decision: Use pytest for backend unit/integration/contract tests and Playwright for end-to-end UI flow verification.
- Rationale: Meets constitutional test gates and maps directly to storefront/admin user stories.
- Alternatives considered:
  - Unit-only backend tests: misses cross-layer behavior and contract drift.
  - Manual UI-only testing: slower feedback and non-repeatable quality gates.
