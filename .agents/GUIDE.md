# Shared Assets

This directory stores assets that should be reusable across multiple AI tools.

## Subdirectories

- `agents/`
  - Shared agent definitions or outlines that are not tied to one vendor format.
- `skills/`
  - Shared skill implementations or portable skill source material.
- `templates/`
  - Reusable starter files for common outputs such as `AGENTS.md`, `CLAUDE.md`, and skill files.
- `references/`
  - Shared notes, checklists, style guides, and supporting material.

## Rules

- Prefer putting reusable content here before creating AI-specific copies.
- Keep vendor-specific syntax out of shared files unless the template is explicitly labeled for a specific tool.
- If a tool needs a special format, create a thin tool-specific adaptation instead of duplicating the full content.
- For skills in this repository, treat `.agents/skills/` as the authoritative source.
- GitHub Copilot should use the shared skill from `.agents/skills/` directly unless a specific exception is documented.
- When Claude Code needs a slash-invokable entrypoint for a shared skill, add a thin wrapper in `.claude/skills/` that points back to the shared source.
