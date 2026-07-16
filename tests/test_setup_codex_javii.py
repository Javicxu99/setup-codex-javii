from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
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
    def test_generates_quality_skills_and_merges_bom_mcp_config(self) -> None:
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
            ):
                self.assertTrue((target / relative_path).is_file(), relative_path)

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
