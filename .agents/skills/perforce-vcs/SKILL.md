---
name: perforce-vcs
description: Use Perforce or Helix Core CLI (`p4`) instead of git for source control work in a Perforce-managed workspace. Activate when the user mentions Perforce, Helix Core, `p4`, changelists, shelves, depot paths, sync, resolve, integrate, or submit workflows, or when file adds, edits, deletes, moves, and changelist management must be handled through `p4` with explicit descriptions and no automatic submit.
---

# Perforce VCS

## Activation

- Use this skill when the workspace is managed by Perforce or Helix Core and version-control work should happen through `p4`, not `git`.
- Also use it when the user mentions `p4`, changelists, shelves, depot paths, client workspaces, sync, reconcile, resolve, integrate, or submit.
- Use it for routine source-control tasks such as inspecting status, syncing, opening files for `edit`, `add`, `delete`, or `move`, reorganizing changelists, shelving work, unshelving work, resolving merges, and preparing or submitting changelists.
- Do not use `git` as a fallback for equivalent source-control actions unless the user explicitly asks for `git` or the workspace is clearly not a Perforce workspace.

## Inputs

- Expected context: a Perforce client workspace, the `p4` CLI, and a task involving source control or changelist management.
- Optional inputs: requested description language, allowed operations such as `submit` or `shelve`, target files, depot paths, stream or branch context, and any known changelist numbers.
- Default description language: English. If the user specifies another language, use that language for changelist descriptions and any submit description text.

## Workflow

1. Confirm that the workspace is actually usable with Perforce before changing source-control state. Prefer `p4 info`, environment inspection, and workspace inspection to confirm `P4PORT`, `P4CLIENT`, `P4USER`, and the active client mapping. If `p4` is unavailable or server access is misconfigured, stop and report the blocking issue instead of switching to `git`.
2. Inspect existing pending work before opening or moving files. Use commands such as `p4 opened`, `p4 changes -s pending`, `p4 diff`, `p4 reconcile -n`, `p4 files`, `p4 fstat`, `p4 filelog`, and `p4 describe -s` according to the question being answered. For the diff of a specific changelist, pick the command that matches the state: `p4 describe [-du] <change>` for submitted, `p4 describe -S [-du] <change>` for shelved pending, or `p4 diff` over files listed by `p4 opened -c <change>` for open pending. `p4 describe` alone does not emit diffs on pending changelists.
3. Open files with the correct Perforce action before editing or rearranging them. Use `p4 edit` for tracked modifications, `p4 add` for new files, `p4 delete` for removals, `p4 move` for renames or moves, `p4 integrate` or `p4 copy` for propagation work, and `p4 reconcile` after offline or tool-driven changes that bypassed `p4`.
4. Create or reuse numbered changelists deliberately. Do not leave unrelated work mixed into the default changelist when the task contains distinct fixes, features, refactors, or generated updates.
5. Split changelists by coherent intent, not by file extension. Keep one changelist per logical unit such as a bug fix, a refactor, a docs change, or a generated-file refresh. When a task expands, move files into the correct changelist with `p4 reopen -c <change>`.
6. Write clear changelist descriptions before handoff, shelving, or submit. Keep the first line concise and specific. Add short context lines only when they materially help review.
7. Submit only when the user explicitly asks for submit. Preparing a changelist, leaving it pending, or shelving it is safe by default. Running `p4 submit` is not.
8. If the user requests submit, verify the exact changelist, unresolved files, and final description first. Use inspection or preview commands before submit when merges, integrations, or resolves are involved, then use `p4 submit -c <change>` for numbered changelists.
9. Prefer shelves when the user wants review, backup, or checkpointing without committing to the depot. Use `p4 shelve -c <change>` and `p4 unshelve -s <change> -c <target>` as needed.
10. After each Perforce operation, report the changelist numbers involved, the file actions taken, and whether anything remains pending, shelved, unresolved, or unsubmitted.

## Changelist Strategy

- Create a numbered changelist as soon as the task is distinct from other pending work.
- Separate unrelated fixes, features, refactors, generated artifacts, and documentation changes into different changelists whenever that separation improves reviewability or submit safety.
- Inspect existing pending changelists before reorganizing files. Avoid moving files across changelists unless the task makes the intent clear.
- Prefer `p4 reopen -c <change>` to split or regroup files after the fact.
- If files were initially opened in the default changelist, move them out once the logical grouping is known.
- Keep each changelist description aligned to the exact files and purpose in that changelist. Never reuse the same generic description for different work items.

## Description Rules

- Use English by default.
- If the user specifies a language, use that language consistently for changelist descriptions and submit descriptions.
- Keep the first line short, specific, and reviewable.
- Add one or more follow-up lines only when they help explain scope, validation, or risk.
- Avoid placeholders such as `misc changes`, `update files`, or `WIP`.
- If multiple changelists are created, write a different description for each one.

## Command Selection

- Read `references/commands.md` for the core command catalogue and usage patterns, including the "Changelist Diffs" section that lays out which command to use for submitted vs pending vs shelved state.
- Prefer inspection commands before mutating commands.
- Prefer `p4 move` over ad hoc delete-and-add renames when the history should be preserved.
- Prefer noninteractive changelist editing for automation. Generate a form with `p4 change -o`, edit the spec outside the interactive editor, and feed it back with `p4 change -i` using a shell-appropriate workflow.
- Prefer `-ztag` or `-Mj` (JSON-per-line) global options when parsing `p4` output in automation. Plain output is not a stable contract.
- When exact flags are uncertain, consult `p4 help <command>` or official Perforce documentation instead of guessing.

## Guardrails

- Never use `git add`, `git commit`, `git checkout`, or equivalent git flows for Perforce-managed work unless the user explicitly asks for git.
- Never run `p4 submit` unless the user explicitly requests submit.
- Never group unrelated work into one changelist just because the files were touched in the same session.
- Never discard user changes with `p4 revert`, force-sync behavior, or destructive workspace cleanup unless the user explicitly approves it.
- Never auto-resolve conflicts blindly. Inspect and report unresolved files before claiming a changelist is ready.
- Never change or submit another user's changelist unless the user explicitly instructs that action and the permissions are clear.
- Never leave the description language ambiguous. If no language is specified, default to English and say so.
- If server connectivity, protections, or file locks block the requested action, stop and report the exact issue.

## Output Rules

- State whether the workspace was connected and usable with `p4`.
- State which changelist or changelists were inspected, created, or updated.
- State how the work was split across changelists and why.
- State which description language was used. If no language was requested, say English was used by default.
- State clearly whether the result is pending, shelved, or submitted.
- If submit was not explicitly requested, state that no submit was performed.
- Report unresolved merges, shelves, locks, or pending files that still require user action.

## Suggested Prompts

- `Use $perforce-vcs to inspect this workspace with p4 instead of git and prepare a changelist for the current edits.`
- `Use $perforce-vcs to open these files for edit, split unrelated work into separate changelists, and leave everything unsubmitted.`
- `Use $perforce-vcs to reconcile offline file changes, write English changelist descriptions, and shelve the results for review.`
- `Use $perforce-vcs to prepare submit-ready changelists, but do not submit until I say so.`
- `Use $perforce-vcs to submit changelist 12345 with a Japanese description after checking for unresolved files.`

## Resources

- `references/commands.md`: core `p4` command catalogue for inspection, file actions, changelists, shelves, sync, integrate, resolve, and submit workflows.
