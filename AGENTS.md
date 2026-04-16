# AGENTS.md

## Purpose Of This Repository

This repository is a workspace for creating, organizing, and reusing `AGENTS.md`, Skill files, and related agent assets for tools such as GitHub Copilot, OpenAI Codex, Claude Code, and Gemini CLI. Prefer outputs that are reusable, portable, and practical in real projects.

## Core Rules

- The root `AGENTS.md` is the operating guide for this repository itself. Do not keep sample `AGENTS.md` files at the root.
- Unless explicitly instructed otherwise, create files in English.
- Use the user's language for chat replies, questions, and other conversational responses.
- Update existing `AGENTS.md`, Skill, and Agent files in place unless the user explicitly asks for a new copy, variant, or comparison version.
- Place reusable, cross-AI assets under `.agents/`. Place AI-specific assets in the directory expected by that AI tool.
- Directory conventions and supported features can change. Verify the latest official documentation before introducing or expanding AI-specific folders.
- Handle vague requests proactively. Ask a short, concrete question only when missing information would materially affect the result. Otherwise proceed with a sensible default.
- If the user says `leave it to you`, use the latest official documentation, current tool behavior, and broadly accepted best practices.
- Treat a user message that starts with `/skill-name` as an explicit request to use the matching skill when a matching folder exists under `.agents/skills/`, `.github/skills/`, or `.claude/skills/`, even if the current AI client does not provide a native slash-skill command.

## Repository Layout

### Shared Assets

- `/.agents/`
  - Primary location for reusable assets that can work across multiple AI tools.
  - Typical examples: `/.agents/skills/`, `/.agents/agents/`, `/.agents/templates/`, `/.agents/references/`
  - Create shared skills in `/.agents/skills/` first.
  - When you create a shared skill in this repository, also create a thin Claude wrapper in `/.claude/skills/<skill-name>/SKILL.md` that points back to the shared skill.
  - GitHub Copilot should consume shared skills from `/.agents/skills/` directly in this repository unless a future case proves that a tool-specific wrapper is required.
  - Do not create AI-specific variants beyond the required Claude wrapper unless the tool truly needs a different format or behavior.

### AI-Specific Assets

- `/.github/`
  - GitHub Copilot-specific assets such as `.github/copilot-instructions.md`, `.github/instructions/`, `.github/prompts/`, `.github/agents/`, and `.github/skills/`
- `/.claude/`
  - Claude Code-specific assets such as `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, and `.claude/settings.json`
  - If persistent repository instructions are needed for Claude Code, use `CLAUDE.md`.
- `/.gemini/`
  - Gemini CLI-specific assets such as `.gemini/commands/`, `.gemini/settings.json`, and `.gemini/skills/`
  - If persistent repository instructions are needed for Gemini CLI, use `GEMINI.md`.
- `/`
  - Use `AGENTS.md` for Codex and vendor-neutral agent instructions.

## Creation Rules

### 1. Create An `AGENTS.md`

- By default, create `agent-samples/<Topic>/AGENTS.md` unless the request is clearly about this repository's own root rules.
- Use a short, clear, recognizable topic name for `<Topic>`.
- Prefer official or widely used naming where possible.
- Examples:
  - `agent-samples/UE5/AGENTS.md`
  - `agent-samples/Nextjs/AGENTS.md`
  - `agent-samples/Laravel/AGENTS.md`

### 2. Create A Skill

- Create the primary implementation under `/.agents/skills/<skill-name>/` unless the user explicitly asks for a tool-specific-only skill.
- For shared skills in this repository, also create a thin Claude wrapper under `/.claude/skills/<skill-name>/SKILL.md`.
- Do not create a `.github/skills/` wrapper for a shared skill by default in this repository.
- If a skill is truly specific to one AI tool, place it only in that tool's dedicated directory.
- Prefer reuse and centralization over duplicate implementations.
- For task-execution skills, include clear `Activation`, `Inputs`, `Workflow`, `Guardrails`, and `Output Rules` sections unless the target format strongly requires something else.
- For bugfix, review, audit, migration, or other high-judgment skills, define how to handle scope limits, uncertainty, validation, and risky changes instead of only describing the ideal outcome.
- For bugfix or audit skills, require the following when relevant:
  - Start from existing diagnostics, failing tests, logs, and concrete symptoms before broad code scanning.
  - State what to do when the repository is too large to inspect exhaustively in one pass.
  - Prioritize confirmed correctness, security, reliability, and regression issues ahead of cosmetic cleanup.
  - Distinguish confirmed bugs, suspected risks, and intentionally unmodified findings.
  - Prefer the smallest safe fix and require asking before architecture, schema, dependency, API, or other wide-impact changes.
  - Require post-change validation and a self-review of the actual diff.
- Do not create skills that imply exhaustive review, formal security auditing, or guaranteed correctness unless the workflow can realistically support that claim.
- Prefer skills that explain how to proceed when evidence is insufficient, reproduction is incomplete, or a safe fix cannot be verified locally.

### 3. Create Agent Files

- For general, vendor-neutral agent instructions, prefer `AGENTS.md`.
- For Claude-specific instructions, use `CLAUDE.md` or `.claude/agents/`.
- For Gemini-specific instructions, use `GEMINI.md` or `.gemini/`.
- For GitHub Copilot-specific instructions, prefer `.github/` instruction, prompt, agent, or skill formats.

### 4. Create Samples

- `agent-samples/` is the home for distributable and reference sample outputs.
- Create one directory per sample.
- If a sample includes AI-specific variants, those can live inside that sample directory.
- If the user only asks for an `AGENTS.md`, prefer the smallest complete structure first, starting with a single `AGENTS.md` file.

## Update Rules

### 1. Update An Existing `AGENTS.md`

- If the target file is specified, update that file in place.
- Do not create a new sample or duplicate file unless the user explicitly asks for a new version, variant, or comparison copy.
- Preserve the file's current scope, location, and overall purpose unless the task explicitly requires restructuring.
- If the update changes a repeated pattern that should affect templates or guides, update the related shared documentation too when appropriate.

### 2. Update An Existing Skill Or Agent File

- Update the current file in place and preserve its tool-specific format.
- Keep required metadata, frontmatter, and naming conventions unless the task explicitly requires a format change.
- If both a shared source and a tool-specific wrapper exist, update the shared source first when the change is logically shared, then adjust the wrapper only where needed.
- Do not create parallel versions just to apply a small revision.

## Handling Ambiguous Requests

- Ask follow-up questions when missing information would materially affect quality, such as target technology, intended AI tool, runtime environment, or desired strictness and scope.
- If the user asks to revise an existing file and multiple plausible targets exist, ask which file should be updated.
- If there is only one obvious target file, update it without asking.
- Do not ask unnecessary questions when common best practices are enough to produce a solid first version.
- When in doubt, create a practical first draft and include concise improvement suggestions if useful.

## Quality Standards

- Optimize for immediate usability. Do not stop at abstract guidance.
- AGENTS, Skill, and Agent files should normally include at least purpose, intended tasks, workflow, constraints, and validation guidance.
- Avoid scattering long duplicated instructions across AI-specific folders. Put shared rules in `.agents/` whenever possible.
- Use one shared source in `.agents/skills/` for shared skills, with a required thin Claude wrapper in `.claude/skills/`.
- Only add additional AI-specific adaptation layers when the tool truly needs them.
- When revising an existing file, prefer targeted edits over broad rewrites unless the file is clearly unsalvageable or the user asks for a rewrite.
- Good skills should define not only what to do, but also what not to claim, when to stop, when to ask, and how to report uncertainty or incomplete coverage.

## Handling Current Information

- It is reasonable to use `.github/` for GitHub Copilot, `.claude/` for Claude Code, and `.gemini/` for Gemini CLI, but these conventions can evolve. Confirm current official guidance when it matters.
- Use `AGENTS.md` as the baseline for Codex and vendor-neutral agent instructions.
- If web verification is needed, prefer official documentation over guesses.

## Default Decision Order

- If it should be shared, use `/.agents/`.
- If it is a shared skill, create it in `/.agents/skills/` and add a thin wrapper in `/.claude/skills/`.
- If it is GitHub Copilot-specific and cannot use the shared skill directly, use `/.github/`.
- If it is Claude Code-specific, use `/.claude/`.
- If it is Gemini CLI-specific, use `/.gemini/`.
- If it is an `AGENTS.md` sample, use `/agent-samples/<Topic>/AGENTS.md`.
