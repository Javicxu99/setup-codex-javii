#!/usr/bin/env python3
"""Bootstrap a project with Javii's Codex setup."""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


ROOT_MARKERS = (".git", "pyproject.toml", "package.json", "Cargo.toml", "go.mod")
PROFILES = ("default", "vehicle-3d")


@dataclass
class Report:
    created: list[Path] = field(default_factory=list)
    updated: list[Path] = field(default_factory=list)
    backups: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a target project with Javii's Codex setup."
    )
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="default",
        help="Bootstrap profile to apply.",
    )
    return parser.parse_args()


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate
    raise RuntimeError(
        "Could not detect a project root. Run inside a project with .git, "
        "pyproject.toml, package.json, Cargo.toml, or go.mod."
    )


def infer_primary_language(root: Path) -> str:
    if (root / "pyproject.toml").exists():
        return "Python"
    if (root / "package.json").exists():
        return "JavaScript/TypeScript"
    if (root / "Cargo.toml").exists():
        return "Rust"
    if (root / "go.mod").exists():
        return "Go"
    return "Unknown"


def render_template(template_path: Path, values: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def next_backup_path(path: Path) -> Path:
    first = path.with_name(path.name + ".bak")
    if not first.exists():
        return first
    index = 1
    while True:
        candidate = path.with_name(path.name + f".bak.{index}")
        if not candidate.exists():
            return candidate
        index += 1


def write_rendered_file(
    source: Path,
    destination: Path,
    values: dict[str, str],
    report: Report,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = render_template(source, values)

    if destination.exists():
        backup = next_backup_path(destination)
        shutil.copy2(destination, backup)
        report.backups.append(backup)
        report.updated.append(destination)
    else:
        report.created.append(destination)

    destination.write_text(content, encoding="utf-8", newline="\n")


def bootstrap(profile: str) -> Report:
    script_path = Path(__file__).resolve()
    skill_root = script_path.parents[1]
    assets = skill_root / "assets"
    common = assets / "common"
    profile_root = assets / "profiles" / profile
    target_root = find_project_root(Path.cwd())

    values = {
        "PROJECT_NAME": target_root.name,
        "DATE": date.today().isoformat(),
        "PRIMARY_LANGUAGE": infer_primary_language(target_root),
        "PROFILE": profile,
    }

    report = Report()

    (target_root / ".codex" / "prompts").mkdir(parents=True, exist_ok=True)
    (target_root / ".codex" / "skills").mkdir(parents=True, exist_ok=True)
    (target_root / "docs").mkdir(parents=True, exist_ok=True)

    agents_template = common / "AGENTS.template.md"
    project_context_template = common / "project-context.template.md"
    if profile != "default":
        profile_agents = profile_root / "AGENTS.template.md"
        profile_context = profile_root / "project-context.template.md"
        if profile_agents.exists():
            agents_template = profile_agents
        if profile_context.exists():
            project_context_template = profile_context

    file_map = [
        (agents_template, target_root / "AGENTS.md"),
        (common / "config.template.toml", target_root / ".codex" / "config.toml"),
        (project_context_template, target_root / "docs" / "project-context.md"),
        (common / "architecture.template.md", target_root / "docs" / "architecture.md"),
        (common / "task-log.template.md", target_root / "docs" / "task-log.md"),
        (common / "README.codex.template.md", target_root / "docs" / "README.codex.md"),
        (
            assets / "skills" / "project-orientation" / "SKILL.md",
            target_root / ".codex" / "skills" / "project-orientation" / "SKILL.md",
        ),
        (
            assets / "skills" / "update-project-context" / "SKILL.md",
            target_root / ".codex" / "skills" / "update-project-context" / "SKILL.md",
        ),
        (
            assets / "skills" / "karpathy-guidelines" / "SKILL.md",
            target_root / ".codex" / "skills" / "karpathy-guidelines" / "SKILL.md",
        ),
    ]

    if profile == "vehicle-3d":
        file_map.extend(
            [
                (profile_root / "data.template.md", target_root / "docs" / "data.md"),
                (profile_root / "training.template.md", target_root / "docs" / "training.md"),
                (profile_root / "evaluation.template.md", target_root / "docs" / "evaluation.md"),
                (profile_root / "export-onnx.template.md", target_root / "docs" / "export-onnx.md"),
                (profile_root / "tensorrt.template.md", target_root / "docs" / "tensorrt.md"),
                (
                    profile_root / "jetson-deployment.template.md",
                    target_root / "docs" / "jetson-deployment.md",
                ),
            ]
        )

    for source, destination in file_map:
        if not source.exists():
            raise RuntimeError(f"Missing asset template: {source}")
        write_rendered_file(source, destination, values, report)

    return report


def print_paths(title: str, paths: list[Path]) -> None:
    print(f"{title}: {len(paths)}")
    for path in paths:
        print(f"  - {path}")


def main() -> int:
    args = parse_args()
    try:
        report = bootstrap(args.profile)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Codex bootstrap complete.")
    print_paths("Files created", report.created)
    print_paths("Files updated with backup", report.updated)
    print_paths("Files skipped", report.skipped)
    print_paths("Backups created", report.backups)
    print("Recommended next steps:")
    print("  - Review AGENTS.md and docs/project-context.md.")
    print("  - Add project-specific details to docs/architecture.md and docs/task-log.md.")
    print("  - Run your normal validation before committing generated files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

