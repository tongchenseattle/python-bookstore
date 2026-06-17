# Feature Specification: Pseudo Bookstore Platform

**Feature Branch**: `001-build-bookstore-platform`  
**Created**: 2026-06-17  
**Status**: Draft  
**Input**: User description: "build a pseudo bookstore using a modern layered architecture with a public storefront and an admin application for authentication and catalog CRUD"

## Clarifications

### Session 2026-06-17

- Q: Must public users authenticate before pseudo checkout? -> A: Sign-in required at checkout
- Q: How should category deletion behave when books are linked? -> A: Block delete if linked books
- Q: How are concurrent admin edits to the same book resolved? -> A: Optimistic lock with retry
- Q: Which books are visible in the public storefront? -> A: Published books only
- Q: What price precision rule is required? -> A: Two-decimal currency rounding

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Browse and Buy Books in Public Storefront (Priority: P1)

A shopper visits the public web storefront, browses categories and books, views book details, and adds books to a cart to complete checkout in a pseudo purchase flow.

**Why this priority**: This is the core customer-facing value. Without this flow, there is no bookstore experience.

**Independent Test**: Can be fully tested by loading the storefront, filtering by category, opening a book detail page, adding items to a cart, and completing a mock checkout confirmation.

**Acceptance Scenarios**:

1. **Given** a shopper is on the public storefront, **When** they select a category, **Then** only books in that category are shown.
2. **Given** a shopper is viewing a book detail page, **When** they add the book to cart, **Then** the cart count and line item total update immediately.
3. **Given** a shopper has at least one item in cart, **When** they submit checkout, **Then** the system creates a pseudo order confirmation with order summary.
4. **Given** a shopper has items in cart but is not authenticated, **When** they initiate checkout submission, **Then** they are redirected to sign-in and return to checkout after authentication.

---

### User Story 2 - Admin Authentication and Catalog Management (Priority: P2)

An admin signs into the admin web app and manages categories and books using forms, including create, read, update, and delete operations.

**Why this priority**: Catalog maintenance is required to keep storefront content useful and current.

**Independent Test**: Can be fully tested by authenticating as an admin user and completing CRUD workflows for categories and books without using storefront checkout.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user accesses admin pages, **When** they request a protected route, **Then** they are redirected to sign-in.
2. **Given** an authenticated admin, **When** they create or edit a category, **Then** changes persist and are visible in category listings.
3. **Given** an authenticated admin, **When** they create or edit a book with title, publish date, price, and category, **Then** validation errors are shown for invalid input and valid data is saved.
4. **Given** an authenticated admin, **When** they delete a category or book, **Then** the system enforces deletion rules and returns a clear success or blocked response.

---

### User Story 3 - Layered Service Integrity and Operational Transparency (Priority: P3)

A development and operations team can verify that all user flows follow the intended layered architecture, and can trace requests across services for troubleshooting.

**Why this priority**: Ensures maintainability, safe scaling, and easier incident diagnosis as the application evolves.

**Independent Test**: Can be tested by running public and admin workflows while verifying request routing only follows approved service boundaries and logs include trace correlation across services.

**Acceptance Scenarios**:

1. **Given** a storefront or admin request, **When** it is processed, **Then** traffic flows through app-ui to app-api to app-resourceAccess-api to SQL with no direct bypass.
2. **Given** a request spans multiple services, **When** logs are reviewed, **Then** a shared correlation identifier links events across all involved services.

---

### Edge Cases

- Attempting admin access with expired session or invalid credentials.
- Creating a book with missing title, negative price, invalid publish date, or non-existent category.
- Deleting a category that still has associated books.
- Concurrent admin edits to the same book causing update conflicts.
- Public users requesting a book that was deleted or unpublished after page pre-render.
- Empty catalog states for new deployments with no categories or books.
- Rounding behavior when admin enters prices with more than two decimal places.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST provide a public storefront that lists categories and books and supports navigation to individual book details.
- **FR-002**: System MUST allow public users to add books to a cart, adjust quantities, and complete a pseudo checkout confirmation flow, requiring authentication at checkout submission.
- **FR-003**: System MUST provide an admin web app with authenticated access for catalog administration.
- **FR-004**: System MUST allow admins to create, read, update, and delete category records.
- **FR-005**: System MUST allow admins to create, read, update, and delete book records with fields including title, publish date, price, description, and category association.
- **FR-006**: System MUST validate admin form input and return clear, field-level errors for invalid data.
- **FR-007**: System MUST prevent unauthorized users from executing admin catalog operations.
- **FR-008**: System MUST enforce category-book referential rules so that invalid associations and unsafe deletes are blocked, including blocking category deletion while linked books exist.
- **FR-009**: System MUST expose business operations through app-api and data CRUD operations through app-resourceAccess-api.
- **FR-010**: System MUST persist catalog and pseudo-order data in SQL with consistent read/write behavior.
- **FR-011**: System MUST generate structured operational logs for requests and errors without leaking secrets or sensitive tokens.
- **FR-012**: System MUST propagate a request correlation identifier across app-ui, app-api, and app-resourceAccess-api for traceability.
- **FR-013**: System MUST detect concurrent admin updates to the same book via optimistic concurrency checks and return a conflict response with retry guidance.
- **FR-014**: System MUST expose only published books in the public storefront; unpublished or draft books MUST be hidden from public listing and detail routes.
- **FR-015**: System MUST normalize and persist book price values using two-decimal currency rounding rules.

### Key Entities _(include if feature involves data)_

- **UserAccount**: Represents a signed-in actor with role attributes such as admin or shopper and session state.
- **Category**: Represents a logical grouping of books with attributes such as name, description, and status.
- **Book**: Represents a sellable catalog item with title, publish date, price, description, stock indicator, publish status, and linked category.
- **Cart**: Represents a shopper basket containing selected books, quantities, and running totals.
- **PseudoOrder**: Represents a submitted mock purchase with line items, totals, timestamp, and confirmation identifier.

## Architecture Constraints _(mandatory)_

- **AC-001**: Changed layers for this feature are app-ui (public and admin web apps), app-api (business orchestration and validation), app-resourceAccess-api (resource CRUD), and SQL (persistent storage).
- **AC-002**: Request flow MUST remain app-ui -> app-api -> app-resourceAccess-api -> SQL for all business and data operations, with no direct UI-to-data access.
- **AC-003**: Contracts MUST be defined for public catalog and pseudo checkout endpoints, admin auth/session endpoints, and admin catalog CRUD endpoints, including request and response payload semantics, error responses, and authorization expectations.
- **AC-004**: Tests MUST include unit tests for each layer’s local logic, integration tests for cross-layer user flows (storefront and admin), and contract tests for endpoint behavior and validation rules.
- **AC-005**: Observability MUST include structured logs and cross-service correlation IDs for successful and failed requests, plus health/readiness exposure per service.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: At least 90% of first-time public users can browse to a book detail page and complete pseudo checkout in under 4 minutes during usability testing.
- **SC-002**: At least 95% of admin CRUD operations for categories and books complete successfully on first submission when valid data is entered.
- **SC-003**: 100% of unauthorized admin route requests are blocked and routed to sign-in or denied actions.
- **SC-004**: At least 95% of valid catalog page requests return visible content to users in under 2 seconds under expected team testing load.
- **SC-005**: 100% of sampled cross-service requests in test runs can be traced end-to-end using a shared correlation identifier.
- **SC-006**: 100% of attempted public checkout submissions by unauthenticated users are redirected to sign-in before order confirmation.
- **SC-007**: 100% of admin update conflicts for the same book return a non-destructive conflict response without silent overwrite.

## Assumptions

- Initial release supports one admin role type with full catalog management permissions.
- Payment processing is out of scope; checkout is a pseudo confirmation flow only.
- Inventory reservation, shipping, tax calculation, and discount engines are out of scope for this feature.
- The storefront and admin are web-only for this iteration; native mobile clients are out of scope.
- SQL schema migration and seed data capabilities are available for local and test environments.
- The resource-access layer is treated as CRUD-oriented and internal to service-to-service operations.
