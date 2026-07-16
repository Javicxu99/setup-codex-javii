from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / ".codex"
    / "skills"
    / "setup-codex-javii"
    / "scripts"
    / "setup_codex_javii.py"
)


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location("setup_codex_javii", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import bootstrap script: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BootstrapTests(unittest.TestCase):
    def test_generates_complete_agent_setup_and_merges_bom_mcp_config(self) -> None:
        module = load_bootstrap_module()

        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            (target / ".git").mkdir()
            (target / ".mcp.json").write_text(
                '{"mcpServers":{"existing":{"command":"keep-me"}}}',
                encoding="utf-8-sig",
            )

            previous_directory = Path.cwd()
            try:
                os.chdir(target)
                first_report = module.bootstrap("default")
                second_report = module.bootstrap("default")
            finally:
                os.chdir(previous_directory)

            for relative_path in (
                ".codex/skills/audit-web-quality/SKILL.md",
                ".codex/skills/review-skill-security/SKILL.md",
                ".claude/skills/audit-web-quality/SKILL.md",
                ".claude/skills/review-skill-security/SKILL.md",
                ".codex/hooks.json",
                ".codex/hooks/session_start_ponytail.py",
                ".codex/agents/daily-project-auditor.toml",
                ".claude/agents/daily-project-auditor.md",
                ".claude/output-styles/pragmatic.md",
                ".github/codex/prompts/daily-project-health.md",
                ".github/workflows/daily-project-health.yml",
            ):
                self.assertTrue((target / relative_path).is_file(), relative_path)

            codex_config = tomllib.loads(
                (target / ".codex/config.toml").read_text(encoding="utf-8")
            )
            self.assertEqual(codex_config["model"], "gpt-5.6-sol")
            self.assertEqual(codex_config["model_reasoning_effort"], "medium")
            self.assertEqual(codex_config["personality"], "pragmatic")
            self.assertTrue(codex_config["features"]["hooks"])

            claude_settings = json.loads(
                (target / ".claude/settings.json").read_text(encoding="utf-8")
            )
            self.assertEqual(claude_settings["model"], "claude-fable-5")
            self.assertEqual(claude_settings["effortLevel"], "high")
            self.assertEqual(claude_settings["outputStyle"], "Pragmatic")
            self.assertEqual(
                claude_settings["permissions"]["defaultMode"], "bypassPermissions"
            )
            self.assertEqual(claude_settings["skillOverrides"]["caveman"], "off")
            self.assertIn("SessionStart", claude_settings["hooks"])

            hook = subprocess.run(
                [sys.executable, str(target / ".codex/hooks/session_start_ponytail.py")],
                input='{"hook_event_name":"SessionStart"}',
                text=True,
                capture_output=True,
                check=True,
            )
            hook_output = json.loads(hook.stdout)
            self.assertIn(
                "Ponytail Lite",
                hook_output["hookSpecificOutput"]["additionalContext"],
            )

            workflow = (target / ".github/workflows/daily-project-health.yml").read_text(
                encoding="utf-8"
            )
            self.assertIn("cron: \"17 3 * * *\"", workflow)
            self.assertIn("model: gpt-5.6-sol", workflow)
            self.assertIn("effort: high", workflow)
            self.assertIn("sandbox: read-only", workflow)

            mcp_config = json.loads(
                (target / ".mcp.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                mcp_config["mcpServers"]["existing"]["command"], "keep-me"
            )
            self.assertEqual(
                mcp_config["mcpServers"]["codebase-memory-mcp"]["command"],
                "codebase-memory-mcp",
            )
            self.assertIn(".mcp.json.bak", [path.name for path in first_report.backups])
            self.assertIn(".mcp.json", [path.name for path in second_report.skipped])
            self.assertTrue((target / "AGENTS.md.bak").is_file())


if __name__ == "__main__":
    unittest.main()
