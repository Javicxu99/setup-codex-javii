# EU AI Act control record

- Project: setup-codex-javii
- Classification: `BASELINE`
- Evidence date: 2026-08-31
- Owner: Javier

## Risk and prohibited practices

The intended purpose is repository development with third-party coding assistants. The project
does not implement emotion recognition, biometric categorisation, employment screening, social
scoring, manipulative targeting, non-consensual intimate synthetic content, or child sexual abuse
material. Reassess before adding any such capability or changing intended purpose.

## Privacy and data governance

Do not enter secrets, protected personal data, or confidential third-party material into an AI
tool without an authorised basis and appropriate controls. The bootstrap keeps local secret files
out of generated context and does not store provider credentials.

## Human oversight

AI-assisted changes receive human review through diffs, tests, release evidence, and pull
requests. Outputs are not accepted as legal conclusions or proof of correctness.

## Transparency and editorial review

No public-facing AI interaction, emotion recognition, biometric categorisation, deepfake, or
public-interest publication is part of the intended purpose. Source code generated with a coding
assistant is outside Article 50's marking obligation according to the Commission FAQ. This does
not exempt other output types or future product features.

## Third-party providers and models

Codex and Claude Code are third-party assistants. This repository acts as a deployer/integrator,
not as provider of their underlying GPAI models. Provider terms, model changes, data handling,
instructions, and transparency capabilities require review when the tool or intended use changes.

## AI literacy

Maintainers review the intended purpose, provider role, hallucination/error risk, data handling,
human review, prohibited practices, transparency triggers, and escalation paths. This dated record
documents guidance; it is not a certificate and does not guarantee a particular literacy level.

## Incidents and substantial changes

Record harmful or unexpected behavior, affected people, containment, evidence, provider contact,
and corrective action in the project issue/task log. Re-run intake after rebranding, substantial
modification, new data or users, a new sector, real-world testing, or a changed intended purpose.

## Release evidence

The release gate is recorded in `release-evidence.md`. High-risk preparation remains inactive;
if classification becomes `HIGH_RISK_REVIEW`, complete `high-risk/README.md` and obtain qualified
human/legal review before release.
