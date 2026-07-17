# Daily project health audit

The first output line must be exactly one of:

- `RESULT: CLEAN`
- `RESULT: ACTION_REQUIRED`

Work read-only. Inspect `.codex/agents`, `.claude/agents`, and `agents/` when present before
reviewing the entire repository. Prefer the codebase-memory knowledge graph when available;
otherwise inspect the checked-out files directly. Check correctness, tests, configuration,
MCP and hook integration, skills, dependencies, automation, documentation drift, security,
secret exposure, and avoidable developer friction.

Report only evidence-backed findings. Order them by severity and include the file and line,
impact, and smallest safe remediation. Do not modify files, install dependencies, publish
changes, or call external services. If there are no actionable findings, explain briefly what
was checked and use `RESULT: CLEAN`. Keep the report concise and pragmatic.
