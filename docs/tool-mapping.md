# Tool Mapping

This document maps each supported AI tool to the file types and directories typically used in this repository.

These conventions can evolve. If a task depends on current tool behavior, verify the latest official documentation before relying on the mapping.

## Shared Source Layer

Use `.agents/` first when content can be reused across tools.

| Purpose | Preferred Location |
| --- | --- |
| Shared reusable skills | `.agents/skills/` |
| Shared reusable agent outlines | `.agents/agents/` |
| Shared templates | `.agents/templates/` |
| Shared supporting notes or references | `.agents/references/` |

## Tool-Specific Mapping

| Tool | Repository Instruction File | Tool-Specific Directories | Typical File Types |
| --- | --- | --- | --- |
| OpenAI Codex or vendor-neutral agents | `AGENTS.md` | `.agents/` | `AGENTS.md`, shared templates, shared skills |
| GitHub Copilot | `.github/copilot-instructions.md` when needed | `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/prompts/` | `.agent.md`, `SKILL.md`, prompt files, instruction files |
| Claude Code | `CLAUDE.md` when needed | `.claude/agents/`, `.claude/commands/` | `CLAUDE.md`, agent files, command files |
| Gemini CLI | `GEMINI.md` when needed | `.gemini/skills/`, `.gemini/commands/` | `GEMINI.md`, skill files, command files |

## Sample Output Mapping

| Output Type | Preferred Location |
| --- | --- |
| General sample `AGENTS.md` | `agent-samples/<Topic>/AGENTS.md` |
| Sample-specific supporting files | `agent-samples/<Topic>/...` |
| Reusable templates behind samples | `.agents/templates/` |

## Placement Decision Guide

1. If the file is meant to be copied into another repository as an example, place it under `agent-samples/`.
2. If the content should be shared across multiple tools, place it under `.agents/`.
3. If a specific tool requires its own format, place only the tool-specific wrapper in that tool's directory.
4. If repository-wide behavior for one tool is needed, use that tool's top-level instruction file such as `CLAUDE.md` or `GEMINI.md`.

## Current Official References

- GitHub Copilot agent skills and instructions: `docs.github.com`
- Claude Code memory and sub-agents: `docs.anthropic.com`
- Gemini CLI `GEMINI.md` and skills: `geminicli.com`
