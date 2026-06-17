# Implementation Plan: Pseudo Bookstore Platform

**Branch**: `001-build-bookstore-platform` | **Date**: 2026-06-17 | **Spec**: `specs/001-build-bookstore-platform/spec.md`
**Input**: Feature specification from `specs/001-build-bookstore-platform/spec.md`

## Summary

Deliver a layered pseudo-bookstore platform with two user-facing portions:
public storefront (browse/catalog/cart/pseudo checkout) and admin management
portal (authenticated CRUD for categories and books). Architecture is explicitly
split into `app-ui` (Next.js SSR), `app-api` (Python business orchestration),
`app-resourceAccess-api` (Python data CRUD boundary), and local SQL Server
persistence, with contract-first APIs, correlation-aware observability, and
layered test gates.

## Technical Context

**Language/Version**: Python 3.11+ (backend APIs), TypeScript with Next.js 14+ (UI)  
**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy, Alembic, pyodbc/mssql driver, Next.js App Router, Playwright  
**Storage**: SQL Server (local instance) with migration scripts under `sql/migrations`  
**Testing**: pytest (unit/integration/contract), Playwright (UI e2e)  
**Target Platform**: Local development on Windows; browser-based web clients
**Project Type**: Layered web application (frontend + 2 backend services + SQL)  
**Performance Goals**: p95 catalog read response under 2s in expected local-team test load; stable admin CRUD under normal concurrency  
**Constraints**: Strict layer flow (`app-ui` -> `app-api` -> `app-resourceAccess-api` -> SQL), checkout requires authentication, no direct UI-to-data access  
**Scale/Scope**: Initial release for pseudo-commerce demo with one admin role, public catalog, cart, pseudo checkout, and catalog management

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Pre-Phase 0 Gate Review

- PASS: Layer boundaries preserved with enforced call chain from UI to business
  API to resource-access API to SQL Server.
- PASS: Contract-first outputs defined in `contracts/app-api.openapi.yaml` and
  `contracts/app-resourceAccess-api.openapi.yaml`.
- PASS: Auth expectations documented (admin routes protected; checkout submit
  requires sign-in).
- PASS: Test strategy includes layer-appropriate unit, integration, contract,
  and UI e2e coverage.
- PASS: Observability requirements captured (structured logs, correlation ID,
  health/readiness endpoints).

### Post-Phase 1 Re-Check

- PASS: Data model and contracts align to strict layer ownership and business vs
  data-access separation.
- PASS: CRUD and conflict handling are represented in both model and contracts
  (category-delete blocking and optimistic concurrency).
- PASS: Quickstart includes operational checks for auth boundaries,
  observability propagation, and service health.

## Project Structure

### Documentation (this feature)

```text
specs/001-build-bookstore-platform/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
app-ui/
├── src/
│   ├── app/
│   ├── components/
│   └── lib/
└── tests/

app-api/
├── src/
│   ├── api/
│   ├── services/
│   └── schemas/
└── tests/

app-resourceAccess-api/
├── src/
│   ├── api/
│   ├── repositories/
│   └── models/
└── tests/

sql/
└── migrations/
```

**Structure Decision**: Use the layered web app structure as the default for
this repository. `app-ui` handles SSR pages and auth flow, `app-api` owns
business orchestration/validation, `app-resourceAccess-api` encapsulates CRUD
and SQL interactions, and `sql/` contains migration artifacts.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| None      | N/A        | N/A                                  |
