---
description: Run the Claude-side pre-release checklist: git state, settings, hooks, agents, skills, secrets, and documentation. Reports pass/fail per step.
---

# Release Check

Review this project before publishing a version. Run each step and report the result.

## Checklist

1. **Git status** - run `git status --short --branch`. No uncommitted changes should be present.

2. **CHANGELOG vs VERSION** - confirm the top entry in `CHANGELOG.md` matches `VERSION`.

3. **Claude hook syntax** - run:
   ```
   python -m py_compile .claude/hooks/session_start_ponytail.py
   ```
   No output = passes.

4. **Claude configuration** - parse `.claude/settings.json` as JSON and verify that
   `CLAUDE.md`, `.claude/agents/`, `.claude/hooks/`, `.claude/output-styles/`, and
   `.claude/skills/` are internally consistent. Confirm that no foreign-provider model
   identifier appears anywhere under `.claude/`.

5. **Secrets check** - search for anything that should not be committed:
   ```
   rg -i "password|secret|token|api.key|private.key" --glob "!*.bak" --glob "!*.bak.*"
   ```

6. **GitHub templates** - confirm `.github/PULL_REQUEST_TEMPLATE.md` and issue templates are current.

7. **README** - confirm the "What It Generates" section matches actual bootstrap output.

## Output

Report: pass/fail per step, any blockers, release readiness summary.

Do not commit, tag, or push unless explicitly asked.
