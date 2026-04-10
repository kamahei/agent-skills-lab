---
name: project-kickoff-docs
description: Create an implementation-ready project documentation pack from a brief or specification. Use when Claude Code should generate README.md, AGENTS.md, and docs/ files for a new or lightly scaffolded project, including structure, schema, implementation plan, and AI handoff docs.
---

# Project Kickoff Docs

## Activation

- Use this wrapper when Claude Code should create the initial project documentation pack from a brief, PRD, issue, or specification.
- Treat `$ARGUMENTS` as the current project brief, scope hint, or file location that contains the source material.
- Keep this wrapper thin. Use the shared skill as the source of truth for workflow details.

## Workflow

1. Read `../../../.agents/skills/project-kickoff-docs/SKILL.md`.
2. Read `../../../.agents/skills/project-kickoff-docs/references/deliverables.md` when deciding which docs to create.
3. Read `../../../.agents/skills/project-kickoff-docs/references/structure-and-schema-guide.md` when deciding the initial architecture or schema.
4. If the repository needs a fresh scaffold, use `../../../.agents/skills/project-kickoff-docs/scripts/init_project_doc_pack.py`.
5. Create or update the shared project docs in the current repository. Prefer updating existing files in place over creating duplicate variants.

## Usage Examples

- `/project-kickoff-docs Build docs for a new SaaS invoicing app from the spec in docs/input.md`
- `/project-kickoff-docs Read this project overview and create README.md, AGENTS.md, and implementation-ready docs for the repo`
- `/project-kickoff-docs Bootstrap a new internal tool project and include only the docs needed for another AI agent to implement it safely`

## Output Rules

- Keep generated project files in English unless the user explicitly asks for another language.
- Keep chat replies in the user's language.
- Keep `README.md` human-facing and `AGENTS.md` plus `docs/ai-implementation-guide.md` agent-facing.
