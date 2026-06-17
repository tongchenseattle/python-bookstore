<!--
Sync Impact Report
- Version change: template (unversioned) -> 1.0.0
- Modified principles:
	- [PRINCIPLE_1_NAME] -> I. Strict Layer Boundaries
	- [PRINCIPLE_2_NAME] -> II. Contract-First APIs
	- [PRINCIPLE_3_NAME] -> III. Secure-By-Default Authentication
	- [PRINCIPLE_4_NAME] -> IV. Test Gates By Layer
	- [PRINCIPLE_5_NAME] -> V. Observable, Operable Services
- Added sections:
	- Technology Standards & Data Rules
	- Delivery Workflow & Quality Gates
- Removed sections: None
- Templates requiring updates:
	- ✅ updated: .specify/templates/plan-template.md
	- ✅ updated: .specify/templates/spec-template.md
	- ✅ updated: .specify/templates/tasks-template.md
	- ✅ reviewed (no change required): .specify/extensions/git/commands/speckit.git.initialize.md
	- ✅ reviewed (no change required): .specify/extensions/git/commands/speckit.git.feature.md
	- ✅ reviewed (no change required): .specify/extensions/git/commands/speckit.git.commit.md
	- ✅ reviewed (no change required): .specify/extensions/git/commands/speckit.git.validate.md
	- ✅ reviewed (no change required): .specify/extensions/git/commands/speckit.git.remote.md
- Follow-up TODOs: None
-->

# Python Bookstore Constitution

## Core Principles

### I. Strict Layer Boundaries

The system MUST preserve a layered architecture with explicit responsibilities:
`app-ui` (Next.js SSR and auth flow), `app-api` (business orchestration and
validation), `app-resourceAccess-api` (data-access CRUD), and SQL persistence.
Direct access from `app-ui` to SQL or from `app-ui` to `app-resourceAccess-api`
is prohibited. Any boundary exception MUST be documented in the feature plan and
approved in review. Rationale: clear boundaries reduce coupling and make changes
safe and predictable.

### II. Contract-First APIs

Changes to API behavior MUST begin with explicit contracts (request/response,
errors, and auth rules) before implementation. `app-api` contracts MUST define
business semantics; `app-resourceAccess-api` contracts MUST define data access
semantics and stay internal to trusted services. Contract changes MUST include
versioning or compatibility notes. Rationale: contract-first delivery prevents
integration drift across UI, orchestration, and data-access layers.

### III. Secure-By-Default Authentication

All user-facing flows MUST enforce authenticated access by default, with any
public endpoint explicitly justified. Authentication and authorization decisions
MUST be centralized in `app-ui` and `app-api`; `app-resourceAccess-api` MUST
trust only service-to-service callers and MUST reject anonymous calls. Secrets
MUST never be hardcoded and MUST be environment-managed. Rationale: default
secure posture lowers exposure and simplifies auditability.

### IV. Test Gates By Layer

Every feature MUST include tests at the layer it changes: unit tests for local
logic, integration tests for inter-layer behavior, and contract tests when API
schemas or semantics change. A feature is not complete until required tests pass
in CI. Skipping tests requires explicit risk acceptance in the plan and review.
Rationale: layered test gates catch defects where they are introduced and where
they integrate.

### V. Observable, Operable Services

Backend services MUST emit structured logs with correlation IDs across request
chains from `app-ui` to `app-api` to `app-resourceAccess-api`. Errors MUST be
actionable and free of sensitive data. Health and readiness endpoints MUST exist
for each service. Rationale: production support depends on traceability and safe
diagnostics.

## Technology Standards & Data Rules

- Backend services MUST use Python.
- UI MUST use Next.js with SSR and authenticated user flow support.
- Persistent storage MUST use SQL with schema changes managed through reviewed,
  repeatable migrations.
- `app-api` owns business rules; `app-resourceAccess-api` owns CRUD and query
  composition without business policy leakage.
- Data model changes MUST document backward compatibility and migration impact.

## Delivery Workflow & Quality Gates

- Each specification MUST map scenarios and requirements to the correct layer.
- Each implementation plan MUST pass a constitution check before design and
  before implementation begins.
- Pull requests MUST include evidence for: contract updates (if any), test
  execution, security considerations, and observability impact.
- Reviews MUST block merges that violate layer boundaries, bypass auth controls,
  or omit required tests for changed behavior.

## Governance

This constitution is the source of truth for engineering decisions in this
repository. Amendments require: (1) a documented proposal, (2) impact analysis
across templates and workflows, and (3) maintainer approval.

Versioning policy for this constitution follows semantic versioning:

- MAJOR: incompatible governance or principle removals/redefinitions.
- MINOR: new principle/section or materially expanded requirements.
- PATCH: wording clarifications and non-semantic refinements.

Compliance review expectations:

- Every plan and PR MUST include a constitution compliance assessment.
- Violations MUST be explicitly listed with justification and mitigation.
- Periodic review cadence SHOULD be at least once per quarter to confirm that
  templates and workflow docs remain consistent with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-06-17 | **Last Amended**: 2026-06-17
