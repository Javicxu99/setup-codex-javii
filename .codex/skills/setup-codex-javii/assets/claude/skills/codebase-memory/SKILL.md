---
description: Orient using Codebase Memory MCP before broad implementation, refactoring, or debugging. Falls back to Grep/Read when the MCP server is unavailable.
---

# Codebase Memory Orientation

Orient using the Codebase Memory knowledge graph before a broad implementation, refactor, or debugging task.
Use when the scope is unclear or the change touches shared/central code.

## Procedure

1. CLAUDE.md is already loaded — use it as the first context layer.
2. Read `docs/project-context.md` if it exists.
3. If the `codebase-memory-mcp` MCP server is available:
   - Call `get_architecture` for a project overview.
   - Use `search_graph` to find relevant symbols and entry points.
   - Use `trace_path` to inspect callers, callees, and impact before editing shared code.
   - Use `detect_changes` on the current diff to assess blast radius.
   - Narrow which files need direct reading using graph context.
4. If the MCP server is unavailable:
   - Fall back to `Grep` and `Read` tools.
5. Summarize before proposing changes:
   - Current understanding of the relevant code area.
   - Key files and symbols involved.
   - Dependency or impact risks.
   - Available validation commands.

## MCP Setup (one-time per machine)

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 -OutFile install.ps1; .\install.ps1
```

Restart Claude Code after install. The installer configures `~/.claude/.mcp.json` automatically.

## Index this project (once per project)

```bash
codebase-memory-mcp cli index_repository '{"repo_path": "/absolute/path/to/project"}'
```

The project `.mcp.json` at the root registers the server — no per-user config needed.

## Key tools

- `get_architecture` — project overview (languages, packages, routes)
- `search_graph` — find symbols by name pattern
- `trace_path` — callers/callees traversal
- `detect_changes` — git diff → affected symbols + blast radius
- `query_graph` — Cypher read-only queries for complex traversals

## Rules

- Do not install codebase-memory-mcp automatically.
- Do not modify code during orientation. Summarize findings first.
- Fall back gracefully to Grep/Read when MCP is unavailable.
- Source: https://github.com/DeusData/codebase-memory-mcp (MIT)
