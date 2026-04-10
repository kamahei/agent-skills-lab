# Deliverables Matrix

Use this reference to decide which files to create for a new project. Start with the core pack. Add optional docs only when they reduce ambiguity or prevent implementation mistakes.

## Core Pack

Create these files for almost every greenfield project:

- `README.md`
  - Human-facing project summary, capability list, documentation map, and entry point for new contributors.
- `AGENTS.md`
  - Repository-level instructions for AI agents, including source-of-truth order, change boundaries, and validation expectations.
- `docs/project-overview.md`
  - Problem statement, goals, non-goals, stakeholders, constraints, and success signals.
- `docs/product-spec.md`
  - Functional requirements, user journeys, non-functional requirements, and out-of-scope items.
- `docs/architecture.md`
  - Proposed repository shape, components, module boundaries, data flow, and major technical decisions.
- `docs/data-model.md`
  - Domain entities, schema, invariants, relationships, lifecycle rules, and access patterns.
- `docs/implementation-plan.md`
  - Phase or slice order, dependencies, delivery strategy, and validation gates.
- `docs/task-breakdown.md`
  - Bounded implementation tasks that another AI agent can execute incrementally.
- `docs/acceptance-criteria.md`
  - Project-level and feature-level done criteria, edge cases, and validation targets.
- `docs/ai-implementation-guide.md`
  - AI-facing implementation brief that points to the right files, defines precedence, and explains how to proceed safely.

## Optional Docs

Add these files only when the project shape makes them useful:

- `docs/api-contracts.md`
  - Create when the project exposes HTTP, RPC, GraphQL, webhook, or event contracts that deserve their own source of truth.
- `docs/ui-spec.md`
  - Create when screen flows, component states, accessibility, responsive behavior, or UX details materially affect implementation.
- `docs/integrations.md`
  - Create when the project depends on third-party APIs, SaaS tools, payment systems, auth providers, queues, storage vendors, or webhooks.
- `docs/testing-strategy.md`
  - Create when the system has multiple layers, non-trivial reliability requirements, or enough complexity that testing guidance should be separated from the implementation plan.
- `docs/open-questions.md`
  - Create whenever important product or technical unknowns remain after the initial read-through.
- `docs/decision-log.md`
  - Create when the project is likely to revisit architectural or product tradeoffs and the reasoning should be tracked over time.

## Decision Rules

- If an optional topic would only add a short paragraph, fold it into `product-spec.md`, `architecture.md`, or `implementation-plan.md` instead of creating another file.
- If a missing answer would materially change the structure or schema, either ask the user or record the current default in `docs/open-questions.md`.
- If the repository already has a document that serves the same purpose, update it in place instead of creating a near-duplicate with a new name.
- Keep the file set small enough that a human and an AI agent can actually maintain it.

## Suggested Scaffold Command

```text
python .agents/skills/project-kickoff-docs/scripts/init_project_doc_pack.py --target . --project-name "Project Name" --include api-contracts,ui-spec
```
