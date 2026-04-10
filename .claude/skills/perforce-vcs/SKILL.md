---
name: perforce-vcs
description: Use Perforce or Helix Core CLI (`p4`) instead of git for source-control work in a Perforce-managed workspace. Use when Claude Code should inspect, sync, open files, manage changelists, shelve, resolve, or prepare submit-ready work through `p4`.
---

# Perforce VCS

## Activation

- Use this wrapper when Claude Code is working in a Perforce or Helix Core workspace and source-control actions should happen through `p4`, not `git`.
- Treat `$ARGUMENTS` as the requested Perforce task, target files, changelist scope, depot path, or submit/shelve instruction.
- Keep this wrapper thin. Use the shared skill as the source of truth for the Perforce workflow, changelist rules, and guardrails.

## Workflow

1. Read `../../../.agents/skills/perforce-vcs/SKILL.md`.
2. Read `../../../.agents/skills/perforce-vcs/references/commands.md` when selecting `p4` commands or flags.
3. Confirm the workspace is usable with Perforce before mutating source-control state.
4. Use `p4` for inspection, file actions, changelist management, shelves, resolves, and submit preparation according to the shared workflow.
5. Do not submit unless the user explicitly asks for submit.

## Usage Examples

- `/perforce-vcs Inspect this workspace with p4 instead of git and prepare a changelist for the current edits`
- `/perforce-vcs Open these files for edit, split unrelated work into separate changelists, and leave everything unsubmitted`
- `/perforce-vcs Reconcile offline changes, write English changelist descriptions, and shelve the results for review`

## Output Rules

- Keep chat replies in the user's language.
- State whether the workspace was usable with `p4`.
- Report changelist numbers, file actions, description language, and whether the result is pending, shelved, or submitted.
