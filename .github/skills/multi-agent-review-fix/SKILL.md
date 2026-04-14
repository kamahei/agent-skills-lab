---
name: multi-agent-review-fix
description: Run the `/multi-agent-review-fix` workflow where the current agent makes or inspects the requested code change, then uses 2-agent or 3-agent review on only the modified code and applies only safe agreed fixes. Use only when the user explicitly invokes `/multi-agent-review-fix`. Do not use for generic code review, generic bug fixing, or multi-agent implementation without that exact skill invocation.
---

# Multi Agent Review Fix

## Activation

- Activate only when the user explicitly invokes `/multi-agent-review-fix`.
- Do not activate for generic requests about code review, bug fixing, second opinions, or multi-agent implementation unless `/multi-agent-review-fix` is explicitly specified.
- Default to 2 agents when the user does not specify a count.
- Use multi-agents only for review of the actual changed code. Do not ask non-current slots to implement the change or edit repository files.
- If the user asks for a code change and no candidate diff exists yet, the current agent performs the initial implementation first, then starts the review phase.
- Keep the participant set fixed for the run: the current agent plus the selected non-current slots only.
- Count only genuinely independent model families. A slot that resolves to an already-participating family does not satisfy the requested count.

## Inputs

- Expected context: a repository with either a requested code change to make first or an existing candidate diff, staged change, or patch to review.
- Optional inputs: target files, diff base, staged-versus-unstaged preference, failing tests, diagnostics, logs, explicit model selection, and whether to stop after review or apply the safe fixes.

## Review Scope

- Review the actual diff in the working tree, staged changes, or a user-provided patch.
- Limit review to changed files, changed hunks, and the minimum surrounding context needed to reason about correctness, safety, and compatibility.
- Expand beyond changed lines only when directly touched interfaces, callers, tests, or nearby invariants must be checked to confirm a finding or apply a safe fix.
- If unrelated dirty changes exist, isolate the intended review scope before invoking non-current slots. If the scope cannot be isolated safely, ask the user to confirm the base, files, or patch to review.
- Do not turn this workflow into a broad repository audit or a full-codebase cleanup pass.

## Participant Selection

Allowed baselines:

- `claude-opus-4.6` or a higher Claude Opus version
- `gpt-5.4` or a higher GPT version
- `gemini-3.1-pro-preview` or a higher Gemini 3.1 version
- `gemini-3-pro-preview` or a higher Gemini preview fallback
- `Current AI model`

Default sets:

- Base default sets (before family filtering):
	- 2-agent: `claude-opus-4.6` + `Current AI model`
	- 3-agent: `claude-opus-4.6` + `gpt-5.4` + `Current AI model`

- Family-aware defaults (must override the base defaults when needed):
	- If `Current AI model` is Claude family, use `gpt-5.4` as the 2-agent non-current slot.
	- If `Current AI model` is Claude family, use `gpt-5.4` + Gemini (`gemini-3.1-pro-preview` or `gemini-3-pro-preview`) for 3-agent mode.
	- If `Current AI model` is GPT family, use Claude (`claude-opus-4.6` or `claude-sonnet-4.6+`) as the 2-agent non-current slot.
	- If `Current AI model` is Gemini family, use Claude (`claude-opus-4.6` or `claude-sonnet-4.6+`) as the 2-agent non-current slot.

Selection rules:

- Resolve `Current AI model` to its actual runtime model before finalizing the set.
- Keep model families distinct, not just model names distinct.
- A non-current reviewer in the same family as `Current AI model` is never allowed, even if it is a different model tier (for example, Sonnet vs Opus).
- If `Current AI model` conflicts by family with a non-current slot, keep `Current AI model` and replace the conflicting slot.
- Use this replacement priority among non-conflicting families: GPT, Gemini, Claude.
- If the user explicitly names 2 or 3 allowed models, use that set after applying the same family rule.
- If the explicit set still cannot satisfy the requested independent count, fall back to the default set.
- Use `gemini-3-pro-preview` as the portable Gemini baseline.
- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, prefer `pinned-gemini-3-1-pro-preview` before `pinned-gemini-3-pro-preview`.
- In Copilot CLI or when client support is unclear, prefer `pinned-gemini-3-pro-preview` before `pinned-gemini-3-1-pro-preview`.

## Depth Controls And Reporting

- Prioritize model-family correctness and slot availability over aggressive depth-control requests.
- Accept only `claude-opus-4.6` or `claude-sonnet-4.6` or higher as valid Claude participants.
- Treat explicit Claude runtimes below 4.6, including `claude-sonnet-4.5`, as unavailable rather than as successful fallbacks.
- Use vendor-native setting names only.
- Prefer `reasoning_effort: xhigh` for GPT or Codex when available, but allow `high` or default behavior if stricter settings reduce availability.
- Prefer a higher Gemini `thinking level`, but allow default Gemini behavior if explicit settings reduce availability.
- Prefer a higher Claude thinking mode such as `extended thinking` or `adaptive thinking`, but allow default Claude behavior if explicit settings reduce availability.
- Do not translate Claude or Gemini settings into `xhigh` unless the runtime explicitly exposes `xhigh`.
- Report model metadata only when the user explicitly asks for it.
- When reporting metadata, use runtime-exposed field names, say `not exposed by runtime` when necessary, and say `requested` rather than `used` when only the request is known.

## Pinned Agents

Supported custom-agent locations:

- `~/.copilot/agents/`
- `.github/agents/`

Mappings:

- `pinned-claude-opus-4-6` -> `claude-opus-4.6`
- `pinned-claude-sonnet-4-6` -> `claude-sonnet-4.6`
- `pinned-gpt-5-4` -> `gpt-5.4`
- `pinned-gemini-3-1-pro-preview` -> `gemini-3.1-pro-preview`
- `pinned-gemini-3-pro-preview` -> `gemini-3-pro-preview`

Execution rules:

- Prefer the mapped pinned agent when it exists.
- Treat the mapped agent file's `model:` field as the source of truth when the runtime model name is not exposed.
- Do not treat current-model substitution as a successful pin.
- If a pinned slot returns a usable independent review report, do not run another fallback for that slot.
- Use best-effort fallback only when the mapped agent is missing, unavailable, errors, or returns no usable independent review report.
- Exclude any slot that resolves to the current model family or another already-counted family.
- This exclusion applies even when the slot appears stronger by tier within that family (for example, do not select `claude-opus-4.6` when `Current AI model` is `claude-sonnet-4.6`).
- Treat `SLOT_UNAVAILABLE` as unavailable, not as a review report.

Claude-specific fallback:

- Try `pinned-claude-opus-4-6` first.
- If the Claude attempt returns `SLOT_UNAVAILABLE`, the current model family, any non-Claude family, or any explicit Claude runtime below 4.6, retry once with a softer or default Claude request.
- If the Claude slot still cannot produce an independent Claude-family participant, try `pinned-claude-sonnet-4-6` or an explicit Claude Sonnet fallback once.
- Count a Claude fallback only when it is `claude-sonnet-4.6` or higher.
- If `pinned-claude-opus-4-6` is unavailable but `pinned-claude-sonnet-4-6` succeeds at version 4.6 or higher, count `pinned-claude-sonnet-4-6` as the Claude participant and say that `pinned-claude-opus-4-6` was unavailable and `pinned-claude-sonnet-4-6` fallback was used.
- If both `pinned-claude-opus-4-6` and `pinned-claude-sonnet-4-6` fail, report that no independent Claude participant could be obtained.

Gemini-specific fallback:

- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, try `pinned-gemini-3-1-pro-preview` first.
- In Copilot CLI or when client support is unclear, try `pinned-gemini-3-pro-preview` first.
- If the first Gemini attempt returns `SLOT_UNAVAILABLE`, the current model family, or any non-Gemini family, retry once with a softer or default Gemini request.
- If the first Gemini slot still cannot produce an independent Gemini-family participant, try the other Gemini preview slot or one explicit Gemini fallback once.
- If the first Gemini slot is unavailable but the other Gemini slot succeeds, count the successful Gemini slot as the Gemini participant and say which Gemini fallback was used.
- If both `pinned-gemini-3-1-pro-preview` and `pinned-gemini-3-pro-preview` fail, report that no independent Gemini participant could be obtained.

## Review Rules

- Give every participant the same task, diff, constraints, diagnostics, and local context.
- Each participant reviews the same candidate diff. Do not ask participants to produce competing implementations.
- Classify findings as `confirmed bug or regression`, `high-confidence risk`, `non-blocking suggestion`, or `no issue found`.
- Prefer findings backed by the diff, surrounding code, diagnostics, tests, or repository conventions over speculative concerns.
- Prioritize correctness, regressions, security, data integrity, API or type contract mismatches, missing validation, broken tests, concurrency problems, resource handling, and error-path gaps.
- Ignore purely stylistic nits, speculative refactors, and unrelated pre-existing issues unless the user explicitly asks for broader cleanup.
- Clearly separate issues introduced by the current change from older issues merely discovered nearby.

## Fix Application Rules

- Only the current agent edits the real repository files.
- Apply only findings that are consensus-backed or strongly supported by local evidence and are low risk to correct surgically.
- Prefer the smallest safe fix that resolves the reviewed issue while preserving the user's intended change.
- Do not overwrite unrelated user edits or expand scope into broad cleanup.
- Ask before architecture, schema, dependency, public API, or other wide-impact changes.
- After applying fixes, review the resulting diff in context before concluding.
- Allow at most 2 review-and-fix rounds after the initial implementation or initial diff intake. Stop early if no new technical evidence appears.

## Workflow

1. Restate the task, constraints, review base, and whether the run is `2-agent` or `3-agent`.
2. Make the requested code change with the current agent only, or inspect the existing candidate diff if the user already has one.
3. Determine the exact review scope from the actual diff and collect the minimum needed context, diagnostics, and relevant validation commands.
4. Resolve the current runtime model and finalize the independent participant set.
5. Print `Models in use:` with model names only.
6. Print `Pinned agents used:` separately when pinned custom agents participate.
7. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
8. Produce the current-agent self-review first, then one review report per non-current slot on the same diff.
9. Compare findings in the current agent only. Prefer issues supported by code evidence over stylistic preference.
10. Apply only safe agreed fixes. If resolving a finding requires broader changes, stop and ask before proceeding.
11. Run the narrowest useful validation available and review the resulting diff.
12. If material fixes introduced new modified hunks, run at most 1 additional review round on those new hunks only. Stop early if no new technical evidence appears.
13. Present the final result when participating agents align. If they do not fully align, choose the safer, more repository-consistent fix set and clearly note any unresolved disagreement.

## Output Rules

- State the requested consensus count and the achieved independent count.
- State the reviewed scope briefly, such as the relevant files, patch, staged diff, or working-tree diff.
- List only model names under `Models in use:`.
- If a pinned participant does not expose its runtime model, use the pinned agent's configured `model:` value as the model name.
- Report custom agent names separately from model names.
- Do not list collapsed or mismatched slots as independent participants.
- If fewer than 2 independent participants remain, explicitly say that multi-agent review could not be fully completed.
- If a requested `3-agent` run ends with only 2 independent participants, explicitly say that it degraded to a `2-agent` run.
- If a Claude slot resolves to `claude-sonnet-4.5` or any lower Claude version, explicitly exclude it from the participant count.
- Clearly separate fixes that were applied from findings intentionally left unchanged.
- Report what validation ran and any residual risk or follow-up that still matters.
- Keep the final answer concise and action-oriented.

## Suggested Prompts

- `/multi-agent-review-fix make this change, then review only the modified diff in 2-agent mode and apply safe fixes`
- `/multi-agent-review-fix review these staged changes in 3-agent mode and fix only consensus-backed issues`
- `/multi-agent-review-fix implement the requested fix, run review only on touched files, and stop after high-confidence corrections`
- `/multi-agent-review-fix inspect this existing patch with current AI model and claude-opus-4.6, then apply only the safe agreed fixes`
