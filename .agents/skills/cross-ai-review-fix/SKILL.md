---
name: cross-ai-review-fix
description: Run a cross-AI implementation, review, and isolated-fix workflow across Codex, Claude Code, and GitHub Copilot CLI. Use when one AI should implement or inspect a change and another AI should review the resulting diff or prepare a bounded fix, including Codex to GitHub Copilot Claude Sonnet 4.6, Claude Code to GitHub Copilot GPT-5.4, GitHub Copilot to Codex, GitHub Copilot to Claude, Codex to Claude, and Claude to Codex. Also use this skill for requests that previously matched a dedicated Copilot bridge review-fix flow.
---

# Cross AI Review Fix

## Activation

- Use this skill when the current AI should delegate review or review-backed fixes to a different AI runtime through its CLI.
- Prefer this skill for bounded scopes such as staged diffs, named files, failing tests, or a small known patch.
- Treat the normal sequence as `implement or inspect -> external review -> isolated external fix if needed -> local validation`.
- Use this skill for all GitHub Copilot bridge cases too. Do not keep a separate Copilot-only skill when the route still fits this workflow.
- Do not use this skill for broad audits, large refactors, or unbounded external editing.

## Inputs

- Expected context: a Git repository, the relevant CLIs installed and authenticated, and a clear review scope.
- Optional inputs: parent AI, target external AI, review base, target files, failing commands, diagnostics, explicit model names, and whether the delegated step should stop at review or continue to an isolated fix.

## Route Matrix

- `Codex -> GitHub Copilot Claude Sonnet 4.6`
  - Review: `copilot --agent=pinned-claude-sonnet-4-6 ...`
  - Fix: `git worktree add ...` then `copilot --agent=pinned-claude-sonnet-4-6 ...`
- `Claude -> GitHub Copilot GPT-5.4`
  - Review: `copilot --agent=pinned-gpt-5-4 ...`
  - Fix: `git worktree add ...` then `copilot --agent=pinned-gpt-5-4 ...`
- `GitHub Copilot -> Codex`
  - Review: `codex review ...`
  - Fix: `codex exec ...`
- `GitHub Copilot -> Claude`
  - Review: `claude -p ...`
  - Fix: `git worktree add ...` then `claude -p ...`
- `Codex -> Claude`
  - Review: `claude -p ...`
  - Fix: `git worktree add ...` then `claude -p ...`
- `Claude -> Codex`
  - Review: `codex review ...`
  - Fix: `codex exec ...`

## Native Commands

- Use a path syntax that is valid in the current shell and OS. Prefer a simple relative path such as `../cross-ai-fix` when possible.

- Shared isolated-fix pattern:

```text
git worktree add --detach <worktree-path> HEAD
```

- Codex review:

```text
codex review --uncommitted "<prompt>"
```

- Codex isolated fix:

```text
codex exec -C <worktree-path> -s danger-full-access -a never "This workspace is isolated and disposable. <prompt>"
```

- Claude review:

```text
claude -p "<prompt>" --permission-mode dontAsk
```

- Claude isolated fix. Run this command from inside `<worktree-path>`:

```text
claude -p "This workspace is isolated and disposable. <prompt>" --permission-mode bypassPermissions
```

- Copilot review:

```text
copilot --agent=<pinned-agent> --prompt "<prompt>" --allow-all-tools --silent
```

- Copilot isolated fix. Run this command from inside `<worktree-path>`:

```text
copilot --agent=<pinned-agent> --prompt "This workspace is isolated and disposable. <prompt>" --allow-all-tools --silent
```

- Inspect and remove the isolated worktree:

```text
git -C <worktree-path> diff --stat
git -C <worktree-path> diff
git worktree remove --force <worktree-path>
```

## Workflow

1. Confirm the parent AI, the external target AI, and whether the delegated step is `review-only` or `review-then-fix`.
2. Narrow the scope before delegating. Prefer changed files, staged diffs, failing tests, or a patch file over a whole-repository request.
3. Run the external reviewer first and capture its report.
4. If the review supports a small fix, create an isolated worktree and run the external fixer there instead of in the active repository.
5. Inspect the resulting report or patch in the parent AI. Apply only the smallest safe subset that matches the user's request.
6. Validate locally and report any residual disagreement or risk.

## Usage Examples And Suggested Prompts

- Codex implemented a fix and now wants Claude to review only the staged diff:
  `/cross-ai-review-fix codex to claude review only the staged diff in src/auth and stop after the report`
- Codex implemented a fix and wants GitHub Copilot Claude Sonnet 4.6 to review it, then prepare an isolated patch only if it finds a real bug:
  `/cross-ai-review-fix codex to github copilot claude sonnet 4.6 review the current diff, and only if there is a confirmed bug create an isolated fix worktree and patch it there`
- Claude implemented a fix and wants GitHub Copilot GPT-5.4 to review only `server/api.ts` and the staged diff:
  `/cross-ai-review-fix claude to github copilot gpt-5.4 review server/api.ts and the staged diff only, then stop after findings`
- Claude wants Codex to inspect failing tests and prepare an isolated fix:
  `/cross-ai-review-fix claude to codex review the failing tests for billing retries, and if the bug is confirmed prepare only the minimal safe fix in an isolated worktree`
- GitHub Copilot wants Codex to review all uncommitted changes before merge:
  `/cross-ai-review-fix github copilot to codex review the current uncommitted diff for regressions and missing tests, then stop after the review report`
- GitHub Copilot wants Claude to review a patch file instead of the whole repository:
  `/cross-ai-review-fix github copilot to claude review only patch checkout-timeout.patch and report correctness or compatibility risks`
- Short prompt for Codex to Claude review:
  `/cross-ai-review-fix codex to claude review the staged diff and stop after the report`
- Short prompt for GitHub Copilot to Codex review plus optional isolated fix:
  `/cross-ai-review-fix github copilot to codex review the current uncommitted diff, then prepare an isolated fix only if the review finds a real bug`
- Short prompt for Codex to GitHub Copilot Claude Sonnet 4.6 review:
  `/cross-ai-review-fix codex to github copilot claude sonnet 4.6 review the diff after implementation and apply only safe agreed fixes`
- Short prompt for Claude to GitHub Copilot GPT-5.4 review:
  `/cross-ai-review-fix claude to github copilot gpt-5.4 review the staged diff and stop after findings`

## Guardrails

- Never claim independence when the parent and delegated AI resolve to the same model family or a substituted fallback.
- Never run an external fixer in the active repository by default.
- Never give the external AI broader scope than needed when file paths, diffs, or diagnostics are enough.
- Never treat the external output as final truth. The parent AI must inspect the report or diff before applying changes.
- Prefer review output or patch output over long narrative explanations.
- If a CLI is missing, unauthenticated, or returns an availability error, stop and report that route as unavailable.

## Output Rules

- State the parent AI and the delegated AI route that ran.
- State whether the delegated step stopped at review or continued to an isolated fix.
- State whether an isolated worktree was used and report its path when relevant.
- Separate delegated findings from the final local decisions and applied changes.
- Report validation and any residual risk.
