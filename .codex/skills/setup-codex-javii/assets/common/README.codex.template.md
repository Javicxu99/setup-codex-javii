# Codex Setup

This project was initialized with the `{{PROFILE}}` profile on {{DATE}}.

## Start work

1. Read `AGENTS.md` and `docs/project-context.md`.
2. Use `project-orientation` for broad tasks.
3. Prefer the `codebase-memory-mcp` graph for symbols and impact; fall back to `rg` and direct reads when unavailable.
4. Keep changes small and record durable decisions in `docs/task-log.md`.
5. Run relevant validation before declaring completion.

Ponytail Lite is injected at each new Codex session. The project includes a Codex-native,
read-only `daily-project-auditor` definition.

## Local skills

- `project-orientation`
- `update-project-context`
- `karpathy-guidelines`
- `codebase-memory`
- `ponytail`
- `audit-web-quality`
- `review-skill-security`

## Graph setup

Install `codebase-memory-mcp` from https://github.com/DeusData/codebase-memory-mcp, restart Codex, and index this repository with `index_repository`. The project `.mcp.json` registers the server command. Do not commit generated graph database files.

## Daily audit

Add `OPENAI_API_KEY` as a GitHub Actions secret to enable the portable daily audit. It runs
`gpt-5.6-sol` with high reasoning in a read-only sandbox at 03:17 UTC and on manual dispatch.
