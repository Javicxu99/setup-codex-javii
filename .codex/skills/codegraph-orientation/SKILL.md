---
name: codegraph-orientation
description: Use optional CodeGraph context to orient before broad coding, refactoring, or debugging tasks. Falls back to normal repo search when CodeGraph is unavailable.
---

# codegraph-orientation

Use this skill before large implementation, refactor, debugging, or architecture tasks where code relationships matter.

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/project-context.md`.
3. Read `docs/codegraph.md` if it exists.
4. Check whether `.codegraph/` exists in the project root.
5. If CodeGraph is initialized and CodeGraph tools are available:
   - use graph search or context to find relevant symbols and entry points
   - inspect callers, callees, and impact before editing shared code
   - use graph file structure to narrow which files need direct reads
6. If CodeGraph is not initialized or tools are unavailable:
   - fall back to `rg`, `rg --files`, and direct file reads
   - mention that `codegraph init -i` can be run for future graph-based orientation
7. Summarize:
   - current understanding
   - relevant files and symbols
   - dependency or impact risks
   - possible validation commands

## Rules

- Do not install CodeGraph.
- Do not run `codegraph init -i` unless the user explicitly asks.
- Do not modify code during orientation.
- Do not treat graph output as a substitute for reading critical code or running validation.
- Keep graph-derived notes concise; do not paste large raw outputs into tracked docs.

## Source

Inspired by optional CodeGraph workflows from:

- Repository: `colbymchenry/codegraph`
- URL: https://github.com/colbymchenry/codegraph
- License: MIT
