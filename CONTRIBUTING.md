# Contributing

This repository is a library of reusable AI agent instructions, skills, prompts, and samples. Contributions should favor reuse, clarity, and low-maintenance structure over one-off files.

## General Principles

- Write created files in English unless a request explicitly requires another language.
- Use the requester's language for chat replies and discussion.
- Put shared content in `.agents/` whenever possible.
- Create AI-specific variants only when a tool requires a different file format, location, or behavior.
- Prefer small, clearly scoped additions over broad speculative restructuring.

## Placement Rules

Use this order when deciding where a new file belongs:

1. If it is a sample output, put it in `agent-samples/<Topic>/`.
2. If it is reusable across tools, put it in `.agents/`.
3. If it is specific to GitHub Copilot, put it in `.github/`.
4. If it is specific to Claude Code, put it in `.claude/`.
5. If it is specific to Gemini CLI, put it in `.gemini/`.
6. If it is repository-wide neutral guidance for Codex or general agents, use the root `AGENTS.md`.

## Naming Conventions

- Use short, descriptive directory names.
- Prefer names that map cleanly to the tool or task.
- For sample directories, use a readable topic name such as `UE5`, `Nextjs`, or `Laravel`.
- For shared skills, prefer kebab-case such as `api-review` or `migration-planner`.
- Preserve tool-specific naming conventions when a tool already expects a known format.

## Adding A New Sample

1. Create `agent-samples/<Topic>/`.
2. Add `AGENTS.md` as the main sample file.
3. Reuse `agent-samples/_template/` when it helps.
4. Add supporting files only if they materially improve reuse.
5. If the sample needs environment variables, include `.env.example` and follow `docs/env-example-policy.md`.

## Adding A Shared Template

1. Put the template in `.agents/templates/`.
2. Keep placeholders obvious and easy to replace.
3. Document the template in `.agents/templates/README.md`.
4. Prefer one strong template over several weakly differentiated ones.

## Adding An AI-Specific File

1. Confirm that the file really needs to be tool-specific.
2. Follow the mapping in `docs/tool-mapping.md`.
3. Reuse shared wording from `.agents/` where possible.
4. If current tool behavior matters, verify the latest official documentation before finalizing the file.

## Review Checklist

Before merging or keeping a change, confirm:

- The file is in the correct directory.
- The output is in English unless intentionally localized.
- The content is practical, not only abstract.
- Shared content was not duplicated unnecessarily into multiple tool folders.
- Paths, examples, and file references are internally consistent.
- New templates or samples are reflected in the relevant README when needed.

## Useful Companion Docs

- `AGENTS.md`
- `docs/tool-mapping.md`
- `docs/checklists.md`
- `docs/env-example-policy.md`
- `.agents/templates/README.md`
