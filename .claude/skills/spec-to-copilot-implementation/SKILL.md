---
name: spec-to-copilot-implementation
description: Prepare a one-shot GitHub Copilot implementation pack from Claude Code. Use when the user wants Claude to do the design, specification, scope control, and implementation briefing first, then let GitHub Copilot perform the actual code changes in a single premium request.
---

# Spec To Copilot Implementation

## Activation

- Use this wrapper when Claude Code should front-load the design and planning work, then hand the actual implementation to GitHub Copilot.
- Treat `$ARGUMENTS` as the requested change, constraints, and desired one-shot behavior.
- Default to creating the handoff pack first and stopping there unless the user also wants Claude to invoke Copilot.

## Workflow

1. Read `../../../.agents/skills/spec-to-copilot-implementation/SKILL.md`.
2. Decide whether the task is `green`, `yellow`, `red-too-small`, or `red-too-risky` under the shared skill's handoff ROI and specifiability rules.
3. If the task is `red-too-small`, keep the work in Claude instead of handing it to Copilot.
4. If the task is `red-too-risky`, stop and report the recommended split instead of forcing a one-shot run.
5. Inspect only the local repository context needed to make the implementation concrete.
6. If the task is `yellow`, tighten the file boundaries, assumptions, non-goals, and acceptance criteria before generating the handoff.
7. Create the minimum handoff docs described by the shared skill.
8. Generate the final dense Copilot prompt.
9. If the user explicitly wants execution and Copilot is available, run Copilot once with that final prompt.
10. If Copilot ran, review the resulting diff and validation output in Claude before accepting the result.
11. If Copilot missed scope or wandered, follow the shared retry rules instead of broadening the prompt blindly.

## Usage Examples

- Ask Claude to inspect a multi-file auth flow and prepare one premium-request handoff:
  `/spec-to-copilot-implementation inspect the app router auth flow, API handlers, Prisma user model, session checks, and auth tests, then write the implementation spec and one final GitHub Copilot prompt`
- Ask Claude to tighten a larger dashboard feature before handing it to Copilot:
  `/spec-to-copilot-implementation analyze the analytics dashboard modules, API client, export flow, and tests, define the bounded scope for persisted filters and CSV export, and optimize the handoff for a single GitHub Copilot request`
- Ask Claude to execute the handoff too when the Copilot CLI is available:
  `/spec-to-copilot-implementation plan a bounded multi-file refactor for the settings area, fix the target files and acceptance criteria first, then generate the one-shot prompt and run GitHub Copilot once`

## Output Rules

- State whether the request was `green`, `yellow`, `red-too-small`, or `red-too-risky`.
- State whether Claude stopped at the handoff pack or continued to a Copilot run.
- If Copilot ran, state that Claude reviewed the resulting diff and validation output.
- List the created handoff files and the final prompt file.
