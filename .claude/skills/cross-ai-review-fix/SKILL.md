---
name: cross-ai-review-fix
description: Delegate a bounded review or isolated review-backed fix from Claude Code to Codex or GitHub Copilot CLI. Use only when the user explicitly wants Claude Code to obtain an external AI review or patch instead of relying on Claude alone, including the GitHub Copilot GPT-5.4 bridge case.
---

# Cross AI Review Fix

## Activation

- Use this wrapper when Claude Code should delegate review or review-backed fixes to Codex or GitHub Copilot.
- Treat `$ARGUMENTS` as the requested route, scope, and stop condition.
- Default to review only unless the user explicitly asks for fix application.
- Use this wrapper for the old Copilot bridge cases too. Do not keep a separate Claude skill for the GitHub Copilot GPT-5.4 route.

## Workflow

1. Read `../../../.agents/skills/cross-ai-review-fix/SKILL.md`.
2. If the user asks for Codex review, run `codex review ...`.
3. If the user asks for Codex fix, create a disposable worktree with `git worktree add --detach <path> HEAD` and then run `codex exec -C <path> ...`.
4. If the user asks for GitHub Copilot GPT-5.4 review, run `copilot --agent=pinned-gpt-5-4 ...` in the active repository.
5. If the user asks for GitHub Copilot GPT-5.4 fix, create a disposable worktree with `git worktree add --detach <path> HEAD`, move into that worktree, and run `copilot --agent=pinned-gpt-5-4 ...`.
6. Keep the active repository unchanged until you inspect the external report or patch and decide what to apply locally.

## Usage Examples

- Ask Claude to send the staged diff to Codex for review only:
  `/cross-ai-review-fix claude to codex review only the staged diff in src/payments and stop after the report`
- Ask Claude to use Codex for an isolated fix after checking failing tests:
  `/cross-ai-review-fix claude to codex inspect the failing retry tests, and if the bug is confirmed prepare only the minimal safe fix in an isolated worktree`
- Ask Claude to use GitHub Copilot GPT-5.4 as a reviewer:
  `/cross-ai-review-fix claude to github copilot gpt-5.4 review auth/session.ts and the staged diff only, then stop after findings`
- Ask Claude to use GitHub Copilot GPT-5.4 for an isolated fix:
  `/cross-ai-review-fix claude to github copilot gpt-5.4 review the current diff for the invoice rounding bug, and if needed apply only the smallest safe fix in an isolated worktree`

## Output Rules

- State which route ran: `Claude -> Codex` or `Claude -> GitHub Copilot GPT-5.4`.
- State whether the run stopped at review or continued to an isolated fix.
- State what validation ran locally after the delegated step.
