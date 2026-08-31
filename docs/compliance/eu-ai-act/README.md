# EU AI Act governance baseline

This directory provides a dated, evidence-oriented release gate. It helps a project classify its
AI use, record controls, and escalate uncertainty. It does **not** provide legal advice, certify a
system, or guarantee compliance.

## Release route

1. Complete `intake.json` using the system's actual intended purpose, EU scope, operator role,
   transparency facts, risk signals, and critical unknowns.
2. Record proportionate evidence in `controls.md` and `release-evidence.md`.
3. Run `python scripts/check_eu_ai_act.py --root .`.
4. Do not release on `BLOCKED` or `LEGAL_REVIEW_REQUIRED`. Resolve `WARNING` findings and record
   why release remains appropriate.
5. Refresh `legal-baseline.json` from its official sources at least every 90 days and whenever a
   recorded milestone is reached.

Exit codes are `0` PASS, `1` WARNING, `2` LEGAL_REVIEW_REQUIRED, and `3` BLOCKED.

## Classification boundaries

- `NOT_APPLICABLE`: no AI system, no EU scope, qualifying strictly personal non-professional use,
  or qualifying pre-market research that is not testing in real conditions.
- `BASELINE`: AI is in scope but the recorded facts do not trigger the specific categories below.
- `TRANSPARENCY_REQUIRED`: Article 50 controls apply and require recorded implementation evidence.
- `HIGH_RISK_REVIEW`: Annex I/III or equivalent signals require legal review and the incremental
  `high-risk/README.md` evidence file. This tool does not perform conformity assessment.
- `PROHIBITED_BLOCKED`: a currently prohibited practice is indicated; stop the release.
- `UNKNOWN_BLOCKED`: a fact needed for classification is unknown or invalid; fail closed.

Using Codex or another assistant to generate source code does not by itself require marking that
code under Article 50. The Commission FAQ lists source code outside the marking obligation. Other
outputs and uses still require their own assessment.

Role and intended purpose control the analysis. Integrating or using a third-party model does not
automatically make the project a provider of that model. Rebranding, substantial modification, or
changing intended purpose can change the role and must trigger reassessment.

## Proportionality and other law

For a project without AI, keep the documented `NOT_APPLICABLE` intake and no further AI-specific
control set. For ordinary coding-assistant use, keep a small `BASELINE` record. Activate the
high-risk evidence only for `HIGH_RISK_REVIEW`.

The AI Act does not replace GDPR/privacy, consumer, product-safety, intellectual-property,
accessibility, employment, cybersecurity, or sector-specific duties. Open-source licensing does
not remove prohibited-practice, Article 50, or high-risk obligations. Escalate biometrics,
employment, health, minors, fundamental-rights impacts, high risk, and unresolved role or scope
questions to qualified human/legal review.

## Official authority

The machine-readable source register and application milestones are in `legal-baseline.json`.
The primary authority is the consolidated Regulation (EU) 2024/1689 as of 2026-07-27, including
Regulation (EU) 2026/1744. The Spanish initiative 121/000096 was still a bill in the parliamentary
amendment stage on 2026-08-31 and is not encoded as enacted national law.
