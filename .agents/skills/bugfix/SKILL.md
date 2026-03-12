---
name: bugfix
description: Inspect project code systematically, find real bugs and safe fixes, preserve existing behavior, and self-review every change.
---

# Bugfix

## Activation

- Use this skill when the user asks to inspect a repository, directory, or file for bugs and fix them safely.
- Also use it for targeted correctness, security, typo, reliability, or design-defect cleanups.
- Do not use it for feature work, speculative cleanup, or broad refactoring.
- If the safest fix would require architecture or design changes beyond a minimal correction, stop and ask first.

## Inputs

- Expected context: a repository or a specific scope to inspect, plus any failing tests, diagnostics, logs, or known problem areas if available.
- Optional inputs: languages or frameworks in use, modules that must not change, and any priorities such as security, stability, user-facing correctness, or directories to exclude.

## Scope And Limits

- Start with concrete evidence first: failing tests, error messages, linter output, logs, stack traces, or user-reported symptoms. Do not begin with a broad code sweep if concrete diagnostics already exist.
- If the repository is too large for a single exhaustive pass, state what scope you covered and continue in prioritized slices rather than implying the entire codebase was fully audited.
- Treat design issues as in scope when they create a real correctness, security, or reliability problem.
- Do not claim exhaustive coverage, guaranteed correctness, or a formal security audit unless the work genuinely met that bar.

## Priority Order

1. Confirmed correctness bugs and regressions.
2. Security vulnerabilities and unsafe defaults.
3. Reliability issues such as error-handling gaps, data-loss risks, resource leaks, concurrency problems, and edge-case failures.
4. Design defects that directly create real bugs, unclear contracts, or recurring reliability problems.
5. Typos and naming mistakes that hurt correctness, safety, clarity, or maintainability.

## Workflow

1. Clarify the requested scope and gather the strongest available signals first: failing tests, diagnostics, error messages, logs, known bug reports, and recently changed high-risk areas.
2. If no concrete diagnostics exist, inspect the target systematically with priority on input handling, authentication, authorization, parsing, persistence, concurrency, resource cleanup, boundary conditions, and compatibility-sensitive code paths.
3. Read enough local context before editing. Verify each suspected issue against surrounding code, existing helpers, tests, repository conventions, and intended behavior.
4. Classify each finding before changing code:
   - Confirmed bug: reproducible or strongly supported by code evidence.
   - Suspected risk: plausible issue that cannot yet be confirmed safely.
   - Intentionally unmodified: a real issue or risk left unchanged because the safe fix is too large, too uncertain, or requires user approval.
5. Prefer the smallest safe change that fixes a confirmed issue. Preserve existing behavior everywhere else, and reuse existing helpers, abstractions, and patterns before introducing new ones.
6. Follow the repository's current coding style first. If the surrounding code is inconsistent or unclear, follow the language or framework standard style instead.
7. Ask before making large or wide-ranging changes. This includes architecture changes, public API or contract changes, schema changes, dependency changes, broad renames, large refactors, or any fix that materially changes behavior outside the bug itself.
8. If a safe fix cannot be verified locally, explain the issue, the risk, and the smallest candidate fix rather than applying a speculative change.
9. Validate with existing tests, builds, linters, or diagnostics when they already exist and are relevant. Do not add new tooling just to support the fix unless the user asks for it.
10. Perform a self code review after every change. Re-read the diff in context, check for unintended edits, broken imports, type or signature mismatches, missed edge cases, compatibility-sensitive typos or renames, and style drift. Confirm the change is minimal and that unrelated code was not altered.

## Guardrails

- Do not make changes just to match personal style.
- Do not bundle unrelated cleanup into the same change unless the user asked for a broad sweep.
- Do not silently weaken security, validation, or error reporting to make a test pass.
- Do not use broad catch blocks, silent fallbacks, dead code, or success-shaped no-op handling as shortcuts unless the existing code clearly relies on that pattern and the change remains safe.
- When evidence is insufficient, report a suspected risk instead of applying a speculative fix.
- When fixing typos, keep the change surgical. Ask before wide renames across public APIs, serialized fields, database columns, migrations, or compatibility-sensitive user-facing surfaces.
- Be extremely careful not to break existing working code while fixing the target issue.
- Treat obvious security issues as in scope, but do not claim a formal security audit if you only performed a best-effort code review pass.

## Output Rules

- Summarize what scope you inspected and what evidence guided the inspection.
- For each fix or important finding, state its classification, what was wrong, why it was a bug or risk, and what minimal change was made or intentionally not made.
- List any important findings you intentionally did not change and why.
- Report what validation you ran and any limits on verification.
- State the result of the self review, including any residual risk or follow-up suggestion.
- Keep chat replies in the user's language and preserve the repository's language and style conventions in code, comments, and docs.

## Suggested Prompts

- `Inspect this repository for bugs and fix the safe ones. Ask before any large changes.`
- `Review src/ for correctness and security issues, then apply the minimal safe fixes.`
- `Find and fix bugs in these files while preserving existing behavior and self-reviewing your changes.`
