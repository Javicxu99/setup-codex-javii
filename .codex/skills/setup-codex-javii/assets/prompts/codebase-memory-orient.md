# Codebase Memory Orientation

Orient using the Codebase Memory knowledge graph before a broad implementation, refactor, or debugging task.

## Steps

1. Read `AGENTS.md` and `docs/project-context.md`.
2. If codebase-memory-mcp tools are available:
   - `get_architecture` for overview
   - `search_graph` for relevant symbols
   - `trace_path` for callers/callees on shared code
   - `detect_changes` if a diff exists
3. If unavailable: fall back to `rg` and file reads.
4. Summarize understanding, relevant files, risks, and validation commands before coding.

Do not modify code during orientation.
