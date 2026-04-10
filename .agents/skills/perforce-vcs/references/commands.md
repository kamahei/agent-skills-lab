# Perforce Command Reference

Use this file when you need command selection help beyond the core workflow in `SKILL.md`.

The commands below cover the standard day-to-day `p4` surface for inspecting state, opening files, organizing changelists, reviewing history, shelving work, resolving merges, and submitting changes. If a nearby standard `p4` command is needed and the exact syntax is uncertain, verify it with local `p4` documentation or official Perforce documentation instead of guessing flags.

## Preflight And Workspace Mapping

| Command | Use |
| --- | --- |
| `p4 info` | Confirm server, user, client, and current workspace context. |
| `p4 set` | Inspect Perforce-related environment variables on Windows. |
| `p4 client -o` | Inspect the current client spec. |
| `p4 where <path>` | Map a local path to depot and client paths. |
| `p4 login -s` | Check whether the session is authenticated. |

## Inspection And History

| Command | Use |
| --- | --- |
| `p4 opened [file ...]` | Show files currently open in pending changelists. |
| `p4 opened -c <change>` | Show files in a specific pending changelist. |
| `p4 changes [-s pending|-s submitted]` | List changelists. |
| `p4 describe -s <change>` | Show summary details for a changelist without file diffs. |
| `p4 files <filespec>` | Show depot files matching a filespec. |
| `p4 fstat <filespec>` | Show detailed file metadata. |
| `p4 filelog <filespec>` | Show revision and integration history. |
| `p4 diff [file ...]` | Compare workspace files to the depot versions. |
| `p4 diff2 <left> <right>` | Compare two depot file revisions or filespecs. |
| `p4 have [filespec]` | Show revisions synced in the current workspace. |
| `p4 sync -n [filespec]` | Preview sync results without changing the workspace. |
| `p4 reconcile -n [file ...]` | Preview add, edit, or delete opens for offline changes. |

## Opening And Updating Files

| Command | Use |
| --- | --- |
| `p4 edit [-c <change>] <file ...>` | Open tracked files for modification. |
| `p4 add [-c <change>] <file ...>` | Open new files for add. |
| `p4 delete [-c <change>] <file ...>` | Open files for delete. |
| `p4 move [-c <change>] <from> <to>` | Rename or move a file while preserving history. |
| `p4 reopen -c <change> <file ...>` | Move open files between changelists. |
| `p4 reconcile [-c <change>] [file ...]` | Open offline or externally modified files for add, edit, or delete. |
| `p4 revert <file ...>` | Discard open file actions and local edits. Use only with explicit approval when user work could be lost. |
| `p4 lock <file ...>` | Lock files before submit-sensitive work. |
| `p4 unlock <file ...>` | Release locks. |

## Changelists

| Command | Use |
| --- | --- |
| `p4 change` | Create a numbered changelist and move files from the default changelist into it. |
| `p4 change <change>` | Edit or view an existing changelist spec. |
| `p4 change -o [<change>]` | Output a changelist spec for noninteractive editing. |
| `p4 change -i` | Create or update a changelist from standard input. |
| `p4 change -d <change>` | Delete an empty pending changelist. |
| `p4 changes -s pending -c <client>` | List pending changelists for a client workspace. |

Use noninteractive changelist editing when automation is safer than launching an editor. A common pattern is:

1. Run `p4 change -o` or `p4 change -o <change>`.
2. Modify the `Description:` block and, if needed, the `Files:` block using a shell-appropriate method.
3. Feed the updated spec back with `p4 change -i`.

## Sync, Integrate, Merge, And Resolve

| Command | Use |
| --- | --- |
| `p4 sync [filespec]` | Sync workspace files from the depot. |
| `p4 integrate ...` | Open files for integration from one branch or stream to another. |
| `p4 copy ...` | Propagate content without scheduling merges. |
| `p4 merge ...` | Schedule merges in workflows that use the merge command. |
| `p4 resolve ...` | Resolve pending integrations or content conflicts. |
| `p4 resolve -n ...` | Preview resolve requirements without modifying files. |

Prefer preview or inspection before claiming a merge path is ready. If a resolve is still pending, report that explicitly.

## Shelving And Unshelving

| Command | Use |
| --- | --- |
| `p4 shelve -c <change>` | Store the current open files of a changelist on the server without submitting. |
| `p4 unshelve -s <change> -c <target>` | Restore shelved files into a pending changelist. |
| `p4 reshelve -s <source> -c <target>` | Copy shelved files into another shelf when needed. |

Use shelves for review, backup, handoff, or checkpointing when the user has not asked for submit.

## Submit

| Command | Use |
| --- | --- |
| `p4 submit` | Submit the default changelist. Avoid this unless the user explicitly asked for submit. |
| `p4 submit -c <change>` | Submit a numbered changelist. |
| `p4 submit -d "<description>"` | Submit with an explicit description when appropriate for the command form in use. |

`p4 submit` is atomic for the changelist it submits. Treat submit as an explicit user-controlled step, not a default completion step.

## Description Guidance

Keep the first line concise and specific. Default to English unless the user requests another language.

English example:

```text
Fix null handling in settings loader

Update fallback logic for missing environment values.
Validate behavior with the existing configuration tests.
```

Requested-language example:

```text
<Use the user-requested language here>

<Add one or two short scope or validation lines only when useful.>
```
