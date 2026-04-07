# GitHub Copilot Assets

This directory stores GitHub Copilot-specific assets.

## Expected Contents

- `agents/`
  - Copilot agent files using `.agent.md`.
- `skills/`
  - Copilot skills organized as one directory per skill.
- `instructions/`
  - Additional instruction files when the Copilot workflow supports them.
- `prompts/`
  - Reusable prompts or prompt snippets.
- `copilot-instructions.md`
  - Optional repository-wide Copilot instructions file.

## Notes

- Existing examples already live in `agents/` and `skills/`.
- Keep reusable pinned subagents in `agents/` with workflow-neutral names when multiple Copilot skills should share them.
- Reuse `.agents/templates/` before creating new file formats from scratch.
