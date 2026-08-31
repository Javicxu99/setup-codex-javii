# Manual project health audit

Work read-only. Inspect `.codex/agents` and `agents/` when present before reviewing the
complete repository. Prefer the codebase-memory knowledge graph when it is already available;
otherwise inspect checked-out files directly. Check correctness, tests, configuration, MCP and
hook integration, skills, dependencies, documentation drift, security, secret exposure, and
avoidable developer friction.

Report only evidence-backed findings. Order them by severity and include file and line, impact,
and the smallest safe remediation. Do not modify files, install dependencies, publish changes,
or call external services. State clearly when no actionable finding exists. Keep the report
concise and pragmatic.
