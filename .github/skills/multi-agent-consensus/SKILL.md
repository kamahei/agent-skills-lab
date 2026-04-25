---
name: multi-agent-consensus
description: Run `/multi-agent-consensus` for bounded 2-agent or 3-agent independent reasoning. Activate only on the exact command.
---

# Multi Agent Consensus

## Activation

- Activate only on the exact `/multi-agent-consensus` command.
- Default to `2-agent`.
- Keep a fixed participant set: the current agent plus the selected non-current slots only. Do not add helper, review, explore, or code-review agents.
- Count only distinct model families.

## Participant Selection

Allowed baselines:

- Claude: prefer `claude-opus-4.7`, then `claude-opus-4.6`, then `claude-sonnet-4.6+`
- GPT: prefer `gpt-5.5`, fallback `gpt-5.4+`
- Gemini: prefer `gemini-3.1-pro-preview`; portable fallback `gemini-3-pro-preview`
- `Current AI model`

Default sets:

- `2-agent`: `Current AI model` + `claude-opus-4.7`
- `3-agent`: `Current AI model` + `claude-opus-4.7` + `gpt-5.5`

Family-aware defaults:

- If the current model is Claude, use GPT for `2-agent`, and GPT + Gemini for `3-agent`.
- If the current model is GPT or Gemini, use the Claude fallback chain above for the single Claude slot.

Selection rules:

- `Current AI model` always occupies one slot. Non-current slots: 1 in `2-agent`, 2 in `3-agent`.
- Resolve the current runtime model before finalizing the set.
- Families must be distinct. Never count another slot from the current family, even at a different tier.
- If a slot conflicts by family, keep `Current AI model` and replace the conflicting slot. Use replacement priority `GPT -> Gemini -> Claude`.
- If the user explicitly names 2 or 3 models, honor that set after the same family check. If independence still fails, fall back to the defaults.
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
- Stop a slot's fallback chain as soon as it returns a usable independent proposal.
- Exclude slots that collapse to the current family or another already-counted family, even at a stronger tier.
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

## Workflow

1. Restate the task, constraints, and decision that needs higher confidence.
2. Resolve the current runtime model and finalize the independent participant set.
3. Print `Models in use:` with model names only.
4. Print `Pinned agents used:` separately when pinned custom agents participate.
5. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
6. Produce the current-agent proposal first, then one proposal per non-current slot.
7. Compare proposals in the current agent only.
8. Run at most 2 refinement rounds and stop early if no new technical evidence appears.
9. Present the consensus answer when the participants align; otherwise choose the safer, more repository-consistent option.

## Output Rules

- State the requested and achieved independent count.
- Under `Models in use:`, list model names only.
- If a pinned participant does not expose its runtime model, use the pinned agent's `model:` value.
- Report custom agent names separately from model names.
- Do not list collapsed slots or fallback attempts as separate participants.
- For `2-agent`, report exactly `Current AI model` plus 1 non-current participant.
- If fewer than 2 independent participants remain, explicitly say that multi-agent consensus could not be fully completed.
- If `3-agent` was requested but only 2 independent participants remain, explicitly say that the run degraded to `2-agent`.
- Exclude any Claude slot that resolves to `claude-sonnet-4.5` or lower.
- If a requested high-effort setting was softened for availability, call that out briefly.
- Keep the final answer concise and action-oriented.
