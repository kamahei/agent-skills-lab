# Compact AI Doc Template

Use the smallest template that fully constrains the work. Keep docs in English.

## Compression Rules

- Use fixed keys.
- Use one fact per line.
- Omit narrative background unless it changes implementation.
- Replace paragraphs with bullets when possible.
- Name exact files, modules, routes, APIs, tables, commands, and tests when known.
- Prefer `MUST`, `MUST NOT`, `ONLY`, `EXACTLY`, `IF`, `THEN`.
- Delete empty sections.

## Ambiguity Replacements

- Bad: `improve the code`
- Good: `reduce duplicate parsing logic in src/parser.ts and parser.test.ts without changing public behavior`

- Bad: `refactor as needed`
- Good: `edit only src/auth/* and tests/auth/*; do not change shared UI components`

- Bad: `handle edge cases`
- Good: `cover null input, empty string, duplicate event id, and timeout retry`

- Bad: `run tests`
- Good: `run npm test -- auth and npm run lint`

- Bad: `keep it simple`
- Good: `prefer the smallest change that preserves current APIs and avoids new dependencies`

## Minimal Plan Template

```md
# PLAN
goal:
consumer_ai:
mode:
scope_in:
scope_out:
constraints:
assumptions:
steps:
1.
2.
3.
acceptance:
validation:
```

## Minimal Spec Template

```md
# SPEC
task:
consumer_ai:
goal:
must:
- 
must_not:
- 
scope_in:
- 
scope_out:
- 
touch:
- 
preserve:
- 
edge_cases:
- 
acceptance:
- 
validation:
- 
```

## Minimal Instruction Template

```md
# INSTRUCTIONS
consumer_ai:
execute:
inputs:
edit_only:
- 
do_not_edit:
- 
requirements:
- 
non_goals:
- 
checks:
- 
final_report:
- list changed files
- list validation run
- list blockers
```

## Selection Rule

- Use `PLAN` when the implementation should be staged.
- Use `SPEC` when requirements and boundaries matter most.
- Use `INSTRUCTIONS` when the implementation AI should execute immediately.
- Merge templates only when separation would add tokens without adding control.
