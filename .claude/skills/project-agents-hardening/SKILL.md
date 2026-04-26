---
name: project-agents-hardening
description: Harden a real project's AGENTS.md after review feedback or repeated agent mistakes expose a preventable instruction gap. Accepts a review file or no arguments, applies safe pending reviewed fixes first, then updates the target project's effective AGENTS.md or related AI instructions.
---

# Project AGENTS Hardening

## Activation

- Use this wrapper when Claude Code should strengthen a real project's effective `AGENTS.md` or related AI instruction files after review feedback, failed validation, or repeated agent mistakes.
- Treat `$ARGUMENTS` as a review feedback file path, inline review or failure signal, target project context, or empty current-session invocation.
- When invoked as `/project-agents-hardening <review-feedback-file>`, apply safe pending reviewed fixes first, then harden the target project's instructions.
- When invoked as `/project-agents-hardening` with no arguments, use the current session's implementation, fix, review, validation, and diff context.
- Keep this wrapper thin. Use the shared skill as the source of truth for target resolution, document priority, guardrails, validation, and reporting.

## Workflow

1. Read `../../../.agents/skills/project-agents-hardening/SKILL.md`.
2. Resolve whether `$ARGUMENTS` is a review feedback file, inline review context, target project context, or empty current-session invocation.
3. Identify the real target project before editing. Do not update the skill repository's own `AGENTS.md` unless it is explicitly the target project.
4. Reconstruct the original execution path and classify each issue using the shared skill.
5. If reviewed fixes are pending, apply only safe, narrow, in-scope fixes before hardening instructions; ask or defer when fixes are broad or risky.
6. If the original target-project task used an editable repository skill, update that source `SKILL.md` first when the feedback exposes a reusable skill-workflow gap.
7. Update the target project's effective `AGENTS.md` when the lesson should apply broadly across future work.
8. Update scoped or tool-specific instruction files only when they are the highest-impact instruction surface.
9. Validate applied fixes, frontmatter, paths, heading structure, duplicate or conflicting guidance, and wrapper thinness.
10. Self-review the diff before concluding.

## Usage Examples

- `/project-agents-hardening path/to/review.md`
- `/project-agents-hardening`
- `/project-agents-hardening Harden the target project's AI instructions after this missed validation requirement`
- `/project-agents-hardening Identify why this agent mistake happened, then update the effective AGENTS.md only where reusable`

## Output Rules

- Keep chat replies in the user's language.
- Keep generated or edited instruction docs in the target project's existing language unless the user explicitly requests another language.
- State whether a review file, inline review context, or current-session context was used.
- State reviewed fixes that were already applied, newly applied, or intentionally deferred.
- State the target project, updated files, why each was selected, validation performed, and any intentionally unmodified candidate docs.
