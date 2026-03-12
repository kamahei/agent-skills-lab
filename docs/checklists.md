# Checklists

Use these checklists before finalizing new files in this repository.

## AGENTS.md Checklist

- The file clearly states the project purpose or scope.
- The file defines how to handle ambiguous requests.
- The file defines language rules for created files and chat replies.
- The file defines placement rules or repository boundaries when relevant.
- The file includes validation expectations.
- The guidance is practical and actionable, not only high-level.

## Skill Checklist

- The skill has a clear activation condition.
- The skill states what inputs or repository context it expects.
- The workflow is specific enough to execute consistently.
- The output format or output expectations are clear.
- The skill does not duplicate a reusable shared skill unnecessarily.
- The skill matches the target tool's expected format.

## Agent File Checklist

- The agent purpose is clear from the frontmatter or header.
- The file explains what the agent should and should not do.
- Tool or runtime constraints are explicit when relevant.
- The agent avoids unsupported handoff or tool assumptions.
- The file is concise enough to be maintainable.

## Sample Output Checklist

- The sample is placed under `agent-samples/<Topic>/`.
- The sample is understandable without extra hidden context.
- The sample uses English unless intentionally localized.
- The sample includes only useful supporting files.
- Any environment variable examples follow `docs/env-example-policy.md`.

## Template Checklist

- Placeholders are obvious and easy to replace.
- The template does not hardcode project-specific secrets or identifiers.
- The template is general enough to reuse more than once.
- The template is documented in the relevant README when needed.

## Final Consistency Check

- Paths and examples match the current repository structure.
- Naming is consistent across README files, templates, and samples.
- Shared content was not copied into multiple places without reason.
- Related documentation was updated if the change introduced a new pattern.
