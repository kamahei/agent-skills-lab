---
name: bugfix
description: Inspect project code systematically, find real bugs and safe fixes, preserve existing behavior, and self-review every change.
---

# Bugfix

## Activation

- Use this skill when the user asks to inspect a repository, directory, or file for bugs and fix them safely.
- Also use it for targeted correctness, security, typo, or reliability cleanups.
- Do not use it for feature work or broad refactoring. If the safest fix would require architecture or design changes beyond a minimal correction, stop and ask first.

## Inputs

- Expected context: a repository or a specific scope to inspect, plus any failing tests, diagnostics, logs, or known problem areas if available.
- Optional inputs: languages or frameworks in use, modules that must not change, and any priorities such as security, stability, or user-facing correctness.

## Workflow

1. Clarify the requested scope and inspect it systematically. Start with existing diagnostics, failing tests, error messages, and high-risk areas such as input handling, authentication, authorization, data parsing, persistence, concurrency, resource cleanup, and boundary conditions.
2. If the repository is too large for a single truly exhaustive pass, say what scope you covered and continue in prioritized slices rather than pretending the whole codebase was fully audited.
3. Read enough local context before editing. Verify each suspected issue against surrounding code, existing helpers, tests, and repository conventions. Distinguish real bugs from intentional patterns or style differences.
4. Look for issues with concrete impact. Include logic errors, broken conditions, off-by-one and null or empty edge cases, unsafe defaults, missing validation, incorrect error handling, typo or naming mistakes that hurt correctness or clarity, and design flaws that create real bugs or reliability risk.
5. Prefer the smallest change that fixes the confirmed issue. Preserve existing behavior everywhere else, and reuse existing helpers, abstractions, and patterns before introducing new ones.
6. Follow the repository's current coding style first. If the surrounding code is inconsistent or unclear, follow the language or framework standard style instead.
7. Ask before making large or wide-ranging changes. This includes architecture changes, public API or contract changes, schema changes, dependency changes, broad renames, large refactors, or any fix that materially changes behavior outside the bug itself.
8. If a safe fix cannot be verified locally, explain the issue, the risk, and the smallest candidate fix rather than applying a speculative change.
9. Validate with existing tests, builds, linters, or diagnostics when they already exist and are relevant. Do not add new tooling just to support the fix unless the user asks for it.
10. Perform a self code review after every change. Re-read the diff in context, check for unintended edits, broken imports, type or signature mismatches, missed edge cases, and style drift. Confirm the change is minimal and that unrelated code was not altered.

## Guardrails

- Do not make changes just to match personal style.
- Do not bundle unrelated cleanup into the same change unless the user asked for a broad sweep.
- Do not silently weaken security, validation, or error reporting to make a test pass.
- Do not use broad catch blocks, silent fallbacks, or dead code as shortcuts unless the existing code clearly relies on that pattern and the change remains safe.
- When fixing typos, keep the change surgical. Ask before wide renames across public APIs, serialized fields, database columns, or compatibility-sensitive user-facing surfaces.
- Treat obvious security issues as in scope, but do not claim a formal security audit if you only performed a code review pass.

## Output Rules

- Summarize what scope you inspected.
- For each fix, state what was wrong, why it was a bug or risk, and what minimal change was made.
- List any important findings you intentionally did not change and why.
- Report what validation you ran and any limits on verification.
- State the result of the self review, including any residual risk or follow-up suggestion.
- Keep chat replies in the user's language and preserve the repository's language and style conventions in code, comments, and docs.

## Suggested Prompts

- `Inspect this repository for bugs and fix the safe ones. Ask before any large changes.`
- `Review src/ for correctness and security issues, then apply the minimal safe fixes.`
- `Find and fix bugs in these files while preserving existing behavior and self-reviewing your changes.`
