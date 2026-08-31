from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_eu_ai_act.py"
BASELINE = REPO_ROOT / "docs" / "compliance" / "eu-ai-act" / "legal-baseline.json"


def load_checker_module():
    spec = importlib.util.spec_from_file_location("check_eu_ai_act", CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import checker: {CHECKER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def complete_intake(status: str = "BASELINE") -> dict[str, object]:
    return {
        "schema_version": 1,
        "assessment": {
            "owner": "Test owner",
            "assessed_on": "2026-08-31",
            "ai_system": "yes",
            "eu_scope": "yes",
            "intended_purpose": "Deterministic test scenario",
            "context": "EU test deployment",
            "role": "deployer",
            "personal_non_professional": False,
            "pre_market_research_only": False,
            "real_world_testing": False,
        },
        "risk_signals": {
            "current_prohibited_practice": False,
            "workplace_emotion_recognition": False,
            "medical_or_safety_exception": False,
            "nonconsensual_intimate_synthetic_content": False,
            "child_sexual_abuse_material": False,
            "high_risk_annex_i": False,
            "high_risk_annex_iii": False,
            "employment_cv_screening": False,
            "gpai_model_provider": False,
        },
        "transparency": {
            "direct_interaction": False,
            "interaction_is_obvious": False,
            "first_interaction_notice": "not_applicable",
            "generates_synthetic_content": False,
            "provider_machine_readable_marking": "not_applicable",
            "source_code_only": False,
            "placed_on_market_before_2026_08_02": False,
            "emotion_recognition": False,
            "biometric_categorisation": False,
            "people_notice": "not_applicable",
            "deepfake": False,
            "deepfake_label": "not_applicable",
            "public_interest_text": False,
            "substantive_human_review": False,
            "editorial_responsibility": False,
            "public_interest_text_label": "not_applicable",
        },
        "critical_unknowns": [],
        "evidence": {
            "controls": "docs/compliance/eu-ai-act/controls.md",
            "release": "docs/compliance/eu-ai-act/release-evidence.md",
            "ai_literacy": "docs/compliance/eu-ai-act/ai-literacy.md",
            "third_party": "docs/compliance/eu-ai-act/third-party.md",
            "transparency": "docs/compliance/eu-ai-act/transparency.md",
            "high_risk": "docs/compliance/eu-ai-act/high-risk/README.md",
            "legal_review": "docs/compliance/eu-ai-act/legal-review.md",
        },
        "decision": {
            "declared_status": status,
            "rationale": "Scenario classification reviewed for a deterministic test.",
            "reviewed_on": "2026-08-31",
            "approved_by": "Test owner",
        },
    }


class ComplianceCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_checker_module()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        compliance = self.root / "docs" / "compliance" / "eu-ai-act"
        compliance.mkdir(parents=True)
        shutil.copy2(BASELINE, compliance / "legal-baseline.json")
        for relative in (
            "controls.md",
            "release-evidence.md",
            "ai-literacy.md",
            "third-party.md",
            "transparency.md",
            "high-risk/README.md",
            "legal-review.md",
        ):
            path = compliance / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"Evidence for {relative}\n", encoding="utf-8")

    def evaluate(self, intake: dict[str, object], on: date = date(2026, 8, 31)):
        path = self.root / "docs" / "compliance" / "eu-ai-act" / "intake.json"
        path.write_text(json.dumps(intake, indent=2) + "\n", encoding="utf-8")
        return self.module.evaluate(self.root, on)

    def test_project_without_ai_is_not_applicable(self) -> None:
        intake = complete_intake("NOT_APPLICABLE")
        intake["assessment"]["ai_system"] = "no"  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "NOT_APPLICABLE")
        self.assertEqual(result.result, "PASS")

    def test_coding_assistant_is_baseline_and_source_code_needs_no_marking(self) -> None:
        intake = complete_intake("BASELINE")
        intake["assessment"]["role"] = "deployer"  # type: ignore[index]
        intake["transparency"]["generates_synthetic_content"] = True  # type: ignore[index]
        intake["transparency"]["source_code_only"] = True  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "BASELINE")
        self.assertEqual(result.result, "PASS")
        self.assertNotIn("MACHINE_MARKING_MISSING", {item.code for item in result.findings})

    def test_public_chatbot_requires_first_interaction_notice(self) -> None:
        intake = complete_intake("TRANSPARENCY_REQUIRED")
        intake["assessment"]["role"] = "provider"  # type: ignore[index]
        intake["transparency"]["direct_interaction"] = True  # type: ignore[index]
        intake["transparency"]["first_interaction_notice"] = "present"  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "TRANSPARENCY_REQUIRED")
        self.assertEqual(result.result, "PASS")

        intake["transparency"]["first_interaction_notice"] = "missing"  # type: ignore[index]
        blocked = self.evaluate(intake)
        self.assertEqual(blocked.result, "BLOCKED")
        self.assertIn(
            "FIRST_INTERACTION_NOTICE_MISSING", {item.code for item in blocked.findings}
        )

    def test_deepfake_requires_label_evidence(self) -> None:
        intake = complete_intake("TRANSPARENCY_REQUIRED")
        intake["transparency"]["deepfake"] = True  # type: ignore[index]
        intake["transparency"]["deepfake_label"] = "present"  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "TRANSPARENCY_REQUIRED")
        self.assertEqual(result.result, "PASS")

    def test_cv_screening_requires_high_risk_legal_review(self) -> None:
        intake = complete_intake("HIGH_RISK_REVIEW")
        intake["risk_signals"]["employment_cv_screening"] = True  # type: ignore[index]
        intake["risk_signals"]["high_risk_annex_iii"] = True  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "HIGH_RISK_REVIEW")
        self.assertEqual(result.result, "LEGAL_REVIEW_REQUIRED")
        self.assertEqual(self.module.EXIT_CODES[result.result], 2)

    def test_workplace_emotion_recognition_is_prohibited(self) -> None:
        intake = complete_intake("PROHIBITED_BLOCKED")
        intake["risk_signals"]["workplace_emotion_recognition"] = True  # type: ignore[index]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "PROHIBITED_BLOCKED")
        self.assertEqual(result.result, "BLOCKED")

    def test_critical_unknown_fails_closed(self) -> None:
        intake = complete_intake("UNKNOWN_BLOCKED")
        intake["critical_unknowns"] = ["Whether biometric categorisation is enabled"]
        result = self.evaluate(intake)
        self.assertEqual(result.classification, "UNKNOWN_BLOCKED")
        self.assertEqual(result.result, "BLOCKED")

    def test_reached_legal_milestone_warns_until_baseline_refresh(self) -> None:
        intake = complete_intake("BASELINE")
        result = self.evaluate(intake, date(2026, 12, 2))
        self.assertEqual(result.classification, "BASELINE")
        self.assertEqual(result.result, "WARNING")
        self.assertIn("LEGAL_MILESTONE_REACHED", {item.code for item in result.findings})


if __name__ == "__main__":
    unittest.main()
