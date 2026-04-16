---
name: write-ai-implementation-docs
description: Write compact English planning and implementation docs for another AI to execute, including GitHub Copilot, Codex plan mode, and any workflow where one AI prepares instructions for another AI. Use when Codex needs to produce an AI-facing plan, design brief, specification, or execution instructions with low ambiguity, strict scope, and low context cost. Also use when the user asks for AI-only design, spec, or instruction docs outside plan mode.
---

# Write AI Implementation Docs

## Activation

- Use this skill when the deliverable is a plan, spec, design brief, or execution instructions meant primarily for another AI to read.
- Use it for GitHub Copilot, Codex plan mode, and any workflow where the current AI should prepare the implementation instructions first.
- Also use it when the user does not mention plan mode, but asks for a design document, specification, or implementation handoff for AI execution.
- Do not use it for human-first PRDs, tutorials, onboarding docs, or explanatory docs unless the user explicitly wants AI-first output.

## Inputs

- Expected context: the user request, the target repo or scope, the intended consumer AI if known, and any hard constraints.
- Helpful inputs: exact files or modules in scope, forbidden edits, required validation, desired output format, and whether the doc is AI-only or shared with humans.
- Optional inputs: word budget, preferred section names, preferred strictness, and whether unresolved items should be turned into assumptions or blocking questions.

## Core Rules

- Write AI-facing docs in English unless the user explicitly requests another language.
- Optimize for machine execution, not human readability. If the document is AI-only, prioritize precision and token efficiency over prose quality.
- Allow terse or unnatural wording when that reduces ambiguity or token cost for an AI-only document.
- Keep the document compact. Use the smallest structure that fully constrains the work.
- Remove ambiguity before writing. Replace soft wording with explicit scope, conditions, and acceptance checks.
- Prefer fixed labels, short bullets, and one fact per line over narrative paragraphs.
- Use direct control words such as `MUST`, `MUST NOT`, `ONLY`, `EXACTLY`, `IF`, and `THEN` when they improve precision.

## Workflow

1. Identify the target artifact:
   - plan for staged execution
   - spec for implementation requirements
   - instruction brief for immediate execution
2. Normalize the request into explicit fields:
   - goal
   - scope in
   - scope out
   - constraints
   - expected output
   - acceptance
   - validation
3. Decide whether missing information is blocking:
   - If the missing detail can materially change implementation behavior, ask one short question.
   - Otherwise choose the safest reasonable default and record it as an assumption.
4. Use the smallest matching template from `references/compact-ai-doc-template.md`.
5. Write the document in dense operational form:
   - one requirement per line
   - no filler rationale unless it changes execution
   - explicit file, module, API, or directory names when known
6. Add non-goals and forbidden edits whenever omission could cause scope drift.
7. Add concrete acceptance and validation. Do not stop at generic phrases such as `works correctly` or `run tests`.
8. Self-review the document for:
   - ambiguous words
   - duplicated information
   - missing scope boundaries
   - missing done criteria
   - avoidable token waste

## Guardrails

- Do not write AI-facing docs in Japanese by default.
- Do not use vague terms such as `etc.`, `and so on`, `some`, `appropriate`, `improve`, `optimize`, `clean up`, `refactor`, `handle edge cases`, or `as needed` without an explicit definition.
- Do not ask the implementation AI to discover requirements that the current AI can specify now.
- Do not create a multi-file doc pack when one compact file is enough.
- Do not spend tokens on background narrative, sales language, or human-friendly transitions that do not change execution.
- Do not leave acceptance implicit. State what counts as done.
- Do not leave file scope implicit when the repo scope is known.

## Output Rules

- State the document type and intended AI consumer when reporting the result.
- List created or updated doc files.
- State any blocking question or recorded assumption that materially affects implementation.
- Keep chat replies in the user's language. Keep generated AI-facing docs in English unless the user explicitly requests another language.

## Resources

- `references/compact-ai-doc-template.md`: minimal templates, compression rules, and ambiguity replacements.

## Suggested Prompts

- `Use $write-ai-implementation-docs to prepare a compact English plan for Codex plan mode before implementation.`
- `Use $write-ai-implementation-docs to write an AI-only implementation spec for GitHub Copilot with strict scope, acceptance, and validation.`
- `Use $write-ai-implementation-docs to turn this feature request into a compact English design brief and execution instructions for another AI.`
