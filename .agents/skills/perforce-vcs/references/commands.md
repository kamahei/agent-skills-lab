# Perforce Command Reference

Use this file when you need command selection help beyond the core workflow in `SKILL.md`. Syntax and options below match the Helix Core P4 Command Reference (2025.x). If a flag or command is uncertain, verify with `p4 help <command>` or the official Perforce documentation instead of guessing.

## Preflight And Workspace Mapping

| Command | Use |
| --- | --- |
| `p4 info` | Confirm server, user, client, and current workspace context. |
| `p4 set` | Inspect Perforce-related environment variables (Windows/macOS/Linux). |
| `p4 client -o` | Output the current client spec for inspection. |
| `p4 clients [-u <user>]` | List known client workspaces. |
| `p4 where [<path>]` | Map a local, client, or depot path to the other two views. |
| `p4 depots` | List all depots on the server. |
| `p4 streams` | List streams the current client can see. |
| `p4 login -s` | Check whether the session ticket is valid. |
| `p4 login` | Obtain a new session ticket. |
| `p4 logout` | Invalidate the current ticket. |
| `p4 tickets` | List cached tickets on this host. |
| `p4 passwd` | Change the current user's password. |

## Inspection And History

| Command | Use |
| --- | --- |
| `p4 opened [file ...]` | Show files currently open in pending changelists for the current client. |
| `p4 opened -c <change>` | Show files in a specific pending changelist. |
| `p4 opened -a` | Show files open across all clients (requires permission). |
| `p4 changes [-s pending|-s submitted|-s shelved]` | List changelists filtered by state. |
| `p4 changes -l` / `-L` | Include full / truncated descriptions in the listing. |
| `p4 changes -u <user> -c <client>` | Filter changelists by user and/or client. |
| `p4 changes <filespec>[@rev,@rev]` | List changelists that touched a filespec or revision range. |
| `p4 describe -s <change>` | Show the spec and affected-file list without diffs. |
| `p4 describe <change>` | Show spec, file list, and diffs (submitted changelists only). |
| `p4 describe -S <change>` | Show spec and diffs of **shelved** files in a pending changelist. |
| `p4 files <filespec>` | List depot files and their head revisions. |
| `p4 fstat <filespec>` | Print file metadata in a tagged, script-friendly format. |
| `p4 filelog [-l] <filespec>` | Show revision and integration history. `-l` includes descriptions. |
| `p4 print -q <file>[@rev]` | Print the depot contents of a file revision (no header). |
| `p4 annotate [-u] [-c] <file>` | Show each line's originating revision (`-u` adds user/date, `-c` shows changelist). |
| `p4 grep -e <pattern> <filespec>` | Search depot file contents for a pattern. |
| `p4 dirs <filespec>` | List depot subdirectories. |
| `p4 have [<filespec>]` | Show revisions currently synced in the workspace. |
| `p4 sync -n [<filespec>]` | Preview sync results without changing the workspace. |
| `p4 cstat <filespec>` | Report per-changelist sync status (have / need / partial). |
| `p4 reconcile -n [<file ...>]` | Preview add/edit/delete opens for offline changes. |
| `p4 interchanges <source> <target>` | List changelists pending integration between two branches or streams. |

## Changelist Diffs

Perforce splits "diff of a changelist" across three distinct commands depending on the changelist state. Pick the command that matches the state; there is no single universal flag.

| Goal | Command |
| --- | --- |
| Diff of a **submitted** changelist | `p4 describe <change>` |
| Unified-format diff of a submitted changelist | `p4 describe -du <change>` |
| Summary-only of a submitted changelist (no diff body) | `p4 describe -s <change>` or `p4 describe -ds <change>` |
| Diff of **shelved** files in a pending changelist | `p4 describe -S -du <change>` |
| Diff of **open (not shelved)** files in a pending changelist | `p4 diff` (workspace vs depot head) on the files in that change |
| Diff a specific file revision against its predecessor | `p4 diff2 -u <file>#<rev-1> <file>#<rev>` |
| Diff between two submitted changelists (path-scoped) | `p4 diff2 -u <filespec>@<change1> <filespec>@<change2>` |

Gotchas:

- `p4 describe` on a **pending** changelist prints the spec and opened-file list but **does not** print diffs. Use `-S` for shelved content, or fall back to `p4 diff` on the open files.
- `p4 diff` has no `-c <change>` filter. To scope it to a pending changelist, get the file list with `p4 opened -c <change>` and feed those paths to `p4 diff`.
- `-du[num]` controls the underlying diff routine. `num` sets context lines (e.g. `-du5`).
- Other `-d` variants: `-dc[num]` context format, `-ds` summary, `-dn` RCS, `-db` ignore whitespace changes, `-dw` ignore all whitespace, `-dl` ignore line-endings.
- `p4 describe -a <change>` includes the content of **added** files (they have no predecessor to diff against).
- `p4 describe -m <max> <change>` limits output to the first `max` files when a changelist is large.

`p4 diff` display filters (no diff body, just file status):

| Option | Shows |
| --- | --- |
| `-sa` | Opened files that differ from the depot. |
| `-sb` | Files opened for integrate that changed after resolve. |
| `-sd` | Unopened files that are missing from the workspace. |
| `-se` | Unopened files that differ from the depot. |
| `-sl` | Every file with `same` / `diff` / `missing` status. |
| `-sr` | Opened files identical to the depot revision. |

## Opening And Updating Files

| Command | Use |
| --- | --- |
| `p4 edit [-c <change>] <file ...>` | Open tracked files for modification. |
| `p4 add [-c <change>] <file ...>` | Open new files for add. |
| `p4 delete [-c <change>] <file ...>` | Open files for delete. |
| `p4 move [-c <change>] <from> <to>` | Rename or move a file while preserving history. |
| `p4 reopen -c <change> <file ...>` | Move open files between changelists. |
| `p4 reconcile [-c <change>] [file ...]` | Open offline/externally modified files for add, edit, or delete. |
| `p4 revert <file ...>` | Discard open file actions and local edits. Use only with explicit approval. |
| `p4 revert -k <file ...>` | Clear the open state on the server without touching the workspace copy. |
| `p4 lock <file ...>` | Lock files on the server before submit-sensitive work. |
| `p4 unlock <file ...>` | Release locks. |

## Changelists

| Command | Use |
| --- | --- |
| `p4 change` | Create a numbered changelist and move default-changelist files into it (interactive). |
| `p4 change <change>` | Edit or view an existing changelist spec (interactive). |
| `p4 change -o [<change>]` | Output a changelist spec for noninteractive editing. |
| `p4 change -i` | Create or update a changelist from standard input. |
| `p4 change -d <change>` | Delete an empty pending changelist. |
| `p4 change -f -d <change>` | Force-delete (admin, e.g. stray pending changes with no files). |
| `p4 changes -s pending -c <client>` | List pending changelists for a specific client workspace. |

Noninteractive changelist editing pattern:

1. `p4 change -o` (or `p4 change -o <change>`) to capture the spec.
2. Modify `Description:` (and optionally `Files:`) using a shell-appropriate method.
3. Pipe the edited spec back with `p4 change -i`.

## Sync, Integrate, Merge, And Resolve

| Command | Use |
| --- | --- |
| `p4 sync [<filespec>]` | Sync workspace files from the depot. |
| `p4 sync -f <filespec>` | Force-resync ignoring have list. Destructive; confirm before using. |
| `p4 sync -k <filespec>` | Update the have list without touching workspace files. |
| `p4 integrate <src> <tgt>` | Open files for integration from one branch or stream to another. |
| `p4 copy <src> <tgt>` | Propagate content to the target without scheduling merges. |
| `p4 merge <src> <tgt>` | Schedule merges where the merge command is preferred. |
| `p4 populate <src> <tgt>` | One-shot branch population without opening files in a changelist. |
| `p4 resolve` | Resolve pending integrations or content conflicts (interactive). |
| `p4 resolve -n` | Preview resolve requirements without modifying files. |
| `p4 resolve -am` | Accept automerge where safe, leave conflicts for manual resolve. |
| `p4 resolve -at` / `-ay` | Accept theirs / yours (destructive; use deliberately). |
| `p4 interchanges <src> <tgt>` | Show changelists that are not yet integrated from src to tgt. |

Prefer preview (`-n`) or inspection before claiming a merge path is ready. If any resolve is still pending, report it explicitly instead of submitting.

## Branches, Streams, And Labels

| Command | Use |
| --- | --- |
| `p4 branch <name>` | Create or edit a branch mapping spec. |
| `p4 branches` | List existing branch specs. |
| `p4 stream <stream>` | Create, edit, or delete a stream spec. |
| `p4 streams` | List streams visible to the client. |
| `p4 switch <stream>` | Switch the current client to a different stream (streams workspaces). |
| `p4 label <name>` | Create or edit a label spec. |
| `p4 labels [<filespec>]` | List labels, optionally scoped to a filespec. |
| `p4 labelsync -l <label> [<filespec>]` | Point a label at current workspace revisions. |
| `p4 tag -l <label> <filespec>` | Tag specific file revisions with a label. |

## Shelving And Unshelving

| Command | Use |
| --- | --- |
| `p4 shelve -c <change>` | Store the open files of a changelist on the server without submitting. |
| `p4 shelve -r -c <change>` | Replace the server shelf with the current workspace state. |
| `p4 shelve -d -c <change> [<file ...>]` | Delete the shelf (all files or listed files). |
| `p4 shelve -f -c <change>` | Force-overwrite an existing shelf. |
| `p4 unshelve -s <change> -c <target>` | Restore shelved files into a pending changelist. |
| `p4 unshelve -s <change> -f` | Force unshelve even when local files are writable. |
| `p4 reshelve -s <source> -c <target>` | Copy shelved files into another shelf. |

Use shelves for review, backup, handoff, or checkpointing when the user has not asked for submit.

## Submit

| Command | Use |
| --- | --- |
| `p4 submit` | Submit the default changelist. Avoid unless the user explicitly asked for submit. |
| `p4 submit -c <change>` | Submit a numbered changelist. |
| `p4 submit -d "<description>"` | Submit with an explicit description (default changelist form). |
| `p4 submit -e <change>` | Submit a changelist whose spec has already been edited and saved. |
| `p4 submit -s` | Include jobs interactively during submit. |

`p4 submit` is atomic for the changelist it submits. Treat submit as an explicit user-controlled step, not a default completion step.

## Jobs And Fixes

| Command | Use |
| --- | --- |
| `p4 jobs [<filter>]` | List jobs known to the server. |
| `p4 job [<jobname>]` | Create or edit a job spec. |
| `p4 fix -c <change> <job>` | Link a job to a changelist. |
| `p4 fixes -c <change>` / `-j <job>` | List fix relationships. |

## Users, Clients, And Admin Inspection

| Command | Use |
| --- | --- |
| `p4 user -o [<user>]` | Output a user spec. |
| `p4 users` | List known users. |
| `p4 group -o <group>` | Output a group spec (admin). |
| `p4 groups` | List groups. |
| `p4 protects [-u <user>] [-h <host>] [<filespec>]` | Show effective protections for a user or file. |
| `p4 monitor show` | Show running server processes (admin, useful for debugging slowness). |
| `p4 counters` | List server counters. |

## Scripting And Global Options

Global options come **before** the subcommand (`p4 [g-opts] <subcmd>`).

| Option | Use |
| --- | --- |
| `-c <client>` | Override `P4CLIENT` for this invocation. |
| `-u <user>` | Override `P4USER`. |
| `-p <port>` | Override `P4PORT`. |
| `-P <password-or-ticket>` | Supply ticket/password inline (prefer tickets). |
| `-d <dir>` | Run as if invoked from `<dir>`. |
| `-s` | Prefix each output line with `info:`, `error:`, etc. for parsing. |
| `-ztag` | Emit tagged output (key-value pairs) for reliable parsing. |
| `-Mj` | Emit JSON-per-line output (supported on many commands). |
| `-G` | Emit Python-marshaled output (legacy scripting). |
| `-x <file>` | Read arguments from a file, one per line. Combine with per-file commands for batch operations. |

Prefer `-ztag` or `-Mj` for automation. Plain output is not a stable contract across versions.

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
