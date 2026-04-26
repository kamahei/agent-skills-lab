---
name: project-agents-hardening
description: Use when Codex or another agent is asked to harden a real project's AGENTS.md, source SKILL.md, or related AI instructions after implementation, bugfix, documentation, review feedback, failed validation, or repeated agent mistakes reveal a preventable behavior gap. Treat explicit skill mentions, slash-style invocations, review feedback files, inline feedback, or current-session context as inputs. Apply safe pending reviewed fixes first when in scope, then update the target project's effective AI instructions.
---

# Project AGENTS Hardening

## Activation

- Use this skill when a real project's AI instructions should be improved after an implementation, fix, review, failed validation, or repeated agent mistake reveals a reusable guidance gap.
- Use it when review feedback says the agent missed a project rule, ignored a workflow, edited the wrong scope, skipped validation, used the wrong file placement, or repeated a preventable mistake.
- Use it when the user explicitly names this skill, asks to harden project agent instructions, or sends a slash-style message such as `/project-agents-hardening <review-feedback-file>`.
- Use it to harden the target project's effective `AGENTS.md` or equivalent AI instruction files, not the repository that merely stores this skill, unless that repository is explicitly the target project.
- Do not use it for one-off code review fixes that do not imply a reusable instruction change.

## Inputs

- Target project root or the file path whose effective agent instructions should be hardened.
- Triggering user message and any parsed arguments, which may be a review feedback file path, inline review feedback, target project context, or empty.
- Original task request and any follow-up constraints.
- Review feedback, failure report, validation output, or concrete symptom that exposed the instruction gap.
- Files changed during the original task.
- Skills, AGENTS files, instruction files, prompts, guides, templates, and other documents read during the original task.
- Any known constraints, such as read-only vendor files, protected docs, tool-specific instruction formats, or repository areas that must not be edited.

## Invocation Handling

- In Codex, treat the triggering user message as the invocation input. Do not assume a native slash-command argument variable exists.
- If the user sends a slash-style message, parse any text after `/project-agents-hardening` as the argument string.
- If the skill triggers from natural language or an explicit path mention, treat that user text as the argument string.
- If a tool-specific wrapper provides an argument variable, map that value into the same modes below.

## Input Modes

- `/project-agents-hardening <review-feedback-file>`:
   - Treat the argument as a review feedback file or path when it resolves to a readable file.
   - Read the review file, identify the reviewed implementation or documentation work, and extract actionable review items.
   - Determine whether each reviewed fix is already applied. If a safe, narrow, in-scope fix is still pending, apply it before hardening instructions.
   - After fixes are applied or explicitly deferred, update the target project's effective `AGENTS.md` or related AI instructions based on the reusable process gap.
- No explicit arguments:
   - Use the implementation, fix, review, validation, terminal, and diff context from the current session.
   - If the same-session context does not contain a concrete review, failure signal, or completed change to learn from, ask for the missing review or failure signal instead of inventing a lesson.
- Other arguments:
   - Treat inline text as review or failure context when it contains concrete feedback.
   - Treat paths or project names as target-project context when they do not resolve to a review file.

## Target Resolution

1. Identify the real target project before editing. Use the user's explicit path when provided.
2. If multiple workspace folders or nested projects exist, choose the project that owns the reviewed implementation or ask one short question when ownership is unclear.
3. Locate the effective AI instruction files for that target project, including root or nearest-scope `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, and tool-specific equivalents.
4. Treat `AGENTS.md` as the preferred cross-agent source of truth when it exists in the target project and the lesson is broadly applicable.
5. Do not update this skill repository's own `AGENTS.md` just because the skill is stored here. Only update it when the skill repository itself is the target project.

## Review Fix Phase

1. Resolve the review source from the invocation mode: review feedback file, inline feedback, or current-session context.
2. Extract actionable review items separately from instruction-hardening lessons.
3. Inspect the target project state to determine which reviewed fixes are already applied, still pending, or no longer relevant.
4. Apply pending reviewed fixes before instruction hardening only when they are safe, narrow, supported by evidence, and within the original task or explicit user scope.
5. Ask or defer when a reviewed fix requires architecture changes, schema or API changes, dependency changes, broad refactors, unclear ownership, or risky behavior changes.
6. Validate newly applied fixes with the narrowest relevant tests, builds, linters, diagnostics, or manual checks available.
7. Proceed to instruction hardening only after reviewed fixes are applied, confirmed already present, or intentionally deferred with a clear reason.

## Workflow

1. Resolve the invocation mode and target project before editing.
2. Reconstruct the original execution path: task, selected skill or workflow, documents read, files changed, validation performed, and review or failure signal received.
3. Complete the Review Fix Phase when review feedback identifies implementation, documentation, or configuration fixes that may still be pending.
4. Classify each hardening issue before editing instructions:
   - Confirmed instruction gap: evidence shows clearer project guidance would likely have prevented the miss.
   - Suspected instruction gap: the issue may be preventable, but evidence is incomplete.
   - Task-specific preference: useful for the current task, but not a durable project rule.
   - Intentionally unmodified: a real issue left unchanged because it needs user approval, broader policy changes, or unavailable context.
5. Diagnose why the issue was not avoided earlier. Common causes include missing instruction, low-salience instruction, conflicting docs, wrong skill activation, incomplete target resolution, insufficient local context, inadequate validation, or an ambiguous user request.
6. If the original task used a repository skill and that skill's `SKILL.md` is part of the target project, update that `SKILL.md` first when the feedback exposes a reusable skill-workflow gap.
7. Among the documents read during the original task, update the document expected to have the highest corrective effect. Prefer the narrowest source of truth that future agents will actually read.
8. Strengthen the target project's `AGENTS.md` when the rule should apply broadly across future project work. Add concise, reusable guidance in the section where future agents are most likely to look.
9. Update tool-specific instruction files only when the lesson is tool-specific or the tool-specific file is the effective instruction surface for the target project.
10. Keep the edit narrow. Extract the reusable project rule behind the review instead of copying one-off reviewer wording.
11. Preserve existing scope, tone, and document structure. Update existing sections in place before adding new sections.
12. Validate the result: frontmatter syntax where present, relative paths, heading hierarchy, duplicate or conflicting instructions, and whether the new rule would likely have changed the original execution.

## AGENTS.md Hardening Checklist

- Add the missing project rule at the smallest durable location.
- Make trigger conditions explicit: when the agent must apply the rule, ask, validate, or stop.
- Include the expected action, not only the desired outcome.
- Preserve priority among instructions, skills, user requests, safety rules, and repository conventions.
- Avoid vague wording such as `as appropriate`, `make sure`, or `handle carefully` unless paired with concrete checks.
- Prefer reusable examples only when they reduce ambiguity.
- Do not turn a single subjective review preference into broad policy.
- Do not add long narratives that future agents are unlikely to read.

## Document Priority

Use this priority order when multiple target-project documents could be edited:

1. The source `SKILL.md` used for the original target-project task, when the review exposes a reusable skill-workflow gap.
2. The target project's effective `AGENTS.md`, when the lesson should apply broadly across future work.
3. The highest-impact document among those read during the original task, when it is more specific and more likely to prevent recurrence than `AGENTS.md`.
4. Scoped instruction files or tool-specific instruction docs, when the gap applies only to a language, folder, tool, or agent client.
5. Human-facing docs, only when humans also need the process rule.

If review feedback exposes both a pending code, documentation, or configuration fix and an instruction gap, apply or explicitly defer the reviewed fix before editing AI instructions so hardening reflects the corrected final state.

## Guardrails

- Do not claim the updated instructions guarantee future correctness. Aim to reduce recurrence.
- Do not edit unrelated project docs just because they mention similar topics.
- Do not turn this skill into an open-ended review-fix workflow. Apply only safe, narrow, in-scope reviewed fixes before hardening instructions.
- Do not weaken existing validation, safety, security, source-control, or edit-scope rules.
- Do not create duplicate AI-specific variants when one shared `AGENTS.md` rule is enough.
- Ask before broad project policy changes, schema or API conventions, dependency policy changes, or edits across many unrelated documents.
- When evidence is insufficient, record the uncertainty and make only the smallest justified instruction change.
- Keep generated or edited instruction docs in the project's existing language unless the user explicitly requests another language.
- Keep chat replies in the user's language.

## Output Rules

- State the target project and prevention scope.
- State whether the run used a review feedback file, inline review context, or current-session context.
- State which reviewed fixes were already applied, newly applied, or intentionally deferred.
- State the issue being prevented and the diagnosed cause.
- List each updated instruction file and why it was the right place to edit.
- Mention important candidate documents intentionally not changed and why.
- Report validation performed and any limits on verification.
- State the self-review result, including whether the new guidance would likely have changed the original execution.

## Suggested Prompts

- `Use project-agents-hardening path/to/review.md to apply pending review fixes and then harden this project's AGENTS.md.`
- `/project-agents-hardening`
- `Harden the effective AGENTS.md for the real project that received this implementation review.`
- `Investigate why this agent miss happened, then update the target project's AGENTS.md or related instructions.`
