# agent-skills-lab

This repository is a workspace for building reusable `AGENTS.md`, skills, prompts, and agent files for GitHub Copilot, OpenAI Codex, Claude Code, Gemini CLI, and similar AI coding tools.

## What This Repository Contains

- `AGENTS.md`
  - Repository-level operating rules for AI agents working in this project.
- `.agents/`
  - Shared assets that can be reused across multiple AI tools.
- `.github/`
  - GitHub Copilot-specific assets such as instructions, prompts, agents, and skills.
- `.claude/`
  - Claude Code-specific assets such as agents and commands.
- `.gemini/`
  - Gemini CLI-specific assets such as commands and skills.
- `docs/`
  - Human-facing operational documentation such as mapping tables, checklists, and policies.
- `agent-samples/`
  - Sample deliverables, including topic-specific `AGENTS.md` files.

## Authoring Defaults

- Create files in English unless the user explicitly asks for another language.
- Reply to users in the language they are using in chat.
- Put shared logic in `.agents/` first, then add AI-specific variants only when needed.
- Verify current AI-specific folder conventions against official documentation when the result depends on up-to-date behavior.

## Typical Workflows

### Create a shared skill

1. Start in `.agents/skills/`.
2. Add supporting references or templates under `.agents/references/` or `.agents/templates/` if needed.
3. Only create AI-specific wrappers when a tool needs a different format.

### Create an AI-specific asset

1. Choose the tool-specific folder such as `.github/`, `.claude/`, or `.gemini/`.
2. Follow the conventions documented in that folder's `GUIDE.md`.
3. Reuse shared templates from `.agents/templates/` instead of rewriting from scratch.

### Create a sample AGENTS.md

1. Create a topic folder under `agent-samples/`.
2. Add `AGENTS.md` inside that topic folder.
3. If helpful, use `agent-samples/_template/` as a starting point.

## Current Starting Point

- Existing GitHub Copilot agent files live in `.github/agents/`.
- Existing GitHub Copilot skill examples live in `.github/skills/multi-agent-consensus/` and `.github/skills/multi-agent-review-fix/`.
- Shared templates live in `.agents/templates/`.
- Operational maintenance docs live in `docs/`.

## Suggested Next Steps

- Add new shared skills under `.agents/skills/`.
- Add tool-specific wrappers only when format differences require them.
- Expand `agent-samples/` with concrete topic directories as requests arrive.
- Use `CONTRIBUTING.md` and `docs/checklists.md` when adding new patterns.
