---
name: multi-agent-consensus
description: Run an on-demand 2-agent or 3-agent reasoning and review workflow with bounded refinement and explicit stop conditions. Use only when the user explicitly asks for `use 2-agents-consensus`, `use 3-agents-consensus`, multi-agent mode, consensus, or a second-opinion review on a plan, implementation, architecture tradeoff, or code review.
---

# Multi Agent Consensus

## Activation

- Activate only on an explicit user request for `use 2-agents-consensus`, `use 3-agents-consensus`, multi-agent mode, consensus, or a second opinion.
- Default to 2 agents when the user does not specify a count.
- Keep the participant set fixed for the run: the current agent plus the selected non-current slots only.
- Do not add helper, review, explore, or code-review agents outside that set.
- Count only genuinely independent model families. A slot that resolves to an already-participating family does not satisfy the requested count.

## Participant Selection

Allowed baselines:

- `claude-opus-4.6` or a higher Claude Opus version
- `gpt-5.4` or a higher GPT version
- `gemini-3.1-pro-preview` or a higher Gemini 3.1 version
- `gemini-3-pro-preview` or a higher Gemini preview fallback
- `Current AI model`

Default sets:

- 2-agent: `claude-opus-4.6` + `Current AI model`
- 3-agent: `claude-opus-4.6` + `gpt-5.4` + `Current AI model`

Selection rules:

- Resolve `Current AI model` to its actual runtime model before finalizing the set.
- Keep model families distinct, not just model names distinct.
- If `Current AI model` conflicts by family with a non-current slot, keep `Current AI model` and replace the conflicting slot.
- Use this replacement priority: Claude Opus, GPT, Gemini.
- If the user explicitly names 2 or 3 allowed models, use that set after applying the same family rule.
- If the explicit set still cannot satisfy the requested independent count, fall back to the default set.
- Use `gemini-3-pro-preview` as the portable Gemini baseline.
- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, prefer `consensus-gemini-3-1-pro-preview` before `consensus-gemini-3-pro-preview`.
- In Copilot CLI or when client support is unclear, prefer `consensus-gemini-3-pro-preview` before `consensus-gemini-3-1-pro-preview`.

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

- `consensus-claude-opus-4-6` -> `claude-opus-4.6`
- `consensus-claude-sonnet-4-6` -> `claude-sonnet-4.6`
- `consensus-gpt-5-4` -> `gpt-5.4`
- `consensus-gemini-3-1-pro-preview` -> `gemini-3.1-pro-preview`
- `consensus-gemini-3-pro-preview` -> `gemini-3-pro-preview`

Execution rules:

- Prefer the mapped pinned agent when it exists.
- Treat the mapped agent file's `model:` field as the source of truth when the runtime model name is not exposed.
- Do not treat current-model substitution as a successful pin.
- If a pinned slot returns a usable independent proposal, do not run another fallback for that slot.
- Use best-effort fallback only when the mapped agent is missing, unavailable, errors, or returns no usable independent proposal.
- Exclude any slot that resolves to the current model family or another already-counted family.
- Treat `SLOT_UNAVAILABLE` as unavailable, not as a proposal.

Claude-specific fallback:

- Try `consensus-claude-opus-4-6` first.
- If the Claude attempt returns `SLOT_UNAVAILABLE`, the current model family, any non-Claude family, or any explicit Claude runtime below 4.6, retry once with a softer or default Claude request.
- If the Claude slot still cannot produce an independent Claude-family participant, try `consensus-claude-sonnet-4-6` or an explicit Claude Sonnet fallback once.
- Count a Claude fallback only when it is `claude-sonnet-4.6` or higher.
- If `consensus-claude-opus-4-6` is unavailable but `consensus-claude-sonnet-4-6` succeeds at version 4.6 or higher, count `consensus-claude-sonnet-4-6` as the Claude participant and say that `consensus-claude-opus-4-6` was unavailable and `consensus-claude-sonnet-4-6` fallback was used.
- If both `consensus-claude-opus-4-6` and `consensus-claude-sonnet-4-6` fail, report that no independent Claude participant could be obtained.

Gemini-specific fallback:

- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, try `consensus-gemini-3-1-pro-preview` first.
- In Copilot CLI or when client support is unclear, try `consensus-gemini-3-pro-preview` first.
- If the first Gemini attempt returns `SLOT_UNAVAILABLE`, the current model family, or any non-Gemini family, retry once with a softer or default Gemini request.
- If the first Gemini slot still cannot produce an independent Gemini-family participant, try the other Gemini preview slot or one explicit Gemini fallback once.
- If the first Gemini slot is unavailable but the other Gemini slot succeeds, count the successful Gemini slot as the Gemini participant and say which Gemini fallback was used.
- If both `consensus-gemini-3-1-pro-preview` and `consensus-gemini-3-pro-preview` fail, report that no independent Gemini participant could be obtained.

## Workflow

1. Restate the task, constraints, and decision that needs higher confidence.
2. Resolve the current runtime model and finalize the independent participant set.
3. Print `Models in use:` with model names only.
4. Print `Pinned agents used:` separately when pinned custom agents participate.
5. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
6. Produce the current-agent proposal first, then one proposal per non-current slot.
7. Compare proposals in the current agent only.
8. Run at most 2 refinement rounds and stop early if no new technical evidence appears.
9. Present the consensus answer when participating agents align; otherwise choose the safer, more repository-consistent option.

## Output Rules

- State the requested consensus count and the achieved independent count.
- List only model names under `Models in use:`.
- If a pinned participant does not expose its runtime model, use the pinned agent's configured `model:` value as the model name.
- Report custom agent names separately from model names.
- Do not list collapsed or mismatched slots as independent participants.
- If fewer than 2 independent participants remain, explicitly say that multi-agent consensus could not be fully completed.
- If a requested 3-agent run ends with only 2 independent participants, explicitly say that it degraded to a 2-agent run.
- If a Claude slot resolves to `claude-sonnet-4.5` or any lower Claude version, explicitly exclude it from the participant count.
- If a requested high-effort setting was softened for availability, call that out briefly.
- Keep the final answer concise and action-oriented.

## Suggested Prompts

- `Use 2-agents-consensus for this task.`
- `Use 3-agents-consensus for this task.`
- `Use 3-agents-consensus with claude-opus-4.6, gemini-3-pro-preview, and current AI model.`
