---
name: multi-agent-isolated-synthesis
description: Run the `/multi-agent-isolated-synthesis` workflow where 2 or 3 agents execute the same task in separate temporary workspaces, review one another's results, synthesize the best parts, reach final consensus, and apply only the agreed final artifact. Use only when the user explicitly invokes `/multi-agent-isolated-synthesis`. Do not use for generic mentions of isolated multi-agent execution, best-of-N implementations, or compare-and-merge workflows without that exact skill invocation.
---

# Multi Agent Isolated Synthesis

## Activation

- Activate only when the user explicitly invokes `/multi-agent-isolated-synthesis`.
- Do not activate for generic requests about isolated multi-agent execution, parallel candidate generation, best-of-N selection, or compare-and-merge unless `/multi-agent-isolated-synthesis` is explicitly specified.
- Honor an explicit user request for `2-agent` or `3-agent` mode.
- Default to 3 agents. Degrade to 2 only when tooling, runtime, or scope limits prevent 3 materially independent candidates.
- Treat the default mode as `same task, same instruction packet, independent execution`. Split work into different subtasks only when the user explicitly asks for decomposition instead of alternative solutions.
- Keep the participant set fixed for the run: the current agent plus the selected non-current slots only.
- Do not add helper, review, explore, merge, or code-review agents outside that set.
- Keep the original repository read-only until the final apply step, except for normal read access and validation commands.

## Inputs

- Expected context: a repository with a task that benefits from multiple independent executions followed by peer review and synthesis.
- Required: the user's task statement. When the task is implicit from conversation history, restate it explicitly before dispatching sub-agents.
- Optional inputs: target files or directories, constraints, acceptance criteria, diagnostics, failing tests, preferred artifact format, explicit model selection, agent count, and whether logs should be preserved.

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
  - If `Current AI model` is GPT family, fill the single 2-agent non-current slot with `claude-opus-4.6`; fall back to `claude-sonnet-4.6+` only per the Claude-specific fallback rules below.
  - If `Current AI model` is Gemini family, fill the single 2-agent non-current slot with `claude-opus-4.6`; fall back to `claude-sonnet-4.6+` only per the Claude-specific fallback rules below.

Selection rules:

- If the user does not specify agent models, use the default set for the requested agent count.
- `Current AI model` always occupies exactly one participant slot. The remaining slots are non-current: exactly 1 in `2-agent` mode and exactly 2 in `3-agent` mode.
- For a requested `2-agent` run, do not replace `Current AI model` with an additional non-current participant, and do not treat 2 non-current participants as satisfying the request.
- Resolve `Current AI model` to its actual runtime model before finalizing the set.
- Keep model families distinct, not just model names distinct.
- A non-current participant in the same family as `Current AI model` is never allowed, even if it is a different model tier (for example, Sonnet vs Opus).
- If `Current AI model` conflicts by family with a non-current slot, keep `Current AI model` and replace the conflicting slot.
- Use this replacement priority among non-conflicting families: GPT, Gemini, Claude.
- If the user explicitly names 2 or 3 allowed models, use that set after applying the same family rule.
- Once the participant set is finalized, use only that set for the run and do not introduce any additional model outside it.
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

## Supported Task Types

- Use for code changes, file creation, refactors, bug fixes, documentation, test design, code review, incident analysis, implementation plans, architecture options, prompts, or other tasks where same-task parallel execution plus peer review and synthesis improve quality.
- For non-file tasks, replace file outputs with per-agent scratch artifacts such as notes, patches, plans, review reports, decision memos, or draft responses.

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
- Each pinned participant must work only inside its own isolated workspace and must not see peer artifacts until the peer-review stage.
- If a pinned slot returns a usable independent candidate, do not run another fallback for that slot.
- Use best-effort fallback only when the mapped agent is missing, unavailable, errors, or returns no usable independent candidate.
- Exclude any slot that resolves to the current model family or another already-counted family.
- This exclusion applies even when the slot appears stronger by tier within that family (for example, do not select `claude-opus-4.6` when `Current AI model` is `claude-sonnet-4.6`).
- Treat `SLOT_UNAVAILABLE` as unavailable, not as a candidate.

Claude-specific fallback:

- Fill at most 1 Claude slot per run. Stop the Claude fallback chain as soon as any Claude model returns a usable independent artifact.
- Try `pinned-claude-opus-4-6` first.
- If the Claude attempt returns `SLOT_UNAVAILABLE`, the current model family, any non-Claude family, or any explicit Claude runtime below 4.6, retry once with a softer or default Claude request.
- If the Claude slot still cannot produce an independent Claude-family participant, try `pinned-claude-sonnet-4-6` or an explicit Claude Sonnet fallback once.
- Count a Claude fallback only when it is `claude-sonnet-4.6` or higher.
- If `pinned-claude-opus-4-6` is unavailable but `pinned-claude-sonnet-4-6` succeeds at version 4.6 or higher, count `pinned-claude-sonnet-4-6` as the Claude participant and say that `pinned-claude-opus-4-6` was unavailable and `pinned-claude-sonnet-4-6` fallback was used.
- If both `pinned-claude-opus-4-6` and `pinned-claude-sonnet-4-6` fail, report that no independent Claude participant could be obtained.

Gemini-specific fallback:

- Fill at most 1 Gemini slot per run. Stop the Gemini fallback chain as soon as any Gemini model returns a usable independent artifact.
- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, try `pinned-gemini-3-1-pro-preview` first.
- In Copilot CLI or when client support is unclear, try `pinned-gemini-3-pro-preview` first.
- If the first Gemini attempt returns `SLOT_UNAVAILABLE`, the current model family, or any non-Gemini family, retry once with a softer or default Gemini request.
- If the first Gemini slot still cannot produce an independent Gemini-family participant, try the other Gemini preview slot or one explicit Gemini fallback once.
- If the first Gemini slot is unavailable but the other Gemini slot succeeds, count the successful Gemini slot as the Gemini participant and say which Gemini fallback was used.
- If both `pinned-gemini-3-1-pro-preview` and `pinned-gemini-3-pro-preview` fail, report that no independent Gemini participant could be obtained.

## Workspace Isolation

- Create one disposable workspace per agent under a project-local ignored temporary directory or the system temporary directory.
- Prefer paths that clearly identify the run and agent, such as `<temp>/multi-agent-isolated-synthesis/<timestamp>/<agent-id>/`.
- Copy only the files needed for the task while preserving relative paths, or create an equivalent disposable worktree when the environment supports it without touching the active worktree.
- Never edit the original files directly during agent execution, peer review, or synthesis.
- Track which original files each workspace mirrors so the final apply step is traceable.
- Clean up temporary workspaces after completion unless the user asks to keep artifacts or logs.

## Sub-Agent Prompt Construction

The prompt sent to each sub-agent is the main quality lever. Do not reduce the task to a lossy summary when the goal is to match top-level agent quality.

Mandatory prompt contents:

1. The full user task statement or a faithful orchestrator restatement when the task must be clarified.
2. A numbered list of concrete acceptance criteria derived from the task.
3. The same scope limits, constraints, and "do not" rules for every agent.
4. The relevant file contents or file excerpts with enough surrounding context to start strong. If the files are too large to include in full, include the most relevant sections and explicitly instruct the sub-agent to read the remaining files from its workspace.
5. Relevant repository conventions, instruction files, diagnostics, failing tests, or logs that materially affect the task.
6. The isolated workspace root path. For file-edit tasks, include the exact phrase `This workspace is isolated and disposable.`.
7. The expected artifact format and validation expectations.
8. An explicit instruction to read files and run available validation commands in the workspace rather than relying only on the prompt.

Prompt anti-patterns to avoid:

- Do not paraphrase the task into a one-line summary and expect top-level quality.
- Do not send different baseline context to different agents unless the user explicitly asks for decomposed subtasks.
- Do not expose peer artifacts during the initial execution phase.
- Do not omit acceptance criteria or artifact expectations.

## Artifact Format Contract

Specify the expected output format in every sub-agent prompt. Use these defaults when the user does not specify one:

- Code changes: complete modified files labeled with target paths, plus a brief rationale and the validation performed.
- Bug fixes and refactors: modified files or patches plus a concise explanation of the chosen approach and any residual risk.
- Plans, designs, and analyses: structured Markdown with sections for summary, proposal, trade-offs, risks, and open questions.
- Reviews: structured findings classified as `confirmed issue`, `high-confidence risk`, `suggestion`, or `no issue found`, each with evidence.
- Tests: complete test files plus the command used to validate them.

If a sub-agent returns a partial or format-mismatched artifact, extract the usable content only when it is still relevant and flag the mismatch during evaluation.

## Workflow

1. Restate the task and constraints. Convert the success criteria into a numbered list of concrete, independently checkable acceptance criteria. State whether the run is `2-agent` or `3-agent`.
2. Resolve the participant set from the user request or the default set before any agent work begins.
3. Print `Models in use:` with model names only.
4. Print `Pinned agents used:` separately when pinned custom agents participate.
5. Print `Requested settings:` only when the user explicitly asks for model or reasoning transparency.
6. Prepare one isolated workspace per agent.
7. Build one shared task packet from the current AI's task instruction, acceptance criteria, constraints, relevant files, diagnostics, and expected artifact format. Dispatch that same packet to every agent before any peer output is visible.
8. Have each agent execute the same task independently in its own workspace, perform a self-check, and return explicit artifacts: files, patches, plans, reports, or decision notes.
9. Dispatch cross-review by sending each candidate's full artifacts to every other agent together with the original task packet. Require review of correctness, constraint fit, safety, completeness, repository consistency, mergeability, and validation readiness. In `3-agent` mode, acknowledge that full cross-review requires 6 review passes. If token or runtime limits make full cross-review impractical, say so explicitly and use the best bounded fallback you can support rather than claiming a full cross-review pass.
10. Collect structured review reports from all agents and the current agent. Distinguish `confirmed strength`, `confirmed flaw`, `suspected risk`, and `stylistic preference`.
11. Select the strongest whole candidate when one clearly dominates on confirmed strengths without confirmed flaws. Otherwise extract the best-supported parts from multiple candidates and build a synthesized result in a fresh synthesis workspace.
12. Send the selected or synthesized result back to all agents for final approval or evidence-backed objections. Silence is not approval.
13. Refine the selected or synthesized result until objections are resolved or no new technical evidence appears.
14. Validate the final result as far as the task allows.
15. Apply only the final agreed result to the real target files or final answer.

## Evaluation Rules

- Prefer confirmed correctness and constraint satisfaction over stylistic preference.
- Prefer the smallest safe change that solves the task.
- Penalize candidates that introduce unnecessary scope, risky side effects, or weak justification.
- When two candidates are close, prefer the one that is easier to validate and easier to maintain.
- Separate confirmed flaws from speculative concerns.
- Do not let an agent's preference for its own output outweigh the peer review evidence.

## Synthesis Rules

- If combining multiple candidates, create the merged result in a dedicated synthesis workspace rather than directly in the repository.
- Preserve traceability by noting which agent contributed each adopted part when that matters for review or logging.
- Re-run compatibility checks whenever mixed parts touch the same interface, file, or assumption.
- When candidates take structurally incompatible approaches, do not force a code-level merge. Choose the stronger approach first, then adopt only clearly compatible improvements from the others.
- When candidates modify the same lines differently, prefer the version with stronger review support. If review support is close, prefer the version closer to repository conventions and easier validation.
- When one candidate expands scope beyond the request and another satisfies the acceptance criteria narrowly, prefer the narrower safe candidate unless the added scope resolves a confirmed gap.
- If a merge would require broad architectural, schema, dependency, API, or workflow changes beyond the user request, stop and ask before applying that direction.

## Consensus And Stop Conditions

- Aim for unanimous approval of the final result.
- Allow at most 2 synthesis refinement rounds after the initial peer review unless the user explicitly asks for deeper iteration.
- Stop early when all agents agree or when further rounds add no new technical evidence.
- If full agreement is impossible, choose the safest high-confidence result and clearly note the remaining disagreement.

## Task-Level Failure Handling

- If a sub-agent returns a partial result that still covers some acceptance criteria, keep it in the evaluation pool and clearly note the gaps.
- If a sub-agent returns output that is empty, off-topic, or unusable, exclude it from the evaluation pool and record why.
- If a sub-agent errors out or times out, treat it as an unavailable slot and apply the same degradation rules used for slot unavailability.
- If all non-current agents fail at the task level, complete the task as a single-agent run and state clearly that isolated synthesis could not be completed.

## Validation

- For file or code tasks, run the narrowest useful validation available, such as tests, lint, typecheck, build, or diff review.
- For review, planning, or analysis tasks, validate against the stated constraints, source material, and internal consistency.
- Before final apply, review the actual final diff or final artifact rather than relying on intermediate notes alone.
- For file tasks, apply the reviewed contents or patch from the selected final workspace rather than recreating the change from memory.

## Logging

- When the user asks for logs, create a log file that includes:
  - the task packet given to each agent
  - the temporary workspace used by each agent
  - the artifacts produced by each agent
  - the evaluation of each candidate, including strengths, weaknesses, and rejection reasons when applicable
  - the basis for selecting one candidate or synthesizing multiple candidates
  - the final consensus result and validation summary
- Prefer a Markdown log such as `multi-agent-isolated-synthesis-log-<timestamp>.md`.
- Unless the user requests a repository path, write logs to a temporary output path and report that path in the final response.
- If the user wants logs preserved in the repository, ask for or use a clearly scoped output path and apply that log file only at the end with the final result.

## Output Rules

- State the requested and achieved agent count.
- List only model names under `Models in use:`.
- If a pinned participant does not expose its runtime model, use the pinned agent's configured `model:` value as the model name.
- Report custom agent names separately from model names.
- Do not list collapsed or mismatched slots as independent participants.
- For a requested `2-agent` run, report exactly `Current AI model` plus 1 non-current participant. Do not report both a primary attempt and its fallback as separate participants.
- State that all participants received the same task packet when the run followed the default same-task workflow.
- State whether the run used whole-candidate selection or synthesized selection.
- Mention any degradation, such as `3-agent` requested but `2-agent` achieved.
- If fewer than 2 independent participants remain, explicitly say that isolated synthesis could not be fully completed.
- If a requested `3-agent` run ends with only `2-agent` independence, explicitly say that it degraded to a `2-agent` run.
- If a Claude slot resolves to `claude-sonnet-4.5` or any lower Claude version, explicitly exclude it from the participant count.
- If a requested high-effort setting was softened for availability, call that out briefly.
- Apply only the final agreed artifact to the real target.
- When a log file is created, report its final path.
- Do not expose temporary draft files as final deliverables unless the user explicitly asks for them.
- Keep the final response concise and action-oriented, but mention validation and any unresolved risk.

## Suggested Prompts

- `/multi-agent-isolated-synthesis send this exact task to 2 agents in isolated workspaces, then have them review and merge the results`
- `/multi-agent-isolated-synthesis run the same implementation task in 3-agent mode, keep peer outputs hidden until review, then synthesize the best final artifact`
- `/multi-agent-isolated-synthesis give every agent the same task packet, make them cross-review the artifacts, and pick the safest merged result`
- `/multi-agent-isolated-synthesis make the change, keep the repository untouched until the final apply step, and emit a task log`
