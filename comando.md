# Commands

## Bootstrap

```powershell
.\iniciar-setup.cmd
.\iniciar-setup.ps1 -NoCodebaseMemory
python .codex\skills\setup-codex-javii\scripts\setup_codex_javii.py --profile default
```

`-NoCodeGraph` remains an alias for backward compatibility.

## Codebase Memory

Install from https://github.com/DeusData/codebase-memory-mcp, restart Codex, then use the MCP tools:

- `index_repository` to create or refresh the graph.
- `get_architecture` for orientation.
- `search_graph` for symbols.
- `trace_path` for callers, callees, and impact.
- `detect_changes` to review the current diff.

## Validation

```powershell
python -m py_compile .codex\skills\setup-codex-javii\scripts\setup_codex_javii.py
git diff --check
git status --short --branch
```

## Release

```powershell
git add .
git commit -m "2.2.0 Align Codex defaults and graph integration"
git push -u origin HEAD
```
