# AGENTS.md

## Project Purpose

[Summarize the project in 1-2 paragraphs.]

## Source Of Truth

Use these files in this order when they overlap:

1. The current user request
2. `docs/product-spec.md`
3. `docs/architecture.md`
4. `docs/data-model.md`
5. `docs/implementation-plan.md`
6. `docs/task-breakdown.md`
7. `README.md`

If two files conflict, follow the higher-priority source and call out the mismatch.

## Default Workflow

- Read the relevant project docs before editing code.
- Start with the smallest implementation slice that delivers visible progress.
- Preserve the declared architecture and schema unless the user asks for a redesign.
- If a code change requires an architecture or schema change, update the docs in the same task.

## Boundaries

- Keep responsibilities separated according to `docs/architecture.md`.
- Keep domain rules and schema decisions aligned with `docs/data-model.md`.
- Do not introduce new dependencies, services, or infrastructure without justification.
- Do not silently widen scope beyond the requested capability or task slice.

## Validation

- Run the smallest meaningful validation for the files you changed.
- If validation cannot be run, state what was skipped and why.
- Check that behavior, docs, and acceptance criteria still match after the change.

## When To Ask Questions

Ask a short question before proceeding if a missing answer would materially change any of these:

- runtime or deployment model
- storage or schema choice
- authentication or authorization behavior
- external integration boundaries
- public API shape

Otherwise, proceed with the safest documented assumption and record it if needed.

## Output Rules

- Write created files in English unless explicitly instructed otherwise.
- Keep chat replies in the user's language.
- Keep explanations concise and practical.
- Call out assumptions, validation status, and any important tradeoffs.
