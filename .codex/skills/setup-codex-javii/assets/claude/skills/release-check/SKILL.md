---
description: Run pre-release validation checklist: git status, CHANGELOG vs VERSION, script syntax, bootstrap test in tmp/, secrets scan, and GitHub templates check. Reports pass/fail per step.
---

# Release Check

Review this project before publishing a version. Run each step and report the result.

## Checklist

1. **Git status** - run `git status --short --branch`. No uncommitted changes should be present.

2. **CHANGELOG vs VERSION** - confirm the top entry in `CHANGELOG.md` matches `VERSION`.

3. **Script syntax** - run:
   ```
   python -m py_compile .codex/skills/setup-codex-javii/scripts/setup_codex_javii.py
   ```
   No output = passes.

4. **Bootstrap validation** - run the bootstrap in a temp folder:
   ```
   mkdir -p tmp/release-test && cd tmp/release-test && git init
   python ../../.codex/skills/setup-codex-javii/scripts/setup_codex_javii.py --profile default
   ```
   Verify: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/` are created.
   Run again to verify idempotence (`.bak` files created, no errors).

5. **Secrets check** - search for anything that should not be committed:
   ```
   rg -i "password|secret|token|api.key|private.key" --glob "!*.bak" --glob "!*.bak.*"
   ```

6. **GitHub templates** - confirm `.github/PULL_REQUEST_TEMPLATE.md` and issue templates are current.

7. **README** - confirm the "What It Generates" section matches actual bootstrap output.

## Output

Report: pass/fail per step, any blockers, release readiness summary.

Do not commit, tag, or push unless explicitly asked.
