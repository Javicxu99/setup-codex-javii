from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "setup_codex_javii.py"


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location("setup_codex_javii", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import bootstrap script: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def create_target() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary_directory = tempfile.TemporaryDirectory()
    target = Path(temporary_directory.name)
    (target / ".git").mkdir()
    return temporary_directory, target


class BootstrapTests(unittest.TestCase):
    def test_preview_apply_and_repeat_are_safe_and_idempotent(self) -> None:
        module = load_bootstrap_module()
        temporary_directory, target = create_target()
        self.addCleanup(temporary_directory.cleanup)

        original_agents = "# Existing project instructions\n"
        original_mcp = '{"mcpServers":{"existing":{"command":"keep-me"}}}'
        (target / "AGENTS.md").write_text(original_agents, encoding="utf-8")
        (target / ".mcp.json").write_text(original_mcp, encoding="utf-8-sig")

        preview = module.bootstrap("default", target=target)
        self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), original_agents)
        self.assertEqual(
            (target / ".mcp.json").read_text(encoding="utf-8-sig"), original_mcp
        )
        self.assertFalse((target / ".codex").exists())
        self.assertFalse((target / "AGENTS.md.bak").exists())
        self.assertIn(target / "AGENTS.md", preview.updated)
        self.assertEqual(preview.backups, [])

        first = module.bootstrap("default", target=target, apply=True)

        for relative_path in (
            ".codex/skills/audit-web-quality/SKILL.md",
            ".codex/skills/review-skill-security/SKILL.md",
            ".claude/skills/audit-web-quality/SKILL.md",
            ".claude/skills/review-skill-security/SKILL.md",
            ".codex/hooks.json",
            ".codex/hooks/session_start_ponytail.py",
            ".codex/agents/project-health-auditor.toml",
            ".codex/prompts/project-health-audit.md",
            ".claude/agents/project-health-auditor.md",
            ".claude/hooks/session_start_ponytail.py",
            ".claude/output-styles/pragmatic.md",
            "docs/claude-session-notes.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ):
            self.assertTrue((target / relative_path).is_file(), relative_path)

        self.assertFalse((target / ".github/workflows/daily-project-health.yml").exists())
        self.assertFalse((target / ".github/codex/prompts/daily-project-health.md").exists())

        codex_config = tomllib.loads(
            (target / ".codex/config.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(codex_config["model"], "gpt-5.6-sol")
        self.assertEqual(codex_config["model_reasoning_effort"], "medium")
        self.assertEqual(codex_config["approval_policy"], "never")
        self.assertEqual(codex_config["sandbox_mode"], "danger-full-access")

        claude_settings = json.loads(
            (target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertEqual(claude_settings["model"], "claude-fable-5")
        self.assertEqual(claude_settings["effortLevel"], "high")
        self.assertEqual(
            claude_settings["permissions"]["defaultMode"], "bypassPermissions"
        )
        self.assertTrue(claude_settings["skipDangerousModePermissionPrompt"])

        codex_hooks = json.loads(
            (target / ".codex/hooks.json").read_text(encoding="utf-8")
        )
        hook_definition = codex_hooks["hooks"]["SessionStart"][0]["hooks"][0]
        self.assertIn("git rev-parse --show-toplevel", hook_definition["command"])
        self.assertIn("commandWindows", hook_definition)

        hook = subprocess.run(
            [sys.executable, str(target / ".codex/hooks/session_start_ponytail.py")],
            input='{"hook_event_name":"SessionStart"}',
            text=True,
            capture_output=True,
            check=True,
        )
        hook_output = json.loads(hook.stdout)
        self.assertIn(
            "Ponytail Lite", hook_output["hookSpecificOutput"]["additionalContext"]
        )

        mcp_config = json.loads((target / ".mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(mcp_config["mcpServers"]["existing"]["command"], "keep-me")
        self.assertEqual(
            mcp_config["mcpServers"]["codebase-memory-mcp"]["command"],
            "codebase-memory-mcp",
        )
        self.assertIn("AGENTS.md.bak", [path.name for path in first.backups])
        self.assertIn(".mcp.json.bak", [path.name for path in first.backups])

        second = module.bootstrap("default", target=target, apply=True)
        self.assertEqual(second.created, [])
        self.assertEqual(second.updated, [])
        self.assertEqual(second.backups, [])
        self.assertGreater(len(second.unchanged), 20)
        self.assertFalse((target / "AGENTS.md.bak.1").exists())

    def test_skip_policy_preserves_every_existing_conflict(self) -> None:
        module = load_bootstrap_module()
        temporary_directory, target = create_target()
        self.addCleanup(temporary_directory.cleanup)

        (target / "AGENTS.md").write_text("keep agents\n", encoding="utf-8")
        (target / ".mcp.json").write_text("not-json", encoding="utf-8")
        (target / ".gitignore").write_text("keep-ignore\n", encoding="utf-8")

        report = module.bootstrap(
            "default",
            target=target,
            apply=True,
            components=("codex", "shared"),
            on_conflict="skip",
        )

        self.assertEqual((target / "AGENTS.md").read_text(), "keep agents\n")
        self.assertEqual((target / ".mcp.json").read_text(), "not-json")
        self.assertEqual((target / ".gitignore").read_text(), "keep-ignore\n")
        self.assertEqual(report.backups, [])
        self.assertIn(target / "AGENTS.md", report.preserved)
        self.assertIn(target / ".mcp.json", report.preserved)
        self.assertTrue((target / ".codex/config.toml").is_file())

    def test_component_selection_is_strict(self) -> None:
        module = load_bootstrap_module()
        temporary_directory, target = create_target()
        self.addCleanup(temporary_directory.cleanup)

        module.bootstrap(
            "default", target=target, apply=True, components=("codex",)
        )

        self.assertTrue((target / "AGENTS.md").is_file())
        self.assertTrue((target / ".codex/config.toml").is_file())
        self.assertFalse((target / "CLAUDE.md").exists())
        self.assertFalse((target / ".claude").exists())
        self.assertFalse((target / "docs").exists())
        self.assertFalse((target / ".github").exists())
        self.assertFalse((target / ".mcp.json").exists())
        self.assertFalse((target / ".gitignore").exists())

    def test_cli_defaults_to_preview_then_applies_explicitly(self) -> None:
        temporary_directory, target = create_target()
        self.addCleanup(temporary_directory.cleanup)

        preview = subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(target)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("PREVIEW (no files changed)", preview.stdout)
        self.assertFalse((target / ".codex").exists())

        applied = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--target",
                str(target),
                "--components",
                "codex",
                "--apply",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("mode: APPLY", applied.stdout)
        self.assertTrue((target / ".codex/config.toml").is_file())

    def test_preflight_failure_leaves_target_unchanged(self) -> None:
        module = load_bootstrap_module()
        temporary_directory, target = create_target()
        self.addCleanup(temporary_directory.cleanup)
        (target / ".mcp.json").write_text("not-json", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "Cannot safely update"):
            module.bootstrap(
                "default", target=target, apply=True, components=("shared",)
            )

        self.assertFalse((target / "CHANGELOG.md").exists())
        self.assertFalse((target / ".gitignore").exists())
        self.assertEqual((target / ".mcp.json").read_text(), "not-json")

    def test_provider_boundaries_and_canonical_assets(self) -> None:
        def combined_text(root: Path) -> str:
            return "\n".join(
                path.read_text(encoding="utf-8", errors="ignore")
                for path in root.rglob("*")
                if path.is_file()
            ).lower()

        codex_text = combined_text(REPO_ROOT / ".codex")
        claude_text = combined_text(REPO_ROOT / ".claude")
        self.assertNotIn("claude-fable-5", codex_text)
        self.assertNotIn("gpt-5.6-sol", claude_text)

        pairs = (
            (
                ".codex/hooks.json",
                ".codex/skills/setup-codex-javii/assets/hooks/hooks.json",
            ),
            (
                ".codex/agents/project-health-auditor.toml",
                ".codex/skills/setup-codex-javii/assets/agents/project-health-auditor.toml",
            ),
            (
                ".codex/prompts/project-health-audit.md",
                ".codex/skills/setup-codex-javii/assets/prompts/project-health-audit.md",
            ),
            (
                ".claude/agents/project-health-auditor.md",
                ".claude/bootstrap-assets/agents/project-health-auditor.md",
            ),
        )
        for live_path, asset_path in pairs:
            self.assertEqual(
                (REPO_ROOT / live_path).read_bytes(),
                (REPO_ROOT / asset_path).read_bytes(),
                live_path,
            )

        self.assertEqual(
            json.loads((REPO_ROOT / ".claude/settings.json").read_text(encoding="utf-8")),
            json.loads(
                (
                    REPO_ROOT / ".claude/bootstrap-assets/settings.template.json"
                ).read_text(encoding="utf-8")
            ),
        )

        self.assertFalse((REPO_ROOT / ".github/workflows/daily-project-health.yml").exists())
        self.assertFalse(
            (
                REPO_ROOT
                / ".codex/skills/setup-codex-javii/assets/github/workflows/daily-project-health.yml"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
