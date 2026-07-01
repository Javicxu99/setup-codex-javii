---
name: codebase-memory
description: Orient using Codebase Memory knowledge graph before broad implementation, refactoring, or debugging tasks. Falls back to rg/file reads when unavailable.
---

# codebase-memory

Use this skill before large implementation, refactor, debugging, or architecture tasks where code relationships matter.

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/project-context.md`.
3. Read `docs/codebase-memory.md` if it exists.
4. If codebase-memory-mcp MCP tools are available:
   - call `get_architecture` for a project overview
   - use `search_graph` to find relevant symbols and entry points
   - use `trace_path` to inspect callers, callees, and impact before editing shared code
   - use `detect_changes` on the current diff to assess blast radius
   - use graph context to narrow which files need direct reading
5. If MCP tools are unavailable:
   - fall back to `rg`, `rg --files`, and direct file reads
6. Summarize:
   - current understanding
   - relevant files and symbols
   - dependency or impact risks
   - possible validation commands

## Rules

- Do not install codebase-memory-mcp automatically.
- Do not modify code during orientation. Summarize first.
- Do not treat graph output as a substitute for reading critical code or running validation.
- Keep graph-derived notes concise; do not paste large raw outputs into tracked docs.

## Source

https://github.com/DeusData/codebase-memory-mcp (MIT)
