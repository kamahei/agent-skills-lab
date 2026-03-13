---
name: multi-agent-isolated-synthesis
description: Run the `/multi-agent-isolated-synthesis` workflow where 2 or 3 agents independently tackle the same task in separate temporary workspaces, compare results, synthesize the best parts, reach final consensus, and apply only the agreed final artifact. Use only when the user explicitly invokes `/multi-agent-isolated-synthesis`. Do not use for generic mentions of isolated multi-agent execution, best-of-N implementations, or compare-and-merge workflows without that exact skill invocation.
---

# Multi Agent Isolated Synthesis

## Activation

- Activate only when the user explicitly invokes `/multi-agent-isolated-synthesis`.
- Do not activate for generic requests about isolated multi-agent execution, parallel candidate generation, best-of-N selection, or compare-and-merge unless `/multi-agent-isolated-synthesis` is explicitly specified.
- Honor an explicit user request for `2-agent` or `3-agent` mode.
- Default to 3 agents. Degrade to 2 only when tooling, runtime, or scope limits prevent 3 materially independent candidates.
- Treat the default mode as `same task, independent candidates`. Split work into different subtasks only when the user explicitly asks for decomposition instead of alternative solutions.
- Keep the participant set fixed for the run: the current agent plus the selected non-current slots only.
- Do not add helper, review, explore, merge, or code-review agents outside that set.
- Keep the original repository read-only until the final apply step, except for normal read access and validation commands.

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

- If the user does not specify agent models, use the default set for the requested agent count.
- Resolve `Current AI model` to its actual runtime model before finalizing the set.
- Keep model families distinct, not just model names distinct.
- If `Current AI model` conflicts by family with a non-current slot, keep `Current AI model` and replace the conflicting slot.
- Use this replacement priority: Claude Opus, GPT, Gemini.
- If the user explicitly names 2 or 3 allowed models, use that set after applying the same family rule.
- Once the participant set is finalized, use only that set for the run and do not introduce any additional model outside it.
- If the explicit set still cannot satisfy the requested independent count, fall back to the default set.
- Use `gemini-3-pro-preview` as the portable Gemini baseline.
- In VS Code or when the client already exposes `gemini-3.1-pro-preview`, prefer `gemini-3.1-pro-preview` before `gemini-3-pro-preview`.
- In Copilot CLI or when client support is unclear, prefer `gemini-3-pro-preview` before `gemini-3.1-pro-preview`.

## Supported Task Types

- Use for code changes, file creation, refactors, bug fixes, documentation, test design, code review, incident analysis, implementation plans, architecture options, prompts, or other tasks where multiple independent candidates improve quality.
- For non-file tasks, replace file outputs with per-agent scratch artifacts such as notes, patches, plans, review reports, decision memos, or draft responses.

## Workspace Isolation

- Create one disposable workspace per agent under a project-local ignored temporary directory or the system temporary directory.
- Prefer paths that clearly identify the run and agent, such as `<temp>/multi-agent-isolated-synthesis/<timestamp>/<agent-id>/`.
- Copy only the files needed for the task while preserving relative paths, or create an equivalent disposable worktree when the environment supports it without touching the active worktree.
- Never edit the original files directly during agent execution, peer review, or synthesis.
- Track which original files each workspace mirrors so the final apply step is traceable.
- Clean up temporary workspaces after completion unless the user asks to keep artifacts or logs.

## Workflow

1. Restate the task, constraints, success criteria, and whether the run is `2-agent` or `3-agent`.
2. Resolve the participant set from the user request or the default set before any agent work begins.
3. Prepare one isolated workspace per agent and give every agent the same baseline context, constraints, and acceptance criteria.
4. Have each agent produce its own candidate result independently before seeing any peer result.
5. Capture each candidate as explicit artifacts: patches, files, plans, reports, or decision notes.
6. Run peer review across all candidates. Each agent reviews every candidate, focusing on correctness, constraint fit, safety, completeness, repository consistency, and validation readiness.
7. Select the strongest whole candidate when one clearly dominates. Otherwise extract the best parts from multiple candidates and build a synthesized result in a fresh synthesis workspace.
8. Review the synthesized result with all agents and require explicit agreement or concrete objections tied to evidence.
9. Refine the synthesized result until objections are resolved or no new technical evidence appears.
10. Validate the final result as far as the task allows.
11. Apply only the final agreed result to the real target files or final answer.

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
- If a merge would require broad architectural, schema, dependency, API, or workflow changes beyond the user request, stop and ask before applying that direction.

## Consensus And Stop Conditions

- Aim for unanimous approval of the final result.
- Allow at most 2 synthesis refinement rounds after the initial peer review unless the user explicitly asks for deeper iteration.
- Stop early when all agents agree or when further rounds add no new technical evidence.
- If full agreement is impossible, choose the safest high-confidence result and clearly note the remaining disagreement.

## Validation

- For file or code tasks, run the narrowest useful validation available, such as tests, lint, typecheck, build, or diff review.
- For review, planning, or analysis tasks, validate against the stated constraints, source material, and internal consistency.
- Before final apply, review the actual final diff or final artifact rather than relying on intermediate notes alone.
- For file tasks, apply the reviewed contents or patch from the selected final workspace rather than recreating the change from memory.

## Logging

- When the user asks for logs, create a log file that includes:
  - the task given to each agent
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
- State whether the run used whole-candidate selection or synthesized selection.
- Mention any degradation, such as `3-agent` requested but `2-agent` achieved.
- Apply only the final agreed artifact to the real target.
- When a log file is created, report its final path.
- Do not expose temporary draft files as final deliverables unless the user explicitly asks for them.
- Keep the final response concise and action-oriented, but mention validation and any unresolved risk.

## Suggested Prompts

- `/multi-agent-isolated-synthesis implement this change with isolated temporary workspaces`
- `/multi-agent-isolated-synthesis compare 3 independent solutions and merge the best parts`
- `/multi-agent-isolated-synthesis review these options independently, then pick the safest final plan`
- `/multi-agent-isolated-synthesis make the change, keep the repository untouched until the final apply step, and emit a task log`
