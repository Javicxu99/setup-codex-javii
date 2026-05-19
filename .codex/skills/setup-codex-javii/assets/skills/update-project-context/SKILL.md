---
name: update-project-context
description: Update living project documentation after important changes. Use when the objective, architecture, main workflow, technical decisions, or relevant validations change.
---

# update-project-context

Use after important changes.

## Procedure

1. Update `docs/project-context.md` if any of these changed:
   - objective
   - scope
   - architecture
   - inputs or outputs
   - deployment
   - risks
   - current status
2. Update `docs/task-log.md` with:
   - date
   - change made
   - decision taken
   - validation run
   - remaining risks
3. Update `docs/codex-session-notes.md` when a Codex conversation created reusable context, decisions, operating assumptions, follow-ups, or risks.
4. Update `docs/codegraph.md` only if the project's CodeGraph workflow or local graph assumptions changed.
5. Update `CHANGELOG.md` when the change affects behavior, compatibility, release notes, or user-facing setup.
6. Keep entries brief and traceable.

## Rule

Do not invent unvalidated results. If a validation was not run, say so explicitly. Do not paste raw secrets or unreviewed transcripts into tracked docs.
