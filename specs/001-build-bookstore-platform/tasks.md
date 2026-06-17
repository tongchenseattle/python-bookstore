# Tasks: Pseudo Bookstore Platform

**Input**: Design documents from `/specs/001-build-bookstore-platform/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are required for this feature by architecture constraints (unit, integration, contract, and UI e2e coverage).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base toolchain setup for all services

- [x] T001 Create layered project folders and baseline README files in app-ui/README.md
- [x] T002 Initialize Next.js app dependencies and scripts in app-ui/package.json
- [x] T003 Initialize app-api Python project and dependencies in app-api/pyproject.toml
- [x] T004 Initialize app-resourceAccess-api Python project and dependencies in app-resourceAccess-api/pyproject.toml
- [x] T005 [P] Configure frontend lint/test settings in app-ui/eslint.config.mjs
- [x] T006 [P] Configure backend lint/test settings in app-api/pytest.ini
- [x] T007 [P] Configure backend lint/test settings in app-resourceAccess-api/pytest.ini
- [x] T008 Configure local SQL Server bootstrap script in sql/migrations/000_create_database.sql

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create initial schema migration for core entities in sql/migrations/001_init_bookstore.sql
- [x] T010 Create seed data script for admin user and sample catalog in sql/migrations/001_seed_bookstore.sql
- [x] T011 [P] Implement app-api settings and environment loader in app-api/src/core/settings.py
- [x] T012 [P] Implement app-resourceAccess-api settings and environment loader in app-resourceAccess-api/src/core/settings.py
- [x] T013 [P] Implement SQLAlchemy engine/session setup in app-resourceAccess-api/src/core/database.py
- [x] T014 Define foundational ORM models for Category and Book in app-resourceAccess-api/src/models/catalog.py
- [x] T015 Define foundational ORM models for Cart, CartItem, PseudoOrder, and PseudoOrderItem in app-resourceAccess-api/src/models/order.py
- [x] T016 [P] Implement app-api service client for app-resourceAccess-api in app-api/src/clients/resource_access_client.py
- [x] T017 [P] Implement app-api authentication/session dependency in app-api/src/api/dependencies/auth.py
- [x] T018 [P] Implement app-ui server-side session utility in app-ui/src/lib/auth.ts
- [x] T019 [P] Implement base router and exception handling in app-api/src/main.py
- [x] T020 [P] Implement base router and exception handling in app-resourceAccess-api/src/main.py
- [x] T021 Implement foundational app-api schemas for catalog and checkout payloads in app-api/src/schemas/storefront.py
- [x] T022 Implement foundational app-api schemas for admin payloads in app-api/src/schemas/admin.py
- [x] T023 Configure contract test harness and fixtures in tests/contract/conftest.py
- [x] T024 Add boundary enforcement for app-ui to call only app-api in app-ui/src/lib/api-client.ts

**Checkpoint**: Foundation ready; user story implementation can begin

---

## Phase 3: User Story 1 - Browse and Buy Books in Public Storefront (Priority: P1) MVP

**Goal**: Deliver public storefront browsing, cart operations, and authenticated pseudo checkout

**Independent Test**: A user can browse categories/books, add cart items, get redirected to sign-in on checkout when unauthenticated, then complete pseudo checkout after authentication

### Tests for User Story 1

- [x] T025 [P] [US1] Add app-api contract tests for catalog, cart, and checkout in tests/contract/test_app_api_storefront.py
- [x] T026 [P] [US1] Add app-api integration test for storefront-to-checkout flow in app-api/tests/integration/test_storefront_checkout_flow.py
- [x] T027 [P] [US1] Add UI e2e test for browse/cart/checkout redirect flow in app-ui/tests/e2e/storefront-checkout.spec.ts

### Implementation for User Story 1

- [x] T028 [P] [US1] Implement category read repository methods in app-resourceAccess-api/src/repositories/category_repository.py
- [x] T029 [P] [US1] Implement book read repository methods with published filter in app-resourceAccess-api/src/repositories/book_repository.py
- [x] T030 [P] [US1] Implement cart and pseudo-order repository methods in app-resourceAccess-api/src/repositories/order_repository.py
- [x] T031 [US1] Implement storefront/internal routes for catalog, cart, and order persistence in app-resourceAccess-api/src/api/routes/storefront_internal.py
- [x] T032 [US1] Implement catalog orchestration service in app-api/src/services/catalog_service.py
- [x] T033 [US1] Implement cart orchestration service in app-api/src/services/cart_service.py
- [x] T034 [US1] Implement checkout orchestration service with auth gate in app-api/src/services/checkout_service.py
- [x] T035 [US1] Implement public storefront and checkout routes in app-api/src/api/routes/storefront.py
- [x] T036 [US1] Implement storefront category and book listing page in app-ui/src/app/page.tsx
- [x] T037 [US1] Implement public book detail page in app-ui/src/app/books/[bookId]/page.tsx
- [x] T038 [US1] Implement cart page and quantity updates in app-ui/src/app/cart/page.tsx
- [x] T039 [US1] Implement checkout page with sign-in redirect behavior in app-ui/src/app/checkout/page.tsx
- [x] T040 [US1] Add checkout success and failure structured logs in app-api/src/services/checkout_service.py

**Checkpoint**: User Story 1 is fully functional and independently testable

---

## Phase 4: User Story 2 - Admin Authentication and Catalog Management (Priority: P2)

**Goal**: Deliver authenticated admin workflows for category and book CRUD with validation and deletion rules

**Independent Test**: An admin signs in, manages categories/books with form validation, sees delete blocking for linked categories, and updates data visible to storefront

### Tests for User Story 2

- [x] T041 [P] [US2] Add app-api contract tests for admin endpoints in tests/contract/test_app_api_admin_catalog.py
- [x] T042 [P] [US2] Add app-api integration tests for admin CRUD and category delete blocking in app-api/tests/integration/test_admin_catalog_crud.py
- [x] T043 [P] [US2] Add UI e2e test for admin authentication and catalog forms in app-ui/tests/e2e/admin-catalog.spec.ts

### Implementation for User Story 2

- [x] T044 [P] [US2] Implement category write and delete-block repository logic in app-resourceAccess-api/src/repositories/category_repository.py
- [x] T045 [P] [US2] Implement book write repository logic with price normalization in app-resourceAccess-api/src/repositories/book_repository.py
- [x] T046 [US2] Implement internal admin CRUD routes in app-resourceAccess-api/src/api/routes/admin_internal.py
- [x] T047 [US2] Implement admin authorization dependency in app-api/src/api/dependencies/admin_auth.py
- [x] T048 [US2] Implement admin catalog orchestration service in app-api/src/services/admin_catalog_service.py
- [x] T049 [US2] Implement app-api admin catalog routes in app-api/src/api/routes/admin.py
- [x] T050 [US2] Implement admin sign-in page and session submit flow in app-ui/src/app/admin/sign-in/page.tsx
- [x] T051 [US2] Implement admin category list/create/edit page in app-ui/src/app/admin/categories/page.tsx
- [x] T052 [US2] Implement admin book list/create/edit page in app-ui/src/app/admin/books/page.tsx
- [x] T053 [US2] Add admin form validation and conflict messaging component in app-ui/src/components/admin/AdminCatalogForm.tsx

**Checkpoint**: User Stories 1 and 2 are independently functional

---

## Phase 5: User Story 3 - Layered Service Integrity and Operational Transparency (Priority: P3)

**Goal**: Enforce operational traceability, health visibility, and optimistic concurrency behavior across layers

**Independent Test**: Requests can be traced end-to-end with correlation IDs, health/readiness endpoints validate service status, and concurrent admin book updates return conflict responses without silent overwrite

### Tests for User Story 3

- [x] T054 [P] [US3] Add resource API contract tests for concurrency and conflict responses in tests/contract/test_resource_api_contracts.py
- [x] T055 [P] [US3] Add integration test for correlation ID propagation across services in app-api/tests/integration/test_correlation_propagation.py
- [x] T056 [P] [US3] Add integration test for optimistic book update conflict handling in app-api/tests/integration/test_book_concurrency_conflict.py

### Implementation for User Story 3

- [x] T057 [US3] Implement correlation ID middleware for app-api in app-api/src/middleware/correlation.py
- [x] T058 [US3] Implement correlation ID middleware for app-resourceAccess-api in app-resourceAccess-api/src/middleware/correlation.py
- [x] T059 [US3] Implement structured logging formatter/configuration in app-api/src/core/logging.py
- [x] T060 [US3] Implement structured logging formatter/configuration in app-resourceAccess-api/src/core/logging.py
- [x] T061 [US3] Implement If-Match optimistic concurrency enforcement in app-resourceAccess-api/src/api/routes/admin_internal.py
- [x] T062 [US3] Implement health/readiness routes for app-api in app-api/src/api/routes/health.py
- [x] T063 [US3] Implement health/readiness routes for app-resourceAccess-api in app-resourceAccess-api/src/api/routes/health.py
- [x] T064 [US3] Implement correlation header forwarding in app-ui API client in app-ui/src/lib/api-client.ts

**Checkpoint**: All user stories are independently functional with operational guarantees

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final hardening and cross-story validation

- [x] T065 [P] Update implementation and runbook notes in specs/001-build-bookstore-platform/quickstart.md
- [x] T066 [P] Add CI workflow for layered test suites in .github/workflows/ci.yml
- [x] T067 Apply security hardening defaults for environment variables in app-api/.env.example
- [x] T068 [P] Add SQL indexes for catalog and order query paths in sql/migrations/002_catalog_indexes.sql
- [x] T069 Run end-to-end quickstart validation checklist in specs/001-build-bookstore-platform/checklists/requirements.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Story Phases (Phase 3-5)**: Depend on Foundational completion
- **Polish (Phase 6)**: Depends on desired user stories completion

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on US2 or US3
- **US2 (P2)**: Starts after Phase 2; can reuse US1 patterns but remains independently testable
- **US3 (P3)**: Starts after Phase 2; verifies cross-cutting guarantees while remaining independently testable

### Within Each User Story

- Tests are created before implementation tasks
- Repository/model updates precede service orchestration
- Service orchestration precedes API route wiring
- API routes precede UI integration where applicable

## Parallel Opportunities

- Setup tasks marked [P] (T005-T007) can run concurrently
- Foundational tasks marked [P] (T011-T013, T016-T020) can run concurrently once schema baseline exists
- US1 tests (T025-T027) can run in parallel
- US1 repository tasks (T028-T030) can run in parallel
- US2 tests (T041-T043) can run in parallel
- US2 repository tasks (T044-T045) can run in parallel
- US3 tests (T054-T056) can run in parallel
- Polish tasks marked [P] (T065, T066, T068) can run concurrently

---

## Parallel Example: User Story 1

```bash
# Parallel test authoring for US1
Task: "T025 [US1] Add app-api contract tests for catalog, cart, and checkout in tests/contract/test_app_api_storefront.py"
Task: "T026 [US1] Add app-api integration test for storefront-to-checkout flow in app-api/tests/integration/test_storefront_checkout_flow.py"
Task: "T027 [US1] Add UI e2e test for browse/cart/checkout redirect flow in app-ui/tests/e2e/storefront-checkout.spec.ts"

# Parallel repository implementation for US1
Task: "T028 [US1] Implement category read repository methods in app-resourceAccess-api/src/repositories/category_repository.py"
Task: "T029 [US1] Implement book read repository methods with published filter in app-resourceAccess-api/src/repositories/book_repository.py"
Task: "T030 [US1] Implement cart and pseudo-order repository methods in app-resourceAccess-api/src/repositories/order_repository.py"
```

## Parallel Example: User Story 2

```bash
# Parallel test authoring for US2
Task: "T041 [US2] Add app-api contract tests for admin endpoints in tests/contract/test_app_api_admin_catalog.py"
Task: "T042 [US2] Add app-api integration tests for admin CRUD and category delete blocking in app-api/tests/integration/test_admin_catalog_crud.py"
Task: "T043 [US2] Add UI e2e test for admin authentication and catalog forms in app-ui/tests/e2e/admin-catalog.spec.ts"

# Parallel repository implementation for US2
Task: "T044 [US2] Implement category write and delete-block repository logic in app-resourceAccess-api/src/repositories/category_repository.py"
Task: "T045 [US2] Implement book write repository logic with price normalization in app-resourceAccess-api/src/repositories/book_repository.py"
```

## Parallel Example: User Story 3

```bash
# Parallel test authoring for US3
Task: "T054 [US3] Add resource API contract tests for concurrency and conflict responses in tests/contract/test_resource_api_contracts.py"
Task: "T055 [US3] Add integration test for correlation ID propagation across services in app-api/tests/integration/test_correlation_propagation.py"
Task: "T056 [US3] Add integration test for optimistic book update conflict handling in app-api/tests/integration/test_book_concurrency_conflict.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2
2. Complete all US1 tasks (Phase 3)
3. Validate storefront browsing/cart/checkout redirect/authenticated submit
4. Demo MVP before starting admin and cross-cutting enhancements

### Incremental Delivery

1. Foundation complete (Phase 1-2)
2. Deliver US1 and validate independently
3. Deliver US2 and validate independently
4. Deliver US3 and validate independently
5. Execute polish and full quickstart validation

### Parallel Team Strategy

1. Team works jointly on Setup + Foundational phases
2. After Phase 2 checkpoint:
   - Engineer A: US1 implementation
   - Engineer B: US2 implementation
   - Engineer C: US3 observability/concurrency work
3. Merge with contract and integration test gates before polish phase

---

## Notes

- Task IDs are sequential and execution-ordered (T001-T069)
- [P] indicates no dependency on incomplete tasks in other files
- [USx] labels appear only in user story phases for traceability
- Each user story includes independent test criteria and dedicated test tasks
- Avoid cross-story coupling that breaks independent validation
