---
name: write-ai-implementation-docs
description: Prepare compact English AI-facing plans, specs, and execution briefs from Claude Code. Use when Claude should write low-ambiguity, low-context planning or implementation docs for another AI, including GitHub Copilot, Codex plan mode, or similar workflows.
---

# Write AI Implementation Docs

## Activation

- Use this wrapper when Claude Code should produce a plan, spec, design brief, or execution instructions for another AI to consume.
- Treat `$ARGUMENTS` as the requested outcome, target AI, scope, constraints, and desired document type.
- Keep this wrapper thin. Use the shared skill as the source of truth for document structure, ambiguity control, and compression rules.

## Workflow

1. Read `../../../.agents/skills/write-ai-implementation-docs/SKILL.md`.
2. Read `../../../.agents/skills/write-ai-implementation-docs/references/compact-ai-doc-template.md` if you need the minimal templates or ambiguity replacements.
3. Decide whether the output should be `PLAN`, `SPEC`, or `INSTRUCTIONS`.
4. Inspect only the repository context needed to define explicit scope, constraints, acceptance, and validation.
5. If a missing detail would materially change implementation behavior, ask one short question. Otherwise record a safe assumption.
6. Write the smallest English AI-facing document that fully constrains the work.
7. Add explicit scope boundaries, non-goals, forbidden edits, acceptance, and validation so the downstream AI does not have to infer them.
8. Keep the output dense and operational. Remove filler text, narrative transitions, and vague wording before concluding.

## Usage Examples

- `/write-ai-implementation-docs turn this feature request into a compact English spec for GitHub Copilot with strict file scope and validation`
- `/write-ai-implementation-docs prepare a Codex plan mode document for this refactor with explicit scope_in, scope_out, acceptance, and validation`
- `/write-ai-implementation-docs write AI-only execution instructions for another agent to implement this bugfix without broad cleanup`

## Output Rules

- Keep chat replies in the user's language.
- Keep generated AI-facing docs in English unless the user explicitly requests another language.
- State the chosen document type and intended consumer AI.
- List created or updated doc files.
- State any blocking question or assumption that materially affects implementation.
