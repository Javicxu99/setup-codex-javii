# Task Log

## 2026-08-31 - EU AI Act governance baseline 3.1

- Added the default/selectable `compliance` component, dated official source baseline,
  deterministic checker, conditional evidence, and manual Codex/Claude workflows.
- Kept the no-AI route minimal, source-code marking exception explicit, high-risk evidence
  inactive by default, critical unknowns fail-closed, and legal review outside automation.
- Added eight required scenarios plus milestone freshness and retained all bootstrap safety tests.
- Preserved provider separation, full trusted-repository autonomy, zero OpenAI API usage, and zero
  new runtime dependencies.

## 2026-08-31 - Safe bootstrap v3

- Replaced the API-key-backed scheduled audit with a manual, read-only Codex Desktop prompt.
- Made preview the default and added explicit apply, component selection, conflict preservation,
  preflight validation, atomic writes, and idempotent repeats.
- Raised the supported runtime to Python 3.11 and aligned PowerShell launcher diagnostics.
- Preserved full Codex and Claude autonomy for trusted personal repositories and strengthened
  automated provider-boundary checks.
- Validated with six standard-library tests, PowerShell syntax/JSON checks, and two complete
  launcher runs in a temporary repository; the second run produced 43 unchanged files and zero
  backups.
