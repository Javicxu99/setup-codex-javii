from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "scripts" / "run_archify.py"
RUNTIME = REPO_ROOT / "third_party" / "archify"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_archify", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import Archify runner: {RUNNER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_archify(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=cwd or REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ArchifyIntegrationTests(unittest.TestCase):
    def test_doctor_validate_deliver_and_demo_use_the_vendored_runtime(self) -> None:
        doctor = run_archify("doctor")
        self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
        self.assertIn("Archify is ready.", doctor.stdout)

        example = RUNTIME / "examples/web-app.architecture.json"
        validated = run_archify(
            "validate", "architecture", str(example), "--quality", "showcase", "--json"
        )
        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
        self.assertIn('"status": "pass"', validated.stdout)
        self.assertIn('"errors": 0', validated.stdout)
        self.assertIn('"warnings": 0', validated.stdout)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory)
            delivered = output_root / "delivered.html"
            receipt = run_archify(
                "deliver",
                "architecture",
                str(example),
                str(delivered),
                "--quality",
                "showcase",
                "--json",
                cwd=output_root,
            )
            self.assertEqual(receipt.returncode, 0, receipt.stdout + receipt.stderr)
            self.assertTrue(delivered.is_file())
            self.assertGreater(delivered.stat().st_size, 100_000)
            self.assertIn('"ok": true', receipt.stdout)

            demo = run_archify("demo", str(output_root / "demo"), cwd=output_root)
            self.assertEqual(demo.returncode, 0, demo.stdout + demo.stderr)
            self.assertTrue((output_root / "demo/archify-demo.html").is_file())

    def test_skill_frontmatter_activation_and_relative_resources_are_valid(self) -> None:
        skill_paths = (
            REPO_ROOT / ".codex/skills/archify/SKILL.md",
            REPO_ROOT / ".codex/skills/setup-codex-javii/assets/skills/archify/SKILL.md",
            REPO_ROOT / ".claude/skills/archify/SKILL.md",
            REPO_ROOT / ".claude/bootstrap-assets/skills/archify/SKILL.md",
        )
        for path in skill_paths:
            text = path.read_text(encoding="utf-8")
            frontmatter = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            self.assertIsNotNone(frontmatter, path)
            self.assertRegex(frontmatter.group(1), r"(?m)^name: archify$")
            self.assertRegex(frontmatter.group(1), r"(?m)^description: .+")
            self.assertIn("python scripts/run_archify.py doctor", text)
            self.assertIn("third_party/archify", text)
            self.assertNotIn("check-update.mjs", text)

        self.assertEqual(skill_paths[0].read_bytes(), skill_paths[1].read_bytes())
        self.assertEqual(skill_paths[2].read_bytes(), skill_paths[3].read_bytes())
        for relative in (
            "schemas/common.schema.json",
            "schemas/architecture.schema.json",
            "examples/web-app.architecture.json",
            "references/authoring-contract.md",
            "references/delivery-contract.md",
            "references/viewer-runtime.md",
            "LICENSE",
        ):
            self.assertTrue((RUNTIME / relative).is_file(), relative)

    def test_offline_default_and_optional_node_error_are_explicit(self) -> None:
        self.assertFalse((RUNTIME / "scripts/check-update.mjs").exists())
        self.assertFalse((RUNTIME / "skill-release.json").exists())
        template = (RUNTIME / "assets/template.html").read_text(encoding="utf-8")
        self.assertNotIn("fonts.googleapis.com", template)
        self.assertNotIn("fonts.gstatic.com", template)

        module = load_runner_module()
        with mock.patch.dict(
            os.environ,
            {"ARCHIFY_NODE": "missing-node-for-archify", "PATH": ""},
            clear=False,
        ):
            with self.assertRaisesRegex(
                RuntimeError, "requires optional Node.js 18 or newer"
            ):
                module.resolve_node()

    def test_all_vendored_javascript_parses(self) -> None:
        module = load_runner_module()
        node, _version = module.resolve_node()
        scripts = sorted(RUNTIME.rglob("*.mjs"))
        self.assertGreater(len(scripts), 30)
        for script in scripts:
            checked = subprocess.run(
                [node, "--check", str(script)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, f"{script}: {checked.stderr}")


if __name__ == "__main__":
    unittest.main()
