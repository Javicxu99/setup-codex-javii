# Codex Setup

This project was initialized with the `{{PROFILE}}` profile on {{DATE}}.

## Start work

1. Read `AGENTS.md` and `docs/project-context.md`.
2. Use `project-orientation` for broad tasks.
3. Prefer the `codebase-memory-mcp` graph for symbols and impact; fall back to `rg` and direct reads when unavailable.
4. Keep changes small and record durable decisions in `docs/task-log.md`.
5. Run relevant validation before declaring completion.
6. Complete `docs/compliance/eu-ai-act/intake.json` and run `python scripts/check_eu_ai_act.py --root .` before release.

Ponytail Lite is injected at each new Codex session. The project includes an on-demand,
read-only `project-health-auditor` definition and matching manual prompt.

## Local skills

- `project-orientation`
- `update-project-context`
- `karpathy-guidelines`
- `codebase-memory`
- `ponytail`
- `audit-web-quality`
- `review-skill-security`
- `eu-ai-act-governance`

## Graph setup

Install `codebase-memory-mcp` from https://github.com/DeusData/codebase-memory-mcp, restart Codex, and index this repository with `index_repository`. The project `.mcp.json` registers the server command. Do not commit generated graph database files.

## Manual project health audit

Open this repository in Codex Desktop while signed in with ChatGPT, then ask Codex to run
`.codex/prompts/project-health-audit.md`. The audit uses the active Codex session, requires no
API key, and remains read-only. No scheduled GitHub workflow is generated.

## EU AI Act governance

Use `docs/compliance/eu-ai-act/README.md` for the minimal no-AI route or the conditional AI route.
The checker is deterministic, dependency-free, and local. It supports governance and escalation;
it is not legal advice, certification, conformity assessment, or a guarantee of compliance.
