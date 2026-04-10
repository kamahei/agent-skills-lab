---
name: project-kickoff-docs
description: Turn a project brief, rough requirements, issue, PRD, or specification into an implementation-ready documentation pack for a new project. Use when starting a greenfield repository or bootstrapping an unfinished repo and Codex needs to read the project overview, decide the initial structure and schema, write a human-facing README.md, create AGENTS.md for AI agents, and produce docs/ files such as overview, product spec, architecture, data model, implementation plan, task breakdown, and AI implementation guidance.
---

# Project Kickoff Docs

## Activation

- Use this skill when the user wants to start a project from notes, a spec, or a project overview instead of from existing code.
- Use it when the repository is empty, lightly scaffolded, or missing the documents needed before implementation can start.
- Use it for greenfield projects, MVP bootstraps, internal tools, prototypes that need to become real projects, and handoff-ready project packs for other AI agents.
- Do not use it for narrow edits to an already-established codebase unless the user explicitly asks to re-baseline or regenerate the project docs.

## Inputs

- Expected context: a project brief, specification, issue, ticket, PRD, meeting notes, or a directory with source material that describes the project to build.
- Helpful details: preferred stack, deployment target, auth model, data or storage needs, API style, integrations, non-functional requirements, and any explicit constraints on scope or deadlines.
- If the specification is fragmented across multiple files, read all relevant local documents before drafting anything.

## Quick Start

1. Read the source material and extract the product goal, users, core capabilities, constraints, non-goals, and unknowns.
2. Decide the project shape and the initial schema. Use `references/structure-and-schema-guide.md` to choose a minimal architecture and data model that fit the requested scope.
3. Choose the documentation pack. Start with the core files, then add optional docs from `references/deliverables.md` only when the project truly needs them.
4. Scaffold the file set with `scripts/init_project_doc_pack.py` or create the files manually if the repository already has overlapping docs.
5. Fill the docs in this order:
   - `docs/project-overview.md`
   - `docs/product-spec.md`
   - `docs/architecture.md`
   - `docs/data-model.md`
   - optional domain-specific docs such as API, UI, integrations, or testing strategy
   - `docs/implementation-plan.md`
   - `docs/task-breakdown.md`
   - `docs/acceptance-criteria.md`
   - `docs/ai-implementation-guide.md`
   - `README.md`
   - `AGENTS.md`
6. Cross-check names, scope, directory conventions, assumptions, and acceptance criteria across every file before finishing.

## Workflow

### 1. Build the project understanding

- Distinguish confirmed requirements from assumptions.
- Normalize vague requests into concrete capabilities, user flows, constraints, and success criteria.
- If a critical decision such as platform, runtime, or deployment model is unknown and it would materially change the structure, ask one short question. Otherwise, choose a conservative default and record it explicitly.

### 2. Decide structure and schema

- Prefer the smallest architecture that can support the known requirements cleanly.
- Separate project shape decisions from implementation details:
  - `architecture.md` owns repository structure, module boundaries, and system flow.
  - `data-model.md` owns domain entities, schema, invariants, and access patterns.
- Avoid speculative microservices, event buses, or heavyweight layering unless the requirements clearly justify them.
- When the spec is incomplete, write down open questions and safe defaults rather than inventing hidden requirements.

### 3. Create the human-facing docs

- Write `README.md` for a human reader who needs to understand the project quickly.
- Keep the README concise: purpose, capabilities, technology direction, doc map, and getting-started expectations.
- Put the detailed behavior in `docs/` rather than bloating the README.

### 4. Create the AI-facing docs

- Write `AGENTS.md` as durable working instructions for AI agents in the repository.
- Write `docs/ai-implementation-guide.md` as the implementation brief that tells an AI agent what to read first, what to treat as the source of truth, what order to build in, and what boundaries not to cross.
- Write `docs/task-breakdown.md` as a sequence of bounded, independently implementable tasks. Each task should have scope, dependencies, and a validation target.

### 5. Validate the pack

- Make sure every required capability in the spec appears in the architecture, plan, and acceptance criteria.
- Make sure the structure, schema, file names, and terminology are consistent across all documents.
- Make sure assumptions and open questions are explicit instead of buried.
- If the repository already contains docs, update the existing files in place instead of creating parallel duplicates unless the user asks for a fresh variant.

## Resources

- `scripts/init_project_doc_pack.py`
  - Scaffold the core doc pack and selected optional docs into the target repository without overwriting existing files by default.
- `references/deliverables.md`
  - Core and optional document matrix with decision rules for when to create each file.
- `references/structure-and-schema-guide.md`
  - Heuristics for choosing project structure, module boundaries, and a first-pass schema from an incomplete or early-stage spec.
- `assets/templates/`
  - Reusable templates for `README.md`, `AGENTS.md`, and the `docs/` files.

## Guardrails

- Do not treat marketing language as a technical requirement until the spec supports it.
- Do not invent third-party services, infra, or dependencies when the brief does not require them.
- Do not create multiple docs that repeat the same content with different wording.
- Do not leave placeholders or TODO markers in the final project docs unless the user explicitly wants a draft skeleton.
- Do not overwrite existing human-authored docs without checking whether they should be updated in place.
- Do not lock in a structure or schema silently when the choice is high-impact. Record the assumption or ask when necessary.

## Output Rules

- Write created files in English unless the user explicitly asks for another language.
- Keep chat replies in the user's language.
- Keep `README.md` human-oriented and `AGENTS.md` agent-oriented.
- Keep each `docs/` file focused on one job and link related docs instead of duplicating them.
- If material unknowns remain, create `docs/open-questions.md` and record the current default assumption for each unresolved point.

## Suggested Prompts

- `Use $project-kickoff-docs to turn this project brief into a README, AGENTS.md, and a docs/ pack I can hand to another AI agent.`
- `Use $project-kickoff-docs to read the spec in docs/input.md and create the project structure, schema notes, and implementation-ready documentation.`
- `Use $project-kickoff-docs to bootstrap docs for a new full-stack app and include API, UI, and integration docs only where they are actually needed.`
