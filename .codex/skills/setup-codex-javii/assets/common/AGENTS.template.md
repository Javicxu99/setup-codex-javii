# {{PROJECT_NAME}}

Project initialized with the Codex `{{PROFILE}}` profile.

## Mission

Help implement, validate, and document changes in a clear, incremental, reviewable way.

## Structure

- `.codex/config.toml`: local Codex configuration.
- `.codex/prompts/`: reusable project prompts.
- `.codex/skills/`: local project skills.
- `docs/project-context.md`: main project context.
- `docs/architecture.md`: technical structure.
- `docs/codegraph.md`: optional graph-based code orientation.
- `docs/task-log.md`: changes, decisions, and validations.

## Rules

- Read `docs/project-context.md` before important tasks.
- Use CodeGraph orientation when `.codegraph/` exists and the task spans multiple files or symbols.
- Keep changes small and directly related to the task.
- Do not introduce dependencies, services, or abstractions without a clear need.
- Do not overwrite existing work without understanding it.
- Record important decisions in `docs/task-log.md`.

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
