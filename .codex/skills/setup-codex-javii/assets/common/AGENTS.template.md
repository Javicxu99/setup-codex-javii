# {{PROJECT_NAME}}

Project initialized with the Codex `{{PROFILE}}` profile.

## Mission

Help implement, validate, and document changes in a clear, incremental, reviewable way.

## Structure

- `.codex/config.toml`: local Codex configuration.
- `.codex/prompts/`: reusable project prompts.
- `.codex/agents/`: on-demand Codex-only agent definitions.
- `.codex/skills/`: local project skills.
- `docs/project-context.md`: main project context.
- `docs/architecture.md`: technical structure.
- `docs/codebase-memory.md`: graph-based code orientation and setup.
- `docs/task-log.md`: changes, decisions, and validations.
- `docs/compliance/eu-ai-act/`: dated AI applicability, controls, and release evidence.

## Rules

- Read `docs/project-context.md` before important tasks.
- Prefer `codebase-memory-mcp` graph tools when a task spans multiple files or symbols; fall back to `rg` and direct reads when unavailable.
- Keep changes small and directly related to the task.
- Do not introduce dependencies, services, or abstractions without a clear need.
- Do not overwrite existing work without understanding it.
- Treat this repository as trusted: the generated Codex profile has full local autonomy and no approval prompts.
- Record important decisions in `docs/task-log.md`.
- Before release, complete the EU AI Act intake and run `python scripts/check_eu_ai_act.py --root .`; never treat the result as legal advice or certification.

## Validation

- Run available tests or checks.
- If there is no automated validation, explain what was reviewed manually.
- Do not claim results from checks that were not run.

## Done

- The change satisfies the agreed objective.
- Relevant validation has been run or explicitly justified.
- Context documentation is updated if the objective, architecture, or workflow changed.

## Response

Respond with a brief summary, touched files, validation, and remaining risks.
