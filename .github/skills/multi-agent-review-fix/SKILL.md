---
name: multi-agent-review-fix
description: Run `/multi-agent-review-fix` to implement or inspect a change, review only the modified diff with 2 or 3 agents, and apply only safe agreed fixes.
---

# Multi Agent Review Fix

## Activation

- Activate only on the exact `/multi-agent-review-fix` command.
- Default to `2-agent`.
- Non-current slots review the real diff only. They do not implement the change or edit repository files.
- If the user requests a code change and no candidate diff exists yet, the current agent implements first, then starts review.
- Keep a fixed participant set: the current agent plus the selected non-current slots only.
- For default selection, count only distinct model families. If the user explicitly names non-current models, the user selection takes precedence even when a named model shares the current model family.

## Inputs

- Expected context: either a requested code change to make first, or an existing candidate diff, staged change, or patch to review.
- Optional inputs: target files, diff base, staged-versus-unstaged preference, failing tests, diagnostics, logs, explicit model selection, and whether to stop after review or apply safe fixes.

## Review Scope

- Review the actual working-tree diff, staged diff, or user-provided patch.
- Limit review to changed files, changed hunks, and the minimum nearby context needed to reason about correctness and safety.
- Expand beyond changed lines only when directly touched interfaces, callers, tests, or invariants must be checked to confirm a finding or apply a safe fix.
- If unrelated dirty changes exist, isolate the intended review scope before invoking non-current slots. If that cannot be done safely, ask the user to confirm the review base.
- Do not turn this workflow into a broad repository audit or cleanup pass.

## Participant Selection

Allowed baselines:

- Claude: prefer `claude-opus-4.7`, then `claude-opus-4.6`, then `claude-sonnet-4.6+`
- GPT: prefer `gpt-5.5`, fallback `gpt-5.4+`
- Gemini: prefer `gemini-3.1-pro-preview`; portable fallback `gemini-3-pro-preview`
- `Current AI model`

Explicit model aliases:

- Treat `opus-4.7` as `claude-opus-4.7`, `opus-4.6` as `claude-opus-4.6`, and `sonnet-4.6` as `claude-sonnet-4.6`.
- Treat `gpt-5.5`, `gpt-5.4`, `gemini-3.1-pro-preview`, and `gemini-3-pro-preview` as canonical model names.

Default sets:

- `2-agent`: `Current AI model` + `claude-opus-4.7`
- `3-agent`: `Current AI model` + `claude-opus-4.7` + `gpt-5.5`

Family-aware defaults:

- If the current model is Claude, use GPT for `2-agent`, and GPT + Gemini for `3-agent`.
- If the current model is GPT or Gemini, use the Claude fallback chain above for the single Claude slot.

Selection rules:

- `Current AI model` always occupies one slot. Non-current slots: 1 in `2-agent`, 2 in `3-agent`.
- Resolve the current runtime model before finalizing the set.
- If the user explicitly names non-current models (e.g., `3-agent opus-4.7 gpt-5.5`), canonicalize aliases and use `Current AI model` plus those models exactly as requested. Do not run family conflict replacement or collapse exclusion for those explicitly named slots.
- For default selection only, families must be distinct. Never count another slot from the current family, even at a different tier.
- For default selection only, if a slot conflicts by family, keep `Current AI model` and replace the conflicting slot. Use replacement priority `GPT -> Claude -> Gemini`.
- Gemini preference: in VS Code or when `gemini-3.1-pro-preview` is already exposed, prefer `pinned-gemini-3-1-pro-preview`; in Copilot CLI or when support is unclear, prefer `pinned-gemini-3-pro-preview`.

## Depth Controls And Reporting

- Prioritize slot correctness and availability over aggressive depth-control requests.
- Valid Claude participants are `claude-opus-4.6+` or `claude-sonnet-4.6+`. Claude versions below 4.6, including `claude-sonnet-4.5`, are unavailable.
- Use vendor-native setting names only. Prefer higher effort or thinking settings, but soften them if that improves availability.
- Report model metadata only on request. Use runtime-exposed field names, `not exposed by runtime` when needed, and `requested` when the runtime did not confirm actual use.

## Pinned Agents

Supported locations:

- `~/.copilot/agents/`
- `.github/agents/`

Mappings:

- `pinned-claude-opus-4-7` -> `claude-opus-4.7`
- `pinned-claude-opus-4-6` -> `claude-opus-4.6`
- `pinned-claude-sonnet-4-6` -> `claude-sonnet-4.6`
- `pinned-gpt-5-5` -> `gpt-5.5`
- `pinned-gpt-5-4` -> `gpt-5.4`
- `pinned-gemini-3-1-pro-preview` -> `gemini-3.1-pro-preview`
- `pinned-gemini-3-pro-preview` -> `gemini-3-pro-preview`

Execution rules:

- Prefer the mapped pinned agent when it exists.
- If the runtime model name is hidden, use the pinned agent file's `model:` field.
- Current-model substitution does not count as a successful pin.
- Stop a slot's fallback chain as soon as it returns a usable review report.
- Exclude default-selected slots that collapse to the current family or another already-counted family, even at a stronger tier. Do not apply this exclusion to slots that were explicitly named by the user.
- Treat `SLOT_UNAVAILABLE` as unavailable.

GPT fallback:

- Fill at most 1 GPT slot.
- Order: `pinned-gpt-5-5` or explicit `gpt-5.5` -> one softer/default retry if needed -> `pinned-gpt-5-4` or explicit `gpt-5.4`.
- Count only `gpt-5.4+`.
- If fallback supplied the slot, say which fallback was used.
- If no GPT fallback succeeds, report that no independent GPT participant could be obtained.

Claude fallback:

- Fill at most 1 Claude slot.
- Order: `pinned-claude-opus-4-7` -> one softer/default retry if needed -> `pinned-claude-opus-4-6` or explicit `claude-opus-4.6` -> `pinned-claude-sonnet-4-6` or explicit Sonnet fallback.
- Count only `claude-opus-4.6+` or `claude-sonnet-4.6+`.
- If fallback supplied the slot, say which fallback was used.
- If no Claude fallback succeeds, report that no independent Claude participant could be obtained.

Gemini fallback:

- Fill at most 1 Gemini slot.
- Order: preferred Gemini slot for the client -> one softer/default retry if needed -> the other Gemini slot or one explicit Gemini fallback.
- If fallback supplied the slot, say which fallback was used.
- If neither Gemini slot succeeds, report that no independent Gemini participant could be obtained.

## Review Rules

- Give every participant the same task, diff, constraints, diagnostics, and relevant local context.
- Every participant reviews the same candidate diff. Do not ask them to produce competing implementations.
- Classify findings as `confirmed bug or regression`, `high-confidence risk`, `non-blocking suggestion`, or `no issue found`.
- Prefer findings backed by code, diagnostics, tests, or repository conventions over speculation.
- Prioritize correctness, regressions, security, data integrity, contract mismatches, missing validation, broken tests, concurrency problems, resource handling, and error-path gaps.
- Ignore stylistic nits, speculative refactors, and unrelated pre-existing issues unless the user explicitly asks for broader cleanup.

## Fix Application Rules

- Only the current agent edits real repository files.
- Apply only consensus-backed or strongly evidenced findings that are safe to correct surgically.
- Prefer the smallest safe fix that preserves the user's intended change.
- Do not overwrite unrelated user edits or expand scope into cleanup.
- Ask before architecture, schema, dependency, public API, or other wide-impact changes.
- After applying fixes, review the resulting diff in context.
- Allow at most 2 review-and-fix rounds. Stop early if no new technical evidence appears.

## Workflow

1. Restate the task, constraints, review base, and whether the run is `2-agent` or `3-agent`.
2. Make the requested change with the current agent only, or inspect the existing candidate diff if one already exists.
3. Determine the exact review scope from the real diff and collect the minimum context, diagnostics, and useful validation commands.
4. Resolve the current runtime model and finalize the participant set.
5. Print `Models in use:` with model names only.
6. Print `Pinned agents used:` separately when pinned custom agents participate.
7. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
8. Produce the current-agent self-review first, then one review report per non-current slot on the same diff.
9. Compare findings in the current agent only. Prefer code-backed issues over stylistic preference.
10. Apply only safe agreed fixes. If a finding requires broader changes, stop and ask before proceeding.
11. Run the narrowest useful validation available and review the resulting diff.
12. If new material hunks were introduced, run at most 1 additional review round on those new hunks only.
13. Present the final result when the participants align; otherwise choose the safer, more repository-consistent fix set and note any unresolved disagreement.

## Output Rules

- State the requested and achieved participant count. For default selection, also state independent family count if it differs.
- State the reviewed scope briefly.
- Under `Models in use:`, list model names only.
- If a pinned participant does not expose its runtime model, use the pinned agent's `model:` value.
- Report custom agent names separately from model names.
- Do not list collapsed slots or fallback attempts as separate participants.
- For `2-agent`, report exactly `Current AI model` plus 1 non-current participant.
- If fewer than 2 usable participants remain, explicitly say that multi-agent review could not be fully completed.
- If `3-agent` was requested but only 2 usable participants remain, explicitly say that the run degraded to `2-agent`.
- Exclude any Claude slot that resolves to `claude-sonnet-4.5` or lower.
- Clearly separate applied fixes from findings intentionally left unchanged.
- Report what validation ran and any residual risk that still matters.
- Keep the final answer concise and action-oriented.
