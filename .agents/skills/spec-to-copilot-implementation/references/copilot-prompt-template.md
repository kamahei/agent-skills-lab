# Copilot Prompt Template

Use this as the final prompt skeleton after the current AI has already inspected the repository and written the handoff docs.

```md
Implement the requested change in this repository in one pass.

Read these files first and treat them as the source of truth:
- `docs/copilot-implementation-spec.md`
- `docs/copilot-execution-brief.md`

Task:
- Implement exactly what the spec requires.

Execution rules:
- Keep the change within the documented scope.
- Reuse existing repository patterns, helpers, and file organization where possible.
- Do not redesign the architecture unless the docs explicitly require it.
- Do not make unrelated cleanup changes.
- Keep the diff easy to audit by the reviewing AI.
- Do not stop for optional improvements or style-only suggestions.
- Stop only for hard blockers such as missing secrets, unavailable external systems, or a direct contradiction between the docs and the repository state.
- If the docs and repository state conflict materially, report the blocker instead of broadening the task or redesigning it on your own.

Validation:
- Run the documented validation commands when available.
- If a command cannot run, explain the exact blocker briefly.

Final response:
- Summarize changed files.
- Summarize validation results.
- Call out any blocker or assumption that still matters.
- Keep the report concise so the reviewing AI can inspect the result quickly.
```

## Adaptation Notes

- If there is no `docs/copilot-execution-brief.md`, remove that line and move the critical execution constraints into the prompt directly.
- If the task is framework-sensitive, add one short line naming the framework and the pattern to preserve.
- If the repo has a strict no-dependency-change rule, say it directly in the prompt instead of hoping Copilot infers it.
