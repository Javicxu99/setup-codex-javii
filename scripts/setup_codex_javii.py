#!/usr/bin/env python3
"""Bootstrap a project with provider-separated Codex and Claude environments."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable


MIN_PYTHON = (3, 11)
ROOT_MARKERS = (".git", "pyproject.toml", "package.json", "Cargo.toml", "go.mod")
PROFILES = ("default",)
COMPONENTS = ("codex", "claude", "docs", "github", "compliance", "shared")
CONFLICT_POLICIES = ("backup", "skip")
LEGACY_SCHEDULED_AUDIT = Path(".github/workflows/daily-project-health.yml")
MANAGED_GITIGNORE_BLOCK = """# setup-codex-javii managed local state
.codex/sessions/
.codex/history/
.codex/transcripts/
docs/conversations/raw/
.claude/settings.local.json
.claude/session-log.txt
tmp/
*.bak
*.bak.*
# end setup-codex-javii managed local state
"""


@dataclass
class Report:
    created: list[Path] = field(default_factory=list)
    updated: list[Path] = field(default_factory=list)
    backups: list[Path] = field(default_factory=list)
    unchanged: list[Path] = field(default_factory=list)
    preserved: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ManagedFile:
    component: str
    source: Path
    destination: Path
    create_only: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Preview or apply Javii's Codex and Claude Code project bootstrap. "
            "Preview is the default."
        )
    )
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="default",
        help="Bootstrap profile to apply.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Directory used to detect the target project root (default: current directory).",
    )
    parser.add_argument(
        "--components",
        nargs="+",
        choices=COMPONENTS,
        default=COMPONENTS,
        metavar="COMPONENT",
        help="Components to include; defaults to all components.",
    )
    parser.add_argument(
        "--on-conflict",
        choices=CONFLICT_POLICIES,
        default="backup",
        help=(
            "For a changed existing file, create a backup and overwrite it, "
            "or preserve it with skip."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Apply the displayed plan. Existing changed files are backed up by default.",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly request preview mode (also the default).",
    )
    return parser.parse_args()


def require_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        required = ".".join(str(part) for part in MIN_PYTHON)
        current = ".".join(str(part) for part in sys.version_info[:3])
        raise RuntimeError(
            f"Python {required}+ is required; the active interpreter is Python {current}."
        )


def find_project_root(start: Path) -> Path:
    if not start.exists():
        raise RuntimeError(f"Target path does not exist: {start}")
    if not start.is_dir():
        raise RuntimeError(f"Target path is not a directory: {start}")

    current = start.resolve()
    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate
    raise RuntimeError(
        "Could not detect a project root. Use --target with a directory inside a project "
        "containing .git, pyproject.toml, package.json, Cargo.toml, or go.mod."
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


def atomic_write_text(destination: Path, content: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def read_existing_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise RuntimeError(f"Cannot safely compare existing text file {path}: {exc}") from exc


def write_content(
    destination: Path,
    content: str,
    report: Report,
    *,
    apply: bool,
    on_conflict: str,
) -> None:
    if destination.exists():
        if on_conflict == "skip":
            report.preserved.append(destination)
            return
        if read_existing_text(destination) == content:
            report.unchanged.append(destination)
            return

        report.updated.append(destination)
        if not apply:
            return

        backup = next_backup_path(destination)
        shutil.copy2(destination, backup)
        report.backups.append(backup)
        atomic_write_text(destination, content)
        return

    report.created.append(destination)
    if apply:
        atomic_write_text(destination, content)


def write_rendered_file(
    source: Path,
    destination: Path,
    values: dict[str, str],
    report: Report,
    *,
    apply: bool,
    on_conflict: str,
) -> None:
    write_content(
        destination,
        render_template(source, values),
        report,
        apply=apply,
        on_conflict=on_conflict,
    )


def ensure_gitignore_entries(
    target_root: Path,
    report: Report,
    *,
    apply: bool,
    on_conflict: str,
) -> None:
    destination = target_root / ".gitignore"
    if destination.exists() and on_conflict == "skip":
        report.preserved.append(destination)
        return

    if not destination.exists():
        content = MANAGED_GITIGNORE_BLOCK
    else:
        existing = read_existing_text(destination)
        if MANAGED_GITIGNORE_BLOCK in existing:
            report.unchanged.append(destination)
            return
        separator = "\n\n" if existing.strip() else ""
        content = existing.rstrip() + separator + MANAGED_GITIGNORE_BLOCK

    write_content(
        destination,
        content,
        report,
        apply=apply,
        on_conflict=on_conflict,
    )


def write_mcp_json(
    target_root: Path,
    report: Report,
    *,
    apply: bool,
    on_conflict: str,
) -> None:
    destination = target_root / ".mcp.json"
    server = {"command": "codebase-memory-mcp"}

    if destination.exists() and on_conflict == "skip":
        report.preserved.append(destination)
        return

    if not destination.exists():
        content = {"mcpServers": {"codebase-memory-mcp": server}}
    else:
        try:
            content = json.loads(destination.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError, UnicodeError) as exc:
            raise RuntimeError(f"Cannot safely update {destination}: {exc}") from exc

        servers = content.setdefault("mcpServers", {})
        if not isinstance(servers, dict):
            raise RuntimeError(
                f"Cannot safely update {destination}: mcpServers is not an object"
            )
        if servers.get("codebase-memory-mcp") == server:
            report.unchanged.append(destination)
            return
        servers["codebase-memory-mcp"] = server

    write_content(
        destination,
        json.dumps(content, indent=2) + "\n",
        report,
        apply=apply,
        on_conflict=on_conflict,
    )


def normalize_components(components: Iterable[str] | None) -> tuple[str, ...]:
    requested = set(COMPONENTS if components is None else components)
    unknown = requested.difference(COMPONENTS)
    if unknown:
        raise RuntimeError(f"Unknown bootstrap components: {', '.join(sorted(unknown))}")
    return tuple(component for component in COMPONENTS if component in requested)


def build_file_map(source_root: Path, target_root: Path) -> list[ManagedFile]:
    bootstrap_skill_root = source_root / ".codex" / "skills" / "setup-codex-javii"
    assets = bootstrap_skill_root / "assets"
    claude_assets = source_root / ".claude" / "bootstrap-assets"
    common = assets / "common"
    compliance_assets = assets / "compliance"
    compliance_docs = source_root / "docs" / "compliance" / "eu-ai-act"

    entries = [
        ManagedFile("codex", common / "AGENTS.template.md", target_root / "AGENTS.md"),
        ManagedFile(
            "codex", common / "config.template.toml", target_root / ".codex/config.toml"
        ),
        ManagedFile(
            "codex", assets / "hooks/hooks.json", target_root / ".codex/hooks.json"
        ),
        ManagedFile(
            "codex",
            assets / "hooks/session_start_ponytail.py",
            target_root / ".codex/hooks/session_start_ponytail.py",
        ),
        ManagedFile(
            "codex",
            assets / "agents/project-health-auditor.toml",
            target_root / ".codex/agents/project-health-auditor.toml",
        ),
        ManagedFile(
            "codex",
            assets / "prompts/archive-session.md",
            target_root / ".codex/prompts/archive-session.md",
        ),
        ManagedFile(
            "codex",
            assets / "prompts/release-check.md",
            target_root / ".codex/prompts/release-check.md",
        ),
        ManagedFile(
            "codex",
            assets / "prompts/codebase-memory-orient.md",
            target_root / ".codex/prompts/codebase-memory-orient.md",
        ),
        ManagedFile(
            "codex",
            assets / "prompts/project-health-audit.md",
            target_root / ".codex/prompts/project-health-audit.md",
        ),
    ]
    entries.extend(
        ManagedFile(
            "codex",
            assets / f"skills/{skill}/SKILL.md",
            target_root / f".codex/skills/{skill}/SKILL.md",
        )
        for skill in (
            "project-orientation",
            "update-project-context",
            "karpathy-guidelines",
            "codebase-memory",
            "ponytail",
            "audit-web-quality",
            "review-skill-security",
        )
    )
    entries.extend(
        [
            ManagedFile(
                "claude", claude_assets / "CLAUDE.template.md", target_root / "CLAUDE.md"
            ),
            ManagedFile(
                "claude",
                claude_assets / "settings.template.json",
                target_root / ".claude/settings.json",
            ),
            ManagedFile(
                "claude",
                claude_assets / "agents/project-health-auditor.md",
                target_root / ".claude/agents/project-health-auditor.md",
            ),
            ManagedFile(
                "claude",
                claude_assets / "output-styles/pragmatic.md",
                target_root / ".claude/output-styles/pragmatic.md",
            ),
            ManagedFile(
                "claude",
                claude_assets / "hooks/session_start_ponytail.py",
                target_root / ".claude/hooks/session_start_ponytail.py",
            ),
        ]
    )
    entries.extend(
        ManagedFile(
            "claude",
            claude_assets / f"skills/{skill}/SKILL.md",
            target_root / f".claude/skills/{skill}/SKILL.md",
        )
        for skill in (
            "karpathy",
            "caveman",
            "codebase-memory",
            "ponytail",
            "archive",
            "release-check",
            "audit-web-quality",
            "review-skill-security",
        )
    )
    entries.extend(
        [
            ManagedFile(
                "docs",
                common / "project-context.template.md",
                target_root / "docs/project-context.md",
            ),
            ManagedFile(
                "docs", common / "architecture.template.md", target_root / "docs/architecture.md"
            ),
            ManagedFile(
                "docs", common / "task-log.template.md", target_root / "docs/task-log.md"
            ),
            ManagedFile(
                "docs",
                common / "codebase-memory.template.md",
                target_root / "docs/codebase-memory.md",
            ),
            ManagedFile(
                "docs",
                common / "codex-session-notes.template.md",
                target_root / "docs/codex-session-notes.md",
            ),
            ManagedFile(
                "docs", common / "README.codex.template.md", target_root / "docs/README.codex.md"
            ),
            ManagedFile(
                "docs",
                claude_assets / "claude-session-notes.template.md",
                target_root / "docs/claude-session-notes.md",
            ),
            ManagedFile(
                "github",
                assets / "github/PULL_REQUEST_TEMPLATE.md",
                target_root / ".github/PULL_REQUEST_TEMPLATE.md",
            ),
            ManagedFile(
                "github",
                assets / "github/ISSUE_TEMPLATE/bug_report.md",
                target_root / ".github/ISSUE_TEMPLATE/bug_report.md",
            ),
            ManagedFile(
                "github",
                assets / "github/ISSUE_TEMPLATE/change_request.md",
                target_root / ".github/ISSUE_TEMPLATE/change_request.md",
            ),
            ManagedFile(
                "github",
                assets / "github/ISSUE_TEMPLATE/config.yml",
                target_root / ".github/ISSUE_TEMPLATE/config.yml",
            ),
            ManagedFile(
                "shared", common / "CHANGELOG.template.md", target_root / "CHANGELOG.md"
            ),
        ]
    )
    entries.extend(
        [
            ManagedFile(
                "compliance",
                source_root / "scripts/check_eu_ai_act.py",
                target_root / "scripts/check_eu_ai_act.py",
            ),
            ManagedFile(
                "compliance",
                compliance_docs / "README.md",
                target_root / "docs/compliance/eu-ai-act/README.md",
            ),
            ManagedFile(
                "compliance",
                compliance_docs / "legal-baseline.json",
                target_root / "docs/compliance/eu-ai-act/legal-baseline.json",
            ),
            ManagedFile(
                "compliance",
                compliance_assets / "intake.template.json",
                target_root / "docs/compliance/eu-ai-act/intake.json",
                create_only=True,
            ),
            ManagedFile(
                "compliance",
                compliance_assets / "controls.template.md",
                target_root / "docs/compliance/eu-ai-act/controls.md",
                create_only=True,
            ),
            ManagedFile(
                "compliance",
                compliance_assets / "release-evidence.template.md",
                target_root / "docs/compliance/eu-ai-act/release-evidence.md",
                create_only=True,
            ),
            ManagedFile(
                "compliance",
                compliance_assets / "high-risk.template.md",
                target_root / "docs/compliance/eu-ai-act/high-risk/README.md",
                create_only=True,
            ),
            ManagedFile(
                "compliance",
                assets / "prompts/eu-ai-act-intake.md",
                target_root / ".codex/prompts/eu-ai-act-intake.md",
            ),
            ManagedFile(
                "compliance",
                assets / "skills/eu-ai-act-governance/SKILL.md",
                target_root / ".codex/skills/eu-ai-act-governance/SKILL.md",
            ),
            ManagedFile(
                "compliance",
                claude_assets / "skills/eu-ai-act-governance/SKILL.md",
                target_root / ".claude/skills/eu-ai-act-governance/SKILL.md",
            ),
        ]
    )
    return entries


def bootstrap(
    profile: str,
    *,
    target: Path | None = None,
    apply: bool = False,
    components: Iterable[str] | None = None,
    on_conflict: str = "backup",
) -> Report:
    require_supported_python()
    if profile not in PROFILES:
        raise RuntimeError(f"Unsupported profile: {profile}")
    if on_conflict not in CONFLICT_POLICIES:
        raise RuntimeError(f"Unsupported conflict policy: {on_conflict}")

    selected_components = normalize_components(components)
    source_root = Path(__file__).resolve().parents[1]
    target_root = find_project_root(Path.cwd() if target is None else target)
    version_path = source_root / "VERSION"
    file_map = build_file_map(source_root, target_root)

    required_sources = [
        entry.source for entry in file_map if entry.component in selected_components
    ]
    missing_sources = [source for source in required_sources if not source.is_file()]
    if not version_path.is_file() or missing_sources:
        missing = [version_path] if not version_path.is_file() else []
        missing.extend(missing_sources)
        details = "\n".join(f"  - {path}" for path in missing)
        raise RuntimeError(
            "Could not locate the complete setup-codex-javii assets:\n" + details
        )

    if apply:
        # Validate every planned read and merge before the first filesystem mutation.
        bootstrap(
            profile,
            target=target_root,
            apply=False,
            components=selected_components,
            on_conflict=on_conflict,
        )

    values = {
        "PROJECT_NAME": target_root.name,
        "DATE": date.today().isoformat(),
        "PRIMARY_LANGUAGE": infer_primary_language(target_root),
        "PROFILE": profile,
        "BOOTSTRAP_VERSION": version_path.read_text(encoding="utf-8").strip(),
    }
    report = Report()

    for entry in file_map:
        if entry.component in selected_components:
            if entry.create_only and entry.destination.exists():
                report.preserved.append(entry.destination)
                continue
            write_rendered_file(
                entry.source,
                entry.destination,
                values,
                report,
                apply=apply,
                on_conflict=on_conflict,
            )

    if "shared" in selected_components:
        write_mcp_json(target_root, report, apply=apply, on_conflict=on_conflict)
        ensure_gitignore_entries(
            target_root, report, apply=apply, on_conflict=on_conflict
        )

    legacy_workflow = target_root / LEGACY_SCHEDULED_AUDIT
    if legacy_workflow.exists():
        report.warnings.append(
            f"Legacy scheduled audit still exists at {legacy_workflow}. This bootstrap will "
            "not delete user files; remove it manually after review to stop API-key failures."
        )

    return report


def print_paths(title: str, paths: list[Path]) -> None:
    print(f"{title}: {len(paths)}")
    for path in paths:
        print(f"  - {path}")


def print_report(
    report: Report,
    *,
    target_root: Path,
    components: tuple[str, ...],
    apply: bool,
    on_conflict: str,
) -> None:
    mode = "APPLY" if apply else "PREVIEW (no files changed)"
    print(f"setup-codex-javii mode: {mode}")
    print(f"Target: {target_root}")
    print(f"Components: {', '.join(components)}")
    print(f"Existing-file policy: {on_conflict}")
    print_paths("Files created" if apply else "Files to create", report.created)
    print_paths(
        "Files updated with backup" if apply else "Files to update (backup on apply)",
        report.updated,
    )
    print_paths("Files unchanged", report.unchanged)
    print_paths("Existing files preserved", report.preserved)
    print_paths("Backups created", report.backups)
    if report.warnings:
        print("Warnings:")
        for warning in report.warnings:
            print(f"  - {warning}")

    if not apply:
        print("No files were changed. Re-run with --apply after reviewing this plan.")
        return

    print("Bootstrap complete (Codex + Claude Code).")
    print("Recommended next steps:")
    print("  - Review AGENTS.md, CLAUDE.md, and docs/project-context.md.")
    print("  - Run your normal project validation before committing generated files.")
    print(
        "  - In Codex Desktop, request the read-only audit from "
        ".codex/prompts/project-health-audit.md when needed."
    )
    if "compliance" in components:
        print(
            "  - Complete docs/compliance/eu-ai-act/intake.json, then run "
            "python scripts/check_eu_ai_act.py --root . before release."
        )
    print("  - Install codebase-memory-mcp only if you want the optional graph workflow.")


def main() -> int:
    try:
        require_supported_python()
        args = parse_args()
        components = normalize_components(args.components)
        target_root = find_project_root(args.target)
        report = bootstrap(
            args.profile,
            target=target_root,
            apply=args.apply,
            components=components,
            on_conflict=args.on_conflict,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print_report(
        report,
        target_root=target_root,
        components=components,
        apply=args.apply,
        on_conflict=args.on_conflict,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
