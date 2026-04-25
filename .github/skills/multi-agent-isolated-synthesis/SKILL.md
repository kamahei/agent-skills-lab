---
name: multi-agent-isolated-synthesis
description: Run `/multi-agent-isolated-synthesis` so 2 or 3 agents solve the same task in isolated workspaces, cross-review the results, synthesize the best final artifact, and apply only that final artifact.
---

# Multi Agent Isolated Synthesis

## Activation

- Activate only on the exact `/multi-agent-isolated-synthesis` command.
- Honor an explicit `2-agent` or `3-agent` request. Default to `3-agent`; for default selection, degrade to `2-agent` only when an independent participant cannot be obtained.
- Default mode is `same task, same instruction packet, independent execution`. Split into different subtasks only when the user explicitly asks for decomposition.
- Keep a fixed participant set: the current agent plus the selected non-current slots only. Do not add helper, review, merge, explore, or code-review agents.
- Keep the original repository read-only until the final apply step, aside from normal reads and validation.

## Inputs And Scope

- Expected context: a task that benefits from multiple independent executions, peer review, and synthesis.
- Required input: the user's task. If it is implicit in history, restate it explicitly before dispatch.
- Optional inputs: target files or directories, constraints, acceptance criteria, diagnostics, failing tests, artifact format, explicit model selection, agent count, and whether logs should be preserved.
- Suitable tasks include code changes, refactors, bug fixes, docs, tests, reviews, plans, prompts, and other tasks where same-task parallel execution improves quality.

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
- Once finalized, use only that participant set for the run.
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
- Each pinned participant works only inside its own isolated workspace until the review phase.
- Stop a slot's fallback chain as soon as it returns a usable candidate.
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

## Workspace Isolation

- Create one disposable workspace per agent under a project-local ignored temp directory or the system temp directory.
- Prefer paths such as `<temp>/multi-agent-isolated-synthesis/<timestamp>/<agent-id>/`.
- Copy only the files needed for the task, preserving relative paths, or use an equivalent disposable worktree when supported.
- Do not edit original files during execution, review, or synthesis.
- Track which original files each workspace mirrors, and clean up temporary workspaces unless the user asks to keep them.

## Task Packet And Artifacts

- Every participant receives the same task packet before any peer output is visible.
- The packet should include: the full task or faithful restatement, numbered acceptance criteria, shared constraints, relevant files or excerpts, repository instructions and diagnostics, isolated workspace root, expected artifact format, validation expectations, and an explicit instruction to read files and run validation inside the workspace.
- For file-edit tasks, include the exact phrase `This workspace is isolated and disposable.`.
- Do not reduce the task to a one-line summary, send different baseline context to different agents, expose peer artifacts during the initial pass, or omit acceptance criteria or artifact expectations.
- Default code artifact: modified files or patches with target paths, brief rationale, and validation performed.
- Default non-code artifact: structured Markdown with evidence, trade-offs, risks, and open questions as needed.
- If an artifact is partial or format-mismatched, salvage only the relevant content and note the mismatch.

## Workflow

1. Restate the task and constraints, convert success criteria into numbered acceptance criteria, and state whether the run is `2-agent` or `3-agent`.
2. Resolve the participant set before any agent work begins.
3. Print `Models in use:` with model names only.
4. Print `Pinned agents used:` separately when pinned custom agents participate.
5. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
6. Prepare one isolated workspace per agent.
7. Build one shared task packet and dispatch it to every agent before any peer output is visible.
8. Have each agent execute the same task independently, self-check, and return explicit artifacts.
9. Dispatch cross-review by sending each candidate's artifacts to every other agent together with the original task packet. In `3-agent` mode, full cross-review means 6 review passes; if that is impractical, say so and use the best bounded fallback you can support.
10. Collect structured review reports and distinguish `confirmed strength`, `confirmed flaw`, `suspected risk`, and `stylistic preference`.
11. Select the strongest whole candidate when one clearly wins. Otherwise synthesize the best-supported parts in a fresh synthesis workspace.
12. Send the selected or synthesized result back to all agents for final approval or evidence-backed objections. Silence is not approval.
13. Refine until objections are resolved or no new technical evidence appears. Allow at most 2 refinement rounds unless the user explicitly asks for more.
14. Validate the final result as far as the task allows.
15. Apply only the final agreed result to the real target files or final answer.

## Evaluation, Synthesis, And Failure Handling

- Prefer confirmed correctness and constraint satisfaction over style.
- Prefer the smallest safe solution and penalize unnecessary scope, risky side effects, or weak justification.
- If two candidates are close, prefer the one that is easier to validate and maintain.
- When combining candidates, use a dedicated synthesis workspace rather than the real repository.
- Do not force incompatible approaches into a code-level merge. Choose the stronger approach first, then adopt only clearly compatible improvements.
- If different candidates change the same area incompatibly, prefer the version with stronger review support; if support is close, prefer the one closer to repository conventions and easier validation.
- If a merge would require broader architecture, schema, dependency, API, or workflow changes than requested, stop and ask.
- If a sub-agent returns a partial result, keep any still-useful part and note the gap.
- If a sub-agent returns empty, off-topic, or unusable output, exclude it and record why.
- If a sub-agent errors or times out, treat it as an unavailable slot and apply the same degradation rules.
- If all non-current agents fail, complete the task as a single-agent run and state that isolated synthesis could not be completed.

## Validation And Logging

- For code or file tasks, run the narrowest useful validation available.
- For review, planning, or analysis tasks, validate against stated constraints, source material, and internal consistency.
- Review the final diff or final artifact before applying it.
- For file tasks, apply the reviewed contents or patch from the selected final workspace rather than recreating the change from memory.
- If the user asks for logs, create a Markdown log containing the task packet, workspaces, produced artifacts, evaluation, selection rationale, final result, and validation summary.
- Unless the user asks for a repository path, write logs to a temporary output path and report that path in the final response.

## Output Rules

- State the requested and achieved agent count.
- Under `Models in use:`, list model names only.
- If a pinned participant does not expose its runtime model, use the pinned agent's `model:` value.
- Report custom agent names separately from model names.
- Do not list collapsed slots or fallback attempts as separate participants.
- For `2-agent`, report exactly `Current AI model` plus 1 non-current participant.
- State whether all participants received the same task packet and whether the final result used whole-candidate selection or synthesized selection.
- Mention any degradation, such as `3-agent` requested but `2-agent` achieved.
- If fewer than 2 usable participants remain, explicitly say that isolated synthesis could not be fully completed.
- If `3-agent` was requested but only 2 usable participants remain, explicitly say that the run degraded to `2-agent`.
- Exclude any Claude slot that resolves to `claude-sonnet-4.5` or lower.
- If a requested high-effort setting was softened for availability, call that out briefly.
- Apply only the final agreed artifact to the real target.
- When a log file is created, report its final path.
- Keep the final response concise and action-oriented, but mention validation and any unresolved risk.
