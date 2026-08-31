#!/usr/bin/env python3
"""Deterministic EU AI Act governance gate for a project repository."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


COMPLIANCE_ROOT = Path("docs/compliance/eu-ai-act")
BASELINE_FILE = COMPLIANCE_ROOT / "legal-baseline.json"
INTAKE_FILE = COMPLIANCE_ROOT / "intake.json"

CLASSIFICATIONS = {
    "NOT_APPLICABLE",
    "BASELINE",
    "TRANSPARENCY_REQUIRED",
    "HIGH_RISK_REVIEW",
    "PROHIBITED_BLOCKED",
    "UNKNOWN_BLOCKED",
}
ROLES = {
    "provider",
    "deployer",
    "importer",
    "distributor",
    "manufacturer",
    "other",
}
CONTROL_STATES = {"not_applicable", "present", "missing", "transition", "unknown"}
RESULT_RANK = {"PASS": 0, "WARNING": 1, "LEGAL_REVIEW_REQUIRED": 2, "BLOCKED": 3}
EXIT_CODES = {"PASS": 0, "WARNING": 1, "LEGAL_REVIEW_REQUIRED": 2, "BLOCKED": 3}


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


@dataclass
class Evaluation:
    classification: str = "UNKNOWN_BLOCKED"
    findings: list[Finding] = field(default_factory=list)

    def add(self, level: str, code: str, message: str) -> None:
        self.findings.append(Finding(level, code, message))

    @property
    def result(self) -> str:
        if not self.findings:
            return "PASS"
        return max(self.findings, key=lambda item: RESULT_RANK[item.level]).level


def parse_date(value: Any, label: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must use YYYY-MM-DD: {value!r}") from exc


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ValueError(f"required file is missing: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value must be an object: {path}")
    return value


def require_mapping(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def require_boolean(mapping: dict[str, Any], key: str, unknowns: list[str]) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        unknowns.append(key)
        return False
    return value


def require_control(mapping: dict[str, Any], key: str, unknowns: list[str]) -> str:
    value = mapping.get(key)
    if value not in CONTROL_STATES:
        unknowns.append(key)
        return "unknown"
    if value == "unknown":
        unknowns.append(key)
    return value


def has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().upper() != "UNSET"


def evidence_exists(project_root: Path, value: Any) -> bool:
    if not has_text(value):
        return False
    candidate = Path(str(value))
    if candidate.is_absolute():
        return False
    resolved_root = project_root.resolve()
    resolved_candidate = (resolved_root / candidate).resolve()
    if not resolved_candidate.is_relative_to(resolved_root):
        return False
    return resolved_candidate.is_file() and resolved_candidate.stat().st_size > 0


def evaluate_baseline(
    baseline: dict[str, Any], evaluation_date: date, evaluation: Evaluation
) -> None:
    baseline_date = parse_date(baseline.get("as_of"), "legal baseline as_of")
    next_review = parse_date(baseline.get("next_review_on"), "legal baseline next_review_on")
    if evaluation_date > next_review or (evaluation_date - baseline_date).days > 90:
        evaluation.add(
            "WARNING",
            "BASELINE_STALE",
            f"Legal baseline dated {baseline_date} must be refreshed; next review was {next_review}.",
        )

    milestones = baseline.get("milestones")
    if not isinstance(milestones, list):
        raise ValueError("legal baseline milestones must be an array")
    for index, milestone in enumerate(milestones):
        if not isinstance(milestone, dict):
            raise ValueError(f"legal baseline milestone {index} must be an object")
        effective_on = parse_date(
            milestone.get("effective_on"), f"legal baseline milestone {index} effective_on"
        )
        if (
            milestone.get("refresh_required") is True
            and evaluation_date >= effective_on
            and baseline_date < effective_on
        ):
            evaluation.add(
                "WARNING",
                "LEGAL_MILESTONE_REACHED",
                f"Refresh the baseline for milestone {effective_on}: {milestone.get('summary', 'unnamed milestone')}.",
            )


def evaluate_intake(
    project_root: Path,
    intake: dict[str, Any],
    evaluation_date: date,
    evaluation: Evaluation,
) -> None:
    assessment = require_mapping(intake, "assessment")
    decision = require_mapping(intake, "decision")

    missing_assessment = [
        key
        for key in ("owner", "assessed_on", "intended_purpose", "context")
        if not has_text(assessment.get(key))
    ]
    try:
        parse_date(assessment.get("assessed_on"), "assessment assessed_on")
    except ValueError:
        if "assessed_on" not in missing_assessment:
            missing_assessment.append("assessed_on")
    if missing_assessment:
        evaluation.add(
            "BLOCKED",
            "ASSESSMENT_INCOMPLETE",
            "Complete assessment fields: " + ", ".join(sorted(missing_assessment)) + ".",
        )

    ai_system = assessment.get("ai_system")
    if ai_system not in {"yes", "no"}:
        evaluation.classification = "UNKNOWN_BLOCKED"
        evaluation.add(
            "BLOCKED",
            "AI_SYSTEM_UNKNOWN",
            "Decide whether the project contains or deploys an AI system under Article 3(1).",
        )
        check_decision(decision, evaluation)
        return

    if ai_system == "no":
        evaluation.classification = "NOT_APPLICABLE"
        check_decision(decision, evaluation)
        return

    eu_scope = assessment.get("eu_scope")
    role = assessment.get("role")
    if eu_scope not in {"yes", "no"}:
        evaluation.classification = "UNKNOWN_BLOCKED"
        evaluation.add(
            "BLOCKED",
            "EU_SCOPE_UNKNOWN",
            "Determine whether the system, operator, output, or affected persons are within EU scope.",
        )
        check_decision(decision, evaluation)
        return
    if role not in ROLES:
        evaluation.classification = "UNKNOWN_BLOCKED"
        evaluation.add(
            "BLOCKED",
            "ROLE_UNKNOWN",
            "Record the operator role: provider, deployer, importer, distributor, manufacturer, or other.",
        )
        check_decision(decision, evaluation)
        return

    personal = assessment.get("personal_non_professional") is True
    research_only = assessment.get("pre_market_research_only") is True
    real_world_testing = assessment.get("real_world_testing") is True
    if eu_scope == "no" or (role == "deployer" and personal) or (
        research_only and not real_world_testing
    ):
        evaluation.classification = "NOT_APPLICABLE"
        check_decision(decision, evaluation)
        return

    risk = require_mapping(intake, "risk_signals")
    transparency = require_mapping(intake, "transparency")
    unknowns = list(intake.get("critical_unknowns", [])) if isinstance(
        intake.get("critical_unknowns"), list
    ) else ["critical_unknowns"]

    current_prohibited = require_boolean(risk, "current_prohibited_practice", unknowns)
    workplace_emotion = require_boolean(
        risk, "workplace_emotion_recognition", unknowns
    )
    medical_safety_exception = require_boolean(
        risk, "medical_or_safety_exception", unknowns
    )
    intimate_content = require_boolean(
        risk, "nonconsensual_intimate_synthetic_content", unknowns
    )
    child_abuse_material = require_boolean(
        risk, "child_sexual_abuse_material", unknowns
    )
    annex_i = require_boolean(risk, "high_risk_annex_i", unknowns)
    annex_iii = require_boolean(risk, "high_risk_annex_iii", unknowns)
    cv_screening = require_boolean(risk, "employment_cv_screening", unknowns)
    gpai_provider = require_boolean(risk, "gpai_model_provider", unknowns)

    direct_interaction = require_boolean(transparency, "direct_interaction", unknowns)
    obvious_interaction = require_boolean(transparency, "interaction_is_obvious", unknowns)
    synthetic_content = require_boolean(
        transparency, "generates_synthetic_content", unknowns
    )
    source_code_only = require_boolean(transparency, "source_code_only", unknowns)
    emotion_recognition = require_boolean(transparency, "emotion_recognition", unknowns)
    biometric_categorisation = require_boolean(
        transparency, "biometric_categorisation", unknowns
    )
    deepfake = require_boolean(transparency, "deepfake", unknowns)
    public_interest_text = require_boolean(
        transparency, "public_interest_text", unknowns
    )
    human_review = require_boolean(
        transparency, "substantive_human_review", unknowns
    )
    editorial_responsibility = require_boolean(
        transparency, "editorial_responsibility", unknowns
    )
    pre_august_market = require_boolean(
        transparency, "placed_on_market_before_2026_08_02", unknowns
    )

    first_notice = require_control(
        transparency, "first_interaction_notice", unknowns
    )
    machine_marking = require_control(
        transparency, "provider_machine_readable_marking", unknowns
    )
    people_notice = require_control(transparency, "people_notice", unknowns)
    deepfake_label = require_control(transparency, "deepfake_label", unknowns)
    public_text_label = require_control(
        transparency, "public_interest_text_label", unknowns
    )

    cleaned_unknowns = sorted({str(item).strip() for item in unknowns if str(item).strip()})
    if cleaned_unknowns:
        evaluation.classification = "UNKNOWN_BLOCKED"
        evaluation.add(
            "BLOCKED",
            "CRITICAL_FACTS_UNKNOWN",
            "Resolve critical facts: " + ", ".join(cleaned_unknowns) + ".",
        )
        check_decision(decision, evaluation)
        return

    if current_prohibited or (workplace_emotion and not medical_safety_exception):
        evaluation.classification = "PROHIBITED_BLOCKED"
        evaluation.add(
            "BLOCKED",
            "PROHIBITED_PRACTICE",
            "A currently prohibited practice is indicated. Stop release and obtain legal review.",
        )
        check_decision(decision, evaluation)
        return

    if intimate_content or child_abuse_material:
        if evaluation_date >= date(2026, 12, 2):
            evaluation.classification = "PROHIBITED_BLOCKED"
            evaluation.add(
                "BLOCKED",
                "2026_PROHIBITION_ACTIVE",
                "A prohibition applicable from 2026-12-02 is indicated. Stop release.",
            )
            check_decision(decision, evaluation)
            return
        evaluation.add(
            "LEGAL_REVIEW_REQUIRED",
            "2026_PROHIBITION_PENDING",
            "A new prohibition takes effect on 2026-12-02; other law may already apply. Obtain legal review.",
        )

    high_risk = annex_i or annex_iii or cv_screening
    transparency_required = False

    if direct_interaction and not obvious_interaction:
        transparency_required = True
        if first_notice != "present":
            evaluation.add(
                "BLOCKED",
                "FIRST_INTERACTION_NOTICE_MISSING",
                "Provide clear, distinguishable, accessible notice at the first interaction.",
            )

    if role == "provider" and synthetic_content and not source_code_only:
        transparency_required = True
        transition_available = (
            pre_august_market
            and evaluation_date < date(2026, 12, 2)
            and machine_marking == "transition"
        )
        if transition_available:
            evaluation.add(
                "WARNING",
                "ARTICLE_50_2_TRANSITION",
                "Limited Article 50(2) transition ends on 2026-12-02.",
            )
        elif machine_marking != "present":
            evaluation.add(
                "BLOCKED",
                "MACHINE_MARKING_MISSING",
                "Provider evidence of machine-readable marking is missing.",
            )

    if role == "deployer" and (emotion_recognition or biometric_categorisation):
        transparency_required = True
        if people_notice != "present":
            evaluation.add(
                "BLOCKED",
                "EXPOSED_PEOPLE_NOTICE_MISSING",
                "People exposed to emotion recognition or biometric categorisation must be informed.",
            )

    if deepfake:
        transparency_required = True
        if deepfake_label != "present":
            evaluation.add(
                "BLOCKED",
                "DEEPFAKE_LABEL_MISSING",
                "Clear deepfake labelling evidence is missing.",
            )

    if public_interest_text:
        transparency_required = True
        editorial_exception = human_review and editorial_responsibility
        if not editorial_exception and public_text_label != "present":
            evaluation.add(
                "BLOCKED",
                "PUBLIC_INTEREST_TEXT_LABEL_MISSING",
                "Label public-interest AI text or document substantive review and editorial responsibility.",
            )

    if high_risk:
        evaluation.classification = "HIGH_RISK_REVIEW"
        evaluation.add(
            "LEGAL_REVIEW_REQUIRED",
            "HIGH_RISK_REVIEW",
            "Potential Annex I/III high-risk use requires human legal review and the incremental high-risk file.",
        )
    elif transparency_required:
        evaluation.classification = "TRANSPARENCY_REQUIRED"
    else:
        evaluation.classification = "BASELINE"

    if gpai_provider:
        evaluation.add(
            "LEGAL_REVIEW_REQUIRED",
            "GPAI_PROVIDER_REVIEW",
            "The project indicates that it is a GPAI model provider; downstream use alone does not establish this role.",
        )

    evidence = require_mapping(intake, "evidence")
    required_evidence = ["controls", "release", "ai_literacy", "third_party"]
    if transparency_required:
        required_evidence.append("transparency")
    if high_risk:
        required_evidence.append("high_risk")
    if gpai_provider or evaluation.result == "LEGAL_REVIEW_REQUIRED":
        required_evidence.append("legal_review")
    missing_evidence = [
        key for key in required_evidence if not evidence_exists(project_root, evidence.get(key))
    ]
    if missing_evidence:
        evaluation.add(
            "BLOCKED",
            "EVIDENCE_MISSING",
            "Missing or invalid in-repository evidence: "
            + ", ".join(sorted(set(missing_evidence)))
            + ".",
        )

    check_decision(decision, evaluation)


def check_decision(decision: dict[str, Any], evaluation: Evaluation) -> None:
    declared = decision.get("declared_status")
    if declared not in CLASSIFICATIONS:
        evaluation.add(
            "BLOCKED",
            "DECISION_STATUS_INVALID",
            "decision.declared_status must contain a supported classification.",
        )
    elif declared != evaluation.classification:
        evaluation.add(
            "BLOCKED",
            "DECISION_STATUS_MISMATCH",
            f"Declared {declared}, but deterministic classification is {evaluation.classification}.",
        )
    missing = [
        key for key in ("rationale", "reviewed_on", "approved_by") if not has_text(decision.get(key))
    ]
    try:
        parse_date(decision.get("reviewed_on"), "decision reviewed_on")
    except ValueError:
        if "reviewed_on" not in missing:
            missing.append("reviewed_on")
    if missing:
        evaluation.add(
            "BLOCKED",
            "DECISION_EVIDENCE_INCOMPLETE",
            "Complete decision fields: " + ", ".join(sorted(missing)) + ".",
        )


def evaluate(project_root: Path, evaluation_date: date) -> Evaluation:
    evaluation = Evaluation()
    try:
        baseline = load_json(project_root / BASELINE_FILE)
        intake = load_json(project_root / INTAKE_FILE)
        evaluate_baseline(baseline, evaluation_date, evaluation)
        evaluate_intake(project_root, intake, evaluation_date, evaluation)
    except ValueError as exc:
        evaluation.classification = "UNKNOWN_BLOCKED"
        evaluation.add("BLOCKED", "INVALID_COMPLIANCE_DATA", str(exc))
    if not evaluation.findings:
        evaluation.add(
            "PASS",
            "CLASSIFICATION_VERIFIED",
            "Classification and required evidence are complete for this deterministic gate.",
        )
    return evaluation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check documented EU AI Act classification and release evidence."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root.")
    parser.add_argument(
        "--as-of-date",
        type=date.fromisoformat,
        default=date.today(),
        help="Evaluation date in YYYY-MM-DD form (default: today).",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = args.root.resolve()
    evaluation = evaluate(project_root, args.as_of_date)
    if args.json:
        print(
            json.dumps(
                {
                    "classification": evaluation.classification,
                    "result": evaluation.result,
                    "exit_code": EXIT_CODES[evaluation.result],
                    "evaluation_date": args.as_of_date.isoformat(),
                    "findings": [finding.__dict__ for finding in evaluation.findings],
                },
                indent=2,
            )
        )
    else:
        print(f"CLASSIFICATION: {evaluation.classification}")
        print(f"RESULT: {evaluation.result}")
        for finding in evaluation.findings:
            print(f"{finding.level}: {finding.code}: {finding.message}")
    return EXIT_CODES[evaluation.result]


if __name__ == "__main__":
    raise SystemExit(main())
