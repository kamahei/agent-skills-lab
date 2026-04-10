# Structure And Schema Guide

Use this guide after reading the project brief and before writing `architecture.md` or `data-model.md`.

## 1. Extract the real design signals

Read for these inputs first:

- primary users or operators
- main user journeys
- core capabilities
- domain objects or records
- integrations or external systems
- trust boundaries, auth rules, or privacy requirements
- scale, latency, or reliability expectations
- explicit constraints such as stack, hosting, or deadlines

If a requirement is only implied by marketing language, keep it as an assumption until a stronger source confirms it.

## 2. Choose the smallest project shape that fits

Prefer the least complicated shape that still supports the requested capabilities:

- UI-only or content-heavy product
  - One app with feature folders is usually enough.
- Full-stack product
  - Separate the user-facing app from the API or backend boundary.
  - Keep shared types or contracts in a dedicated shared location only if both sides truly need them.
- Backend service or worker
  - Keep entrypoints, domain logic, storage access, and integration adapters clearly separated.
- Library, SDK, or CLI
  - Optimize for a clean `src/`, tests, examples, and usage docs rather than web-style layering.

Avoid microservices, event buses, plugin systems, or deep layering unless the spec clearly requires them.

## 3. Derive module boundaries

Define boundaries from responsibilities, not from framework fashion:

- entrypoints
  - routes, commands, jobs, or UI screens that receive input
- application or orchestration layer
  - workflow coordination and use-case execution
- domain layer
  - entities, rules, invariants, and decisions that should not depend on transport or UI
- infrastructure layer
  - database, filesystem, external API, cache, queue, or cloud adapters

When writing `architecture.md`, state which directories or modules own which responsibility. Do not let the same business rule live in multiple layers without a clear reason.

## 4. Derive the first-pass schema

For every important entity, capture:

- purpose
- canonical identifier
- important fields
- relationships
- lifecycle states
- ownership and permissions
- validation rules
- read and write paths
- query or indexing needs

Keep the schema aligned with the actual access patterns. Do not normalize or denormalize purely out of habit.

## 5. Record assumptions and open questions

When a detail is missing:

- choose a safe default if implementation can still proceed
- record the assumption explicitly in `project-overview.md` or `open-questions.md`
- avoid pretending the choice was user-approved when it was only inferred

If the unknown affects the whole architecture, data model, or deployment model, ask before locking it in.

## 6. Check for cross-file consistency

Before finalizing the doc pack:

- every capability in `product-spec.md` should map to components in `architecture.md`
- every durable domain concept should appear in `data-model.md`
- every major implementation slice in `implementation-plan.md` should be reflected in `task-breakdown.md`
- acceptance criteria should cover the same scope that the architecture and plan claim to support
