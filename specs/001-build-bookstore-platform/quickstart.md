# Quickstart: Pseudo Bookstore Platform

## Prerequisites

- Python 3.11+
- Node.js 20+
- SQL Server (local instance)
- ODBC Driver 18 for SQL Server

## 1) Create service/application folders

- app-ui (Next.js SSR)
- app-api (Python business API)
- app-resourceAccess-api (Python data-access API)
- sql/migrations (schema + seed scripts)

## 2) Configure environment variables

- app-ui:
  - APP_API_BASE_URL
  - AUTH_SECRET
- app-api:
  - RESOURCE_API_BASE_URL
  - APP_API_LOG_LEVEL
  - CORRELATION_HEADER_NAME (default: X-Correlation-ID)
- app-resourceAccess-api:
  - SQLSERVER_CONNECTION_STRING
  - RESOURCE_API_LOG_LEVEL

## 3) Initialize database

1. Create local database (example: bookstore_local).
2. Apply migrations from sql/migrations.
3. Seed admin user, sample categories, and sample published books.

## 4) Run services (development)

1. Start app-resourceAccess-api.
2. Start app-api.
3. Start app-ui.
4. Open storefront and admin routes in browser.

## 5) Smoke tests

- Storefront:
  - Browse categories and published books.
  - Add to cart.
  - Attempt checkout while signed out (expect redirect to sign-in).
  - Sign in and submit pseudo checkout (expect confirmation).
- Admin:
  - Sign in as admin.
  - Create/edit/delete category (delete blocked if linked books exist).
  - Create/edit/delete book.
  - Trigger concurrent update test and confirm conflict response.

## 6) Test execution targets

- Backend unit tests: app-api/tests/unit and app-resourceAccess-api/tests/unit
- Backend integration tests: app-api/tests/integration
- Contract tests: tests/contract against both OpenAPI contracts in specs/001-build-bookstore-platform/contracts
- UI e2e tests: app-ui/tests/e2e (public + admin critical paths)

## 7) Observability checks

- Verify correlation ID is present and propagated across all service logs for a single request.
- Verify error responses do not expose secrets.
- Verify health/readiness endpoints for both Python APIs.

## 8) Developer runbook commands

- app-ui:
  - `npm install`
  - `npm run dev`
  - `npm run test:e2e`
- app-api:
  - `pip install -e .[dev]`
  - `uvicorn src.main:app --reload --port 8000`
  - `pytest`
- app-resourceAccess-api:
  - `pip install -e .[dev]`
  - `uvicorn src.main:app --reload --port 8001`
  - `pytest`

## 9) Final validation checklist

- Run contract tests from `tests/contract`.
- Run integration tests for checkout, admin CRUD, and correlation propagation.
- Run Playwright e2e tests for storefront and admin flows.
- Verify `GET /health` and `GET /readiness` endpoints for both Python APIs.
