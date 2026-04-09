# AGENTS.md

## Purpose Of This Repository

This repository is a workspace for creating, organizing, and reusing `AGENTS.md`, Skill files, and Agent-related files for tools such as GitHub Copilot, OpenAI Codex, Claude Code, and Gemini CLI. Prefer outputs that are reusable, portable, and practical in real projects.

## Core Rules

- The root `AGENTS.md` is the operating guide for this repository itself. Do not keep sample `AGENTS.md` files at the root.
- When a user asks to create an `AGENTS.md`, create it under `agent-samples/<Topic>/AGENTS.md` unless the request is clearly about this repository's own root rules.
- When a user asks to revise, improve, or fix an existing `AGENTS.md`, Skill, or Agent file, update the existing file in place unless the user explicitly asks for a new copy or variant.
- Place reusable, cross-AI assets under `.agents/`.
- Place AI-specific assets in the directory expected by that AI tool.
- Directory conventions and supported features can change. Verify the latest official documentation before introducing or expanding AI-specific folders.
- Handle vague requests proactively. If missing details would materially change the result, ask a short and concrete question. Otherwise, proceed with a sensible default.
- If the user says "leave it to you", use the latest official documentation, current tool behavior, and broadly accepted best practices to produce the best default result.
- Treat a user message that starts with `/skill-name` as an explicit request to use the matching skill when a matching folder exists under `.agents/skills/`, `.github/skills/`, or `.claude/skills/`, even if the current AI client does not provide a native slash-skill command.
- Unless explicitly instructed otherwise, create files in English.
- Use the user's language for chat replies, questions, and other conversational responses.

## Repository Layout

### Shared Assets

- `/.agents/`
  - Stores reusable assets that can work across multiple AI tools.
  - Typical examples: `/.agents/skills/`, `/.agents/agents/`, `/.agents/templates/`, `/.agents/references/`
  - Treat this as the primary shared source when possible. Only create AI-specific variants when a tool requires a different format or behavior.

### AI-Specific Assets

- `/.github/`
  - Stores GitHub Copilot-related assets.
  - Typical examples: `.github/copilot-instructions.md`, `.github/instructions/`, `.github/prompts/`, `.github/agents/`, `.github/skills/`
- `/.claude/`
  - Stores Claude Code-related assets.
  - Typical examples: `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, `.claude/settings.json`
  - If persistent repository instructions are needed for Claude Code, use `CLAUDE.md`.
- `/.gemini/`
  - Stores Gemini CLI-related assets.
  - Typical examples: `.gemini/commands/`, `.gemini/settings.json`, `.gemini/skills/`
  - If persistent repository instructions are needed for Gemini CLI, use `GEMINI.md`.
- `/`
  - Use `AGENTS.md` for Codex and vendor-neutral agent instructions.

## Output Placement Rules

### 1. Requests To Create An AGENTS.md

- By default, create `agent-samples/<Topic>/AGENTS.md`.
- Use a short, clear, and recognizable topic name for `<Topic>`.
- Prefer official or widely used naming where possible.
- Examples:
  - `agent-samples/UE5/AGENTS.md`
  - `agent-samples/Nextjs/AGENTS.md`
  - `agent-samples/Laravel/AGENTS.md`

### 2. Requests To Create A Skill

- If the skill is reusable across multiple AI tools, create it under `/.agents/skills/<skill-name>/`.
- If it is specific to one AI tool, place it in that tool's dedicated directory.
- Prefer reuse and centralization over duplicate implementations when an existing shared skill can cover the need.
- For task-execution skills, include clear `Activation`, `Inputs`, `Workflow`, `Guardrails`, and `Output Rules` sections unless the target format strongly requires a different structure.
- For bugfix, review, audit, migration, or other high-judgment skills, define how to handle scope limits, uncertainty, validation, and risky changes instead of only describing the ideal outcome.
- For bugfix or audit skills specifically, require all of the following when relevant:
  - Start from existing diagnostics, failing tests, logs, and concrete symptoms before broad code scanning.
  - State what to do when the repository is too large to inspect exhaustively in one pass.
  - Prioritize confirmed correctness, security, reliability, and regression issues ahead of cosmetic cleanup.
  - Distinguish confirmed bugs, suspected risks, and intentionally unmodified findings.
  - Prefer the smallest safe fix and require asking before architecture, schema, dependency, API, or other wide-impact changes.
  - Require post-change validation and a self-review of the actual diff.
- Do not create skills that imply exhaustive review, formal security auditing, or guaranteed correctness unless the workflow can realistically support that claim.
- Prefer skills that explain how to proceed when evidence is insufficient, reproduction is incomplete, or a safe fix cannot be verified locally.

### 3. Requests To Update An Existing AGENTS.md

- If the target file is specified, update that file in place.
- Do not create a new sample or duplicate file unless the user explicitly asks for a new version, variant, or comparison copy.
- Preserve the file's current scope, location, and overall purpose unless the task explicitly requires restructuring.
- If the update changes a repeated pattern that should affect templates or guides, update the related shared documentation too when appropriate.

### 4. Requests To Update An Existing Skill Or Agent File

- Update the current file in place and preserve its tool-specific format.
- Keep required metadata, frontmatter, and naming conventions unless the task explicitly requires a format change.
- If both a shared source and a tool-specific wrapper exist, update the shared source first when the change is logically shared, then adjust the wrapper only where needed.
- Do not create parallel versions just to apply a small revision.

### 5. Requests To Create Agent Files

- For general, vendor-neutral agent instructions, prefer `AGENTS.md`.
- For Claude-specific instructions, use `CLAUDE.md` or `.claude/agents/`.
- For Gemini-specific instructions, use `GEMINI.md` or `.gemini/`.
- For GitHub Copilot-specific instructions, prefer `.github/` instruction, prompt, agent, or skill formats.

## Sample Creation Rules

- `agent-samples/` is the home for distributable and reference sample outputs.
- Create one directory per sample.
- If a sample includes AI-specific variants, those can live inside that sample directory.
- If the user only asks for an `AGENTS.md`, prefer the smallest complete structure first, starting with a single `AGENTS.md` file.

## Handling Ambiguous Requests

- Ask follow-up questions when missing information would materially affect quality, such as:
  - Target technology or framework
  - Intended AI tool or tools
  - Runtime or operating environment
  - Desired strictness, scope, or output depth
- If the user asks to revise an existing file and multiple plausible targets exist, ask which file should be updated.
- If there is only one obvious target file, update it without asking.
- Do not ask unnecessary questions when common best practices are enough to produce a solid first version.
- When in doubt, create a practical first draft and include concise improvement suggestions if useful.

## Quality Standards

- Optimize for immediate usability. Do not stop at abstract guidance.
- AGENTS, Skill, and Agent files should normally include at least purpose, intended tasks, workflow, constraints, and validation guidance.
- Avoid scattering long duplicated instructions across AI-specific folders. Put shared rules in `.agents/` whenever possible.
- Only add thin AI-specific adaptation layers when the tool truly needs its own format or conventions.
- When revising an existing file, prefer targeted edits over broad rewrites unless the file is clearly unsalvageable or the user asks for a rewrite.
- Good skills should define not only what to do, but also what not to claim, when to stop, when to ask, and how to report uncertainty or incomplete coverage.

## Handling Current Information

- It is reasonable to use `.github/` for GitHub Copilot, `.claude/` for Claude Code, and `.gemini/` for Gemini CLI, but these conventions can evolve. Confirm current official guidance when it matters.
- Use `AGENTS.md` as the baseline for Codex and vendor-neutral agent instructions.
- If web verification is needed, prefer official documentation over guesses.

## Default Decision Order

- If it should be shared, use `/.agents/`
- If it is GitHub Copilot-specific, use `/.github/`
- If it is Claude Code-specific, use `/.claude/`
- If it is Gemini CLI-specific, use `/.gemini/`
- If it is an `AGENTS.md` sample, use `/agent-samples/<Topic>/AGENTS.md`
