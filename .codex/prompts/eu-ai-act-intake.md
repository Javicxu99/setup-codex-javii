# EU AI Act intake and evidence review

Read `docs/compliance/eu-ai-act/README.md`, `legal-baseline.json`, and `intake.json`. Inspect the
repository and its documented intended purpose before proposing changes.

Help complete the intake with evidence-backed facts: AI-system definition, EU scope, intended
purpose and context, operator role, prohibited-practice signals, Article 50 transparency triggers,
possible Annex I/III high risk, GPAI-provider status, and critical unknowns. Do not infer a safe
answer when a material fact is unknown. Keep unrelated control sets inactive.

Update `controls.md`, `release-evidence.md`, and `high-risk/README.md` only as the resulting
classification requires. Run `python scripts/check_eu_ai_act.py --root .` and report the exact
classification, result, exit code, evidence, and unresolved questions.

This is governance support, not legal advice or certification. Escalate prohibited practices,
high risk, biometrics, employment, health, minors, fundamental-rights impacts, and material doubt
to qualified human/legal review. When refreshing law, use the official URLs recorded in
`legal-baseline.json`; never treat a secondary article or pending national bill as enacted law.
