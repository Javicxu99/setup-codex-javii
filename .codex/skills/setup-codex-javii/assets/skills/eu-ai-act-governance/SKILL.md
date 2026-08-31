---
name: eu-ai-act-governance
description: Complete or refresh the repository's EU AI Act intake, classification, controls, and release evidence when AI applicability or governance must be assessed. Do not use as legal certification.
---

# EU AI Act Governance

Read `docs/compliance/eu-ai-act/README.md`, `legal-baseline.json`, and `intake.json` before acting.

## Intake mode

Inspect the actual intended purpose and repository evidence. Record AI-system status, EU scope,
operator role, prohibited-practice signals, transparency triggers, high-risk/GPAI signals, and
critical unknowns. Do not guess a material fact; unresolved facts must remain fail-closed. Keep
controls proportional and activate `high-risk/README.md` only for `HIGH_RISK_REVIEW`.

## Source-refresh mode

Use only the official URLs already listed in `legal-baseline.json` as legal authority. Update the
dated baseline, milestones, and evidence when official sources change. A secondary article may be
a discovery lead but never overrides the Regulation, Commission guidance, or parliamentary status.

## Finish

Run `python scripts/check_eu_ai_act.py --root .` and report its classification, result, exit code,
evidence, and unresolved issues. Never promise automatic compliance, legal advice, certification,
conformity assessment, or CE marking. Require qualified human/legal review for prohibited or
possible high-risk uses, biometrics, employment, health, minors, fundamental-rights impacts, GPAI
provider status, role changes, and material uncertainty.
