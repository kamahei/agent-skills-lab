# AI Implementation Guide

## Mission

[Summarize what an AI agent is expected to build.]

## Read Order

1. `docs/project-overview.md`
2. `docs/product-spec.md`
3. `docs/architecture.md`
4. `docs/data-model.md`
5. `docs/implementation-plan.md`
6. `docs/task-breakdown.md`
7. `docs/acceptance-criteria.md`
8. `AGENTS.md`

## Source Of Truth Precedence

1. Current user request
2. `docs/product-spec.md`
3. `docs/architecture.md`
4. `docs/data-model.md`
5. `docs/task-breakdown.md`
6. `README.md`

If two files conflict, follow the higher-priority file and report the mismatch.

## Build Order

- [Start with the smallest vertical slice]
- [Implement foundational data or contract work before dependent features]
- [Keep documentation synchronized when architecture or schema changes]

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Validation Expectations

- [Tests, type checks, linting, or manual verification]
- [Minimum checks required per task]

## Stop And Ask Conditions

- [Architecture boundary would change]
- [Schema or storage model would change]
- [Auth, security, or external interface behavior would change]
