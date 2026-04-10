---
name: spec-to-copilot-implementation
description: Convert a user request into an implementation-ready design, specification, and GitHub Copilot handoff pack, then generate one dense final Copilot prompt so the actual code work can be requested in a single premium request. Use when Codex or Claude should do the planning, scope control, architecture decisions, acceptance criteria, and implementation instructions first in order to reduce Codex or Claude credits or GitHub Copilot premium-request usage, especially when the main cost is large input-token repository reading or large output-token code generation that should be bundled into one Copilot request. Do not use for small tasks that Codex or Claude should implement directly.
---

# Spec To Copilot Implementation

## Activation

- Use this skill when the user wants the current AI to think, design, and write the implementation brief first, then hand the actual coding pass to GitHub Copilot in one request.
- Use it when the user explicitly wants to reduce Codex or Claude credits, reduce GitHub Copilot premium-request usage, or front-load the design work before invoking Copilot.
- Use it when the biggest cost driver is the amount of repository context to inspect, the number of files to modify, or the amount of code Copilot can emit in one long run after the current AI has already pinned down the approach.
- Use it for bounded feature work, targeted refactors, scaffolded greenfield work, and medium-to-large bugfixes where the current AI can inspect the repository and remove ambiguity before the Copilot handoff.
- Do not use it for tiny requests, single-file touchups, or low-token changes that the current AI can implement faster directly.
- Do not use it for broad audits, emergency debugging, production firefights, or work that still depends on unresolved product or architecture decisions.
- If the requested change is too broad for one safe Copilot pass, narrow the scope or switch to a phased plan instead of forcing a one-shot request.

## Inputs

- Expected context: a user request, the target repository or files, and enough local context to decide the implementation approach before handing off to Copilot.
- Helpful inputs: preferred stack, exact files or modules in scope, validation commands, forbidden changes, dependency constraints, schema or API constraints, and whether the current AI should stop at the handoff pack or also invoke Copilot.
- Optional inputs: a hard request budget such as `one premium request only`, a target model or Copilot client, whether the user wants English or another language for the generated documents, and whether the user wants the current AI to keep small tasks local instead of handing them to Copilot.

## One Shot Decision

- Judge the task on 2 axes before choosing Copilot:
  - `handoff ROI`: how much Codex or Claude cost is avoided by pushing a large inspection or implementation pass into one Copilot request
  - `specifiability risk`: how likely the task is to go wrong unless the current AI makes more decisions first
- Estimate `handoff ROI` primarily from token pressure:
  - high input-token pressure: many files, configs, tests, or call sites must be read before implementation
  - high output-token pressure: many files or sizable code blocks will likely be written or refactored
  - low handoff ROI: a small local fix, a trivial single-file change, or any task the current AI can finish faster than writing the handoff
- Then classify the task:
  - `green`: high or medium handoff ROI, low specifiability risk, clear acceptance criteria, and no unresolved architecture or environment blocker. This is the ideal one-shot Copilot case.
  - `yellow`: high or medium handoff ROI, but the task is still too fuzzy or cross-cutting until the current AI tightens file boundaries, assumptions, non-goals, and validation expectations. It can still become a one-shot Copilot task after that tightening.
  - `red`: do not send as a one-shot Copilot task. This includes 2 very different cases:
    - `red-too-small`: the task is too small to justify the handoff overhead and should be implemented directly in Codex or Claude.
    - `red-too-risky`: the task is too ambiguous, too architecture-heavy, or too dependent on schema, infra, secrets, or unresolved constraints to compress safely into one Copilot request.
- Proceed with a one-shot Copilot handoff for `green`.
- Proceed for `yellow` only after shrinking the scope, fixing the target files, making assumptions explicit, and turning the request into a concrete implementation brief.
- Do not force a one-shot Copilot implementation for `red`. For `red-too-small`, implement directly in the current AI. For `red-too-risky`, ask one blocking question or split the work into phases.

## Decision Signals

- Favor Copilot handoff when any of these are true and the task is still specifiable:
  - the current AI would need to read many repository files just to gather context
  - the implementation will likely touch many files or emit a large amount of code
  - the user explicitly wants to compress a large implementation into one premium request
- Favor direct Codex or Claude implementation when any of these are true:
  - the task is narrow, local, and quick enough that writing the handoff would cost more than doing the change
  - the change is a small bugfix, copy edit, rename, or straightforward localized edit
  - the expected code output is small and the investigation cost is low
- Favor `yellow` instead of `green` when Copilot could handle the volume, but only after the current AI chooses the boundaries and removes ambiguity.
- Favor `red-too-risky` when even a detailed brief would still leave too many material choices open.

## Task Fit Checklist

Use this checklist before deciding to invoke the skill.

1. Will the current AI need to inspect many files, configs, tests, or call sites before implementation?
2. Will the implementation likely modify several files or generate a large amount of code?
3. Would the user benefit from compressing that heavy read or heavy write pass into one GitHub Copilot request?
4. Can the current AI name the likely target files or directories before handing off?
5. Can the current AI define clear acceptance criteria and at least one realistic validation command?
6. Can the current AI state important non-goals and forbidden edits so Copilot does not wander?
7. Is the task larger than a tiny local edit, copy change, rename, or one-file touchup?
8. Does the task avoid unresolved schema, infra, secret, auth-provider, or architecture decisions that would still need interactive discovery?
9. Can the task be made concrete without asking Copilot to choose among multiple major designs?
10. Is writing the handoff likely cheaper than having Codex or Claude do the entire implementation directly?

Decision rule:

- Strong fit: items 1, 2, 3, 4, 5, 6, 9, and 10 are mostly `yes`, item 7 is `yes`, and item 8 is also `yes`. Treat this as `green`.
- Tighten first: items 1, 2, 3, and 10 are `yes`, but items 4, 5, 6, or 9 are not solid yet. Treat this as `yellow` and remove ambiguity before handoff.
- Do not use the skill because the task is too small: items 1, 2, 3, or 10 are mostly `no`, or item 7 is `no`. Treat this as `red-too-small`.
- Do not use the skill because the task is too risky: item 8 is `no`, or item 9 stays `no` even after tightening. Treat this as `red-too-risky`.

## Deliverable Strategy

- Prefer the smallest document set that fully constrains Copilot.
- Use the default handoff pack in `references/handoff-pack.md`.
- For narrow but still handoff-worthy `green` tasks, collapse the output to:
  - `docs/copilot-implementation-spec.md`
  - `docs/copilot-one-shot-prompt.md`
- For medium tasks or repo work with meaningful constraints, add:
  - `docs/copilot-execution-brief.md`
- Only create extra planning files when they materially improve implementation accuracy. Do not spend tokens on decorative or repetitive docs.

## Workflow

1. Read only the local context needed to make the implementation concrete. Prefer the relevant files, tests, configs, and current patterns over a whole-repository scan.
2. Normalize the request into confirmed requirements, assumptions, explicit constraints, non-goals, and a done definition.
3. Estimate `handoff ROI` from likely input-token and output-token volume, then classify the task as `green`, `yellow`, `red-too-small`, or `red-too-risky`.
4. If the task is `red-too-small`, stop using this skill and implement the change directly in the current AI unless the user explicitly insists on Copilot anyway.
5. If the task is `yellow`, tighten the scope before writing the handoff. Fix the target files, interfaces, validation path, and acceptance criteria so Copilot is not asked to invent them.
6. If the task is `red-too-risky`, do not write a one-shot Copilot handoff as if it were ready. Ask one blocking question or split the work into phases.
7. Pre-make the important decisions yourself:
   - target files and modules
   - data flow or control flow changes
   - API or type changes
   - edge cases and failure handling
   - validation commands and acceptance checks
   - non-goals and things Copilot must not change
8. Write the implementation spec. Use `references/handoff-pack.md` for the minimum required sections.
9. If the change is not trivially small, write an execution brief that tells Copilot exactly how to approach the work, in what order, and what repository patterns to preserve.
10. Generate the final Copilot prompt with `references/copilot-prompt-template.md`. The prompt should tell Copilot to read the handoff docs first, then implement the code directly without re-opening the design phase.
11. Self-review the handoff before execution:
   - Can Copilot identify the files to inspect?
   - Are acceptance criteria measurable?
   - Are important edge cases explicit?
   - Are validation commands real and relevant?
   - Are out-of-scope changes and forbidden edits explicit?
12. If the user asked for execution and Copilot is available, run Copilot once with the final prompt. Otherwise stop at the finished handoff pack.
13. After any Copilot execution, inspect the actual diff, touched files, and validation output in the current AI before accepting the result. Do not treat Copilot output as final truth.
14. If Copilot missed scope, touched the wrong areas, or failed validation, apply the retry rules below instead of broadening the prompt blindly.

## Native Copilot CLI Example

Use a shell-appropriate equivalent of one of these commands after writing `docs/copilot-one-shot-prompt.md`.

PowerShell:

```powershell
$prompt = Get-Content -Raw docs/copilot-one-shot-prompt.md
copilot -p $prompt --allow-all --no-ask-user --silent
```

POSIX shells:

```bash
copilot -p "$(cat docs/copilot-one-shot-prompt.md)" --allow-all --no-ask-user --silent
```

## Post Run Review And Retry Rules

- Always review the Copilot-produced diff locally in the current AI before concluding.
- Check three things after the run:
  - whether the touched files stayed inside the intended scope
  - whether the documented validation actually ran and passed
  - whether the implementation matched the explicit acceptance criteria and non-goals
- If the result is close but not fully correct, prefer a narrowed follow-up prompt or a small local fix over a broad retry.
- If the result wandered outside scope, tighten the file list, forbidden edits, and acceptance criteria before any retry.
- Do not immediately retry with a looser or broader prompt. That usually burns extra premium requests and defeats the purpose of this skill.
- Default to at most one narrowed Copilot retry. If the result still misses the target, finish the work locally in the current AI or split the task into phases.

## Copilot Prompt Rules

- Make the current AI do the ambiguity removal. Do not ask Copilot to discover product requirements, choose among several architectures, or explore the repository broadly unless that exploration is tightly bounded.
- Use Copilot for the heavy reading or heavy writing pass, not for tiny edits that the current AI could finish more cheaply.
- Put the authoritative requirements in the docs, not in scattered chat text.
- Tell Copilot what to read first, what to edit, what not to edit, and how to validate.
- Make it clear that the resulting diff will be reviewed by the current AI and therefore must stay bounded and easy to audit.
- Prefer direct imperatives such as `Implement`, `Update`, `Preserve`, `Do not`, and `Run`.
- Require Copilot to keep the scope bounded and to stop only for hard blockers such as missing secrets, unavailable external systems, or irreconcilable repository contradictions.
- Ask Copilot to summarize changed files and validation at the end so the current AI can review the result quickly.
- Keep the final prompt dense and operational. Avoid long narrative context that does not change implementation behavior.

## Guardrails

- Do not hand Copilot a fuzzy brief and hope it designs the solution for you. Front-load the design decisions in the current AI.
- Do not send a tiny local task to Copilot just because the user mentioned premium requests. Small tasks should usually stay in Codex or Claude.
- Do not ask Copilot to do planning, architecture review, implementation, test strategy design, and documentation authoring in one vague request when the goal is to save premium requests.
- Do not produce oversized doc packs for small tasks. More documents are not automatically better.
- Do not accept a Copilot result without reviewing the actual diff and validation output in the current AI.
- Do not hide assumptions. If the user left something important unspecified, either choose a conservative default and record it or ask one short question when the decision is too risky.
- Do not treat a one-shot Copilot plan as safe when the work needs schema changes, public API changes, new infrastructure, secrets, or wide repository reorganization unless the user explicitly approves that wider blast radius.
- Do not rely on Copilot to infer repository conventions that the current AI can state directly from local inspection.

## Output Rules

- State whether the request was treated as `green`, `yellow`, `red-too-small`, or `red-too-risky`.
- State whether the result stopped at the handoff pack or continued to a Copilot run.
- If Copilot ran, state that the current AI reviewed the resulting diff and validation output.
- List the created or updated handoff files.
- If the task was not a safe one-shot candidate, state the recommended split or blocking reason clearly.
- Keep chat replies in the user's language. Write generated docs in English unless the user explicitly asks for another language.

## Resources

- `references/handoff-pack.md`: minimum document set and contents for a Copilot implementation handoff.
- `references/copilot-prompt-template.md`: reusable structure for the final one-shot Copilot prompt.

## Suggested Prompts

- `Use $spec-to-copilot-implementation to inspect the auth flow across the app router, API handlers, Prisma models, and tests, then write a one-shot GitHub Copilot implementation pack for the full multi-file change.`
- `Use $spec-to-copilot-implementation to analyze the current dashboard modules, export flow, API client, and related tests, then compress the implementation into one final GitHub Copilot prompt.`
- `Use $spec-to-copilot-implementation to do the planning in Codex or Claude for a bounded multi-file refactor, fix the target files and acceptance criteria, and leave only the heavy implementation pass to GitHub Copilot.`

## Sample Input Examples

- `Use $spec-to-copilot-implementation to add email and password login to this Next.js app across the existing Prisma user model, server actions, session handling, middleware checks, login UI, and auth-related tests. Keep the current UI style, avoid new dependencies unless absolutely necessary, and prepare a one-shot Copilot handoff pack only.`
- `Use $spec-to-copilot-implementation to inspect the current React analytics dashboard and design a bounded multi-file feature that adds CSV export, persisted table filters, and the related API wiring. Limit scope to the dashboard modules, API client, and tests, define acceptance criteria, and generate one final Copilot prompt.`
- `Use $spec-to-copilot-implementation to plan and specify a bugfix for duplicate webhook processing in this Node.js service. Read the retry logic, idempotency checks, persistence flow, worker integration, and related tests first, choose the minimal safe fix, document edge cases, and leave the final implementation to GitHub Copilot in one premium request.`
- `Use $spec-to-copilot-implementation to turn the current TypeScript repo into a bounded internal admin tool MVP by deciding the minimal folder structure, route map, data flow, validation approach, and implementation order, then produce the execution brief and a single final Copilot prompt without running Copilot yet.`
- `Use $spec-to-copilot-implementation to prepare a one-shot GitHub Copilot implementation for refactoring the settings area from one large screen into smaller profile, notifications, and billing components, while preserving behavior, routing, validation rules, and tests, and forbidding broad cleanup outside the touched files.`
