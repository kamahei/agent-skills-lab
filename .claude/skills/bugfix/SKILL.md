---
name: bugfix
description: Inspect project code for real bugs and apply the smallest safe fixes. Use when Claude Code should debug or fix correctness, reliability, security, typo, or design-defect issues while preserving existing behavior and self-reviewing each change.
---

# Bugfix

## Activation

- Use this wrapper when Claude Code should inspect a repository, directory, or file for real bugs and fix them safely.
- Treat `$ARGUMENTS` as the requested scope, diagnostics, failing tests, or known problem description.
- Keep this wrapper thin. Use the shared skill as the source of truth for the bugfix workflow and guardrails.

## Workflow

1. Read `../../../.agents/skills/bugfix/SKILL.md`.
2. Start from the strongest available evidence such as failing tests, errors, logs, or user-reported symptoms before broad scanning.
3. Inspect enough local context to confirm each suspected issue before editing.
4. Apply only the smallest safe fix that matches the shared skill's scope, validation rules, and reporting expectations.
5. Self-review the resulting diff before concluding.

## Usage Examples

- `/bugfix Inspect this repository for bugs and fix the safe ones`
- `/bugfix Review src/auth for correctness and security issues, then apply the minimal safe fixes`
- `/bugfix Investigate the failing retry tests and fix only the confirmed bug without broad refactoring`

## Output Rules

- Keep chat replies in the user's language.
- Preserve the repository's language and style conventions in code, comments, and docs.
- Report inspected scope, applied fixes, validation, and any intentionally unmodified risks.
