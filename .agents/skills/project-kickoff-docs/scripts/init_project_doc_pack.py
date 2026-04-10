#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


CORE_FILES = {
    "README.template.md": "README.md",
    "AGENTS.template.md": "AGENTS.md",
    "docs/project-overview.template.md": "docs/project-overview.md",
    "docs/product-spec.template.md": "docs/product-spec.md",
    "docs/architecture.template.md": "docs/architecture.md",
    "docs/data-model.template.md": "docs/data-model.md",
    "docs/implementation-plan.template.md": "docs/implementation-plan.md",
    "docs/task-breakdown.template.md": "docs/task-breakdown.md",
    "docs/acceptance-criteria.template.md": "docs/acceptance-criteria.md",
    "docs/ai-implementation-guide.template.md": "docs/ai-implementation-guide.md",
}

OPTIONAL_FILES = {
    "api-contracts": ("docs/api-contracts.template.md", "docs/api-contracts.md"),
    "ui-spec": ("docs/ui-spec.template.md", "docs/ui-spec.md"),
    "integrations": ("docs/integrations.template.md", "docs/integrations.md"),
    "testing-strategy": ("docs/testing-strategy.template.md", "docs/testing-strategy.md"),
    "open-questions": ("docs/open-questions.template.md", "docs/open-questions.md"),
    "decision-log": ("docs/decision-log.template.md", "docs/decision-log.md"),
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def parse_include(raw: str | None) -> list[str]:
    if not raw:
        return []

    values = [item.strip() for item in raw.split(",") if item.strip()]
    invalid = [item for item in values if item not in OPTIONAL_FILES]
    if invalid:
        raise ValueError(
            "Unknown optional docs: "
            + ", ".join(invalid)
            + ". Valid values: "
            + ", ".join(sorted(OPTIONAL_FILES))
        )
    return values


def render_template(content: str, project_name: str) -> str:
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": slugify(project_name),
        "{{DATE_ISO}}": date.today().isoformat(),
    }
    for token, value in replacements.items():
        content = content.replace(token, value)
    return content


def write_file(template_path: Path, target_path: Path, project_name: str, force: bool) -> str:
    existed_before = target_path.exists()
    if existed_before and not force:
        return "skipped"

    target_path.parent.mkdir(parents=True, exist_ok=True)
    content = template_path.read_text(encoding="utf-8")
    rendered = render_template(content, project_name)
    target_path.write_text(rendered, encoding="utf-8")
    return "overwritten" if existed_before else "created"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a project kickoff documentation pack from bundled templates."
    )
    parser.add_argument("--target", help="Target repository or project directory")
    parser.add_argument("--project-name", help="Project name used for template substitution")
    parser.add_argument(
        "--include",
        help="Comma-separated optional docs: " + ",".join(sorted(OPTIONAL_FILES)),
    )
    parser.add_argument(
        "--list-optional",
        action="store_true",
        help="Print available optional doc keys and exit",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of skipping them",
    )
    args = parser.parse_args()

    if args.list_optional:
        for key in sorted(OPTIONAL_FILES):
            print(key)
        return 0

    if not args.target:
        parser.error("--target is required unless --list-optional is used")

    if not args.project_name:
        parser.error("--project-name is required unless --list-optional is used")

    selected_optional = parse_include(args.include)
    template_root = Path(__file__).resolve().parent.parent / "assets" / "templates"
    target_root = Path(args.target).resolve()
    target_root.mkdir(parents=True, exist_ok=True)

    files_to_create = list(CORE_FILES.items())
    for key in selected_optional:
        files_to_create.append(OPTIONAL_FILES[key])

    results: list[tuple[str, str]] = []
    for template_rel, target_rel in files_to_create:
        template_path = template_root / template_rel
        target_path = target_root / target_rel
        status = write_file(template_path, target_path, args.project_name, args.force)
        results.append((target_rel, status))

    print(f"Target: {target_root}")
    for path, status in results:
        print(f"{status:11} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
