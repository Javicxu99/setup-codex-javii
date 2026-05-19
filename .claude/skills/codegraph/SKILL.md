---
description: Orient using CodeGraph before broad implementation, refactoring, or debugging. Includes complete MCP setup instructions for Claude Code. Falls back to Grep/Read when CodeGraph is not initialized.
---

# CodeGraph Orientation

Orient using CodeGraph before a broad implementation, refactor, or debugging task.
Use when the scope is unclear or the change touches shared/central code.

## Procedure

1. CLAUDE.md is already loaded - use it as the first context layer.
2. Read `docs/project-context.md` if it exists.
3. Check whether `.codegraph/` exists in the project root.
4. **If CodeGraph MCP server is available AND `.codegraph/` exists:**
   - Use CodeGraph tools to find relevant symbols, entry points, callers/callees.
   - Identify impact radius before touching shared code.
   - Use the graph to narrow which files need direct reading.
5. **If CodeGraph is not available or not initialized:**
   - Fall back to `Grep` and `Read` tools.
   - Note: run `codegraph init -i` from the project root to initialize (user-controlled).
6. Summarize before proposing changes:
   - Current understanding of the relevant code area.
   - Key files and symbols involved.
   - Dependency or impact risks.
   - Available validation commands.

## MCP Setup (to enable CodeGraph tools in Claude Code)

CodeGraph exposes an MCP server. One-time setup per machine:

### Step 1 - Install CodeGraph globally:
```
npx @colbymchenry/codegraph
```
Restart Claude Code after the installer runs if prompted.

### Step 2 - Add MCP server to `~/.claude/settings.json`:
```json
"mcpServers": {
  "codegraph": {
    "type": "stdio",
    "command": "codegraph",
    "args": ["mcp"]
  }
}
```
Or from the project root, run `codegraph install --print-config claude-code`
and paste the printed snippet into the settings file.

### Step 3 - Initialize each project (once per project):
```
codegraph init -i
```
This creates `.codegraph/` (excluded from git). Re-run after large refactors.

## Without MCP

After `codegraph init -i`, the `.codegraph/` folder contains graph files that
can be searched directly with `Bash(rg)` when the MCP server is not configured.
Orientation is still useful - just slower.

## Rules

- Do not install CodeGraph automatically. Do not run `codegraph init -i` unless asked.
- Do not modify code during orientation. Summarize findings first.
- CodeGraph is optional. Fall back gracefully to search tools when unavailable.
- Source: https://github.com/colbymchenry/codegraph (MIT license)
