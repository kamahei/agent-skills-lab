# Handoff Pack

Use the smallest document set that removes ambiguity before the Copilot run.

## Default Files

- `docs/copilot-implementation-spec.md`
  - Purpose: define the requested change precisely.
  - Include:
    - objective and user-visible outcome
    - confirmed requirements
    - explicit assumptions
    - non-goals
    - exact files, modules, or areas to inspect
    - target behavior and edge cases
    - acceptance criteria
- `docs/copilot-execution-brief.md`
  - Create only when the task is not a narrow but still handoff-worthy green case.
  - Purpose: tell Copilot how to implement the change without reopening design.
  - Include:
    - implementation order
    - repository patterns to preserve
    - allowed and forbidden changes
    - validation commands
    - expected summary format after implementation
- `docs/copilot-one-shot-prompt.md`
  - Purpose: the final prompt to paste into Copilot or feed to a CLI.
  - Keep it concise and operational.
  - Point back to the spec and execution brief as the source of truth.

## Narrow Handoff Shortcut

For a narrow but still handoff-worthy `green` task, skip `docs/copilot-execution-brief.md` and fold the critical execution guidance into `docs/copilot-implementation-spec.md`.

## Medium Task Rules

Add `docs/copilot-execution-brief.md` when any of these are true:

- the task touches multiple modules
- the order of changes matters
- the repository has strict patterns to preserve
- validation is non-obvious
- there are important out-of-scope boundaries

## Spec Checklist

Before handing off to Copilot, ensure the spec answers these questions:

1. What exactly must change?
2. Which files or directories are in scope?
3. Which existing patterns or helpers should be reused?
4. What must not change?
5. What counts as done?
6. What commands should verify the result?

## One Shot Readiness

The pack is ready only if Copilot can execute without reopening product or architecture discovery. If the prompt still needs phrases like `decide the best approach`, `explore the codebase`, or `consider multiple options`, the handoff is still under-specified.
