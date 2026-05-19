---
name: project-orientation
description: Orient before an important Codex project task. Use to read context, identify the affected layer, summarize constraints, relevant files, risks, and possible validations without modifying code.
---

# project-orientation

Use at the start of an important task.

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/project-context.md`.
3. Read `docs/codegraph.md` if it exists.
4. If `.codegraph/` exists and CodeGraph tools are available, use graph context to narrow relevant symbols, dependencies, and impact.
5. Review relevant files in `docs/` based on the task.
6. Identify the affected layer:
   - data
   - training
   - evaluation
   - export
   - optimization
   - deployment
   - frontend/backend if applicable
7. Summarize:
   - current state
   - relevant constraints
   - involved files
   - risks
   - possible validations

## Rule

Do not modify code during orientation. If an important ambiguity appears, make it explicit before proposing changes.
