# Codebase Memory

This project is prepared for optional Codebase Memory MCP usage.

Codebase Memory builds a local code knowledge graph so agents can inspect symbols, dependencies,
callers, callees, and impact before making changes. It is optional project-local state and is
not required for normal work.

Source: https://github.com/DeusData/codebase-memory-mcp (MIT)

## Install (one-time per machine)

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 -OutFile install.ps1; .\install.ps1
```

Restart your agent after install. The installer configures `~/.claude/.mcp.json`, Codex, VS Code, and other agents automatically.

## Index this project (once per project)

```bash
codebase-memory-mcp cli index_repository '{"repo_path": "/absolute/path/to/project"}'
```

The project `.mcp.json` at the root registers the MCP server — no per-user config needed for teammates.

## Agent workflow

When codebase-memory-mcp is available:

- Prefer `.codex/skills/codebase-memory` or `.claude/skills/codebase-memory` before large implementation or refactor tasks.
- Use `get_architecture` for project overview, `search_graph` for symbols, `trace_path` for impact.
- Use direct file reads only for files the graph has already narrowed down.
- Keep normal validation as source of truth.

When unavailable:

- Continue with normal `AGENTS.md`, `docs/project-context.md`, and file search orientation.

## Notes

- Do not paste raw graph output into tracked docs unless reviewed and summarized.
- Do not assume the graph replaces tests, builds, or manual review.
- The graph index is local state — not committed to git.
