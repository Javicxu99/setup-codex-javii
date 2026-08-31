---
name: eu-ai-act-governance
description: Complete or refresh EU AI Act intake, classification, controls, and release evidence. Use for project AI-governance assessment, not legal certification.
---

# EU AI Act Governance

Read `docs/compliance/eu-ai-act/README.md`, `legal-baseline.json`, and `intake.json` first.

For intake, inspect actual intended purpose and evidence; record AI-system status, EU scope, role,
prohibited-practice signals, transparency triggers, high-risk/GPAI signals, and unknowns. Never
guess a material fact. Keep controls proportional and activate the high-risk template only for
`HIGH_RISK_REVIEW`.

For a source refresh, use only official URLs listed in `legal-baseline.json` as authority. Do not
turn a secondary article or pending national bill into binding law.

Run `python scripts/check_eu_ai_act.py --root .` and report its exact classification, result, exit
code, evidence, and unresolved issues. Never claim legal advice, certification, conformity, CE
marking, or automatic compliance. Escalate prohibited or possible high-risk uses, biometrics,
employment, health, minors, fundamental rights, GPAI-provider status, role changes, and material
uncertainty to qualified human/legal review.
