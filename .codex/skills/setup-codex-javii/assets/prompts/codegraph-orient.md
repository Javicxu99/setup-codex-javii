# CodeGraph orient

Use this prompt when a task would benefit from graph-based code understanding.

1. Read `AGENTS.md` and `docs/project-context.md`.
2. Check whether `.codegraph/` exists.
3. If CodeGraph is initialized and tools are available, use graph context to identify:
   - relevant entry points
   - symbol relationships
   - callers and callees
   - likely impact radius
   - files that need direct review
4. If CodeGraph is not initialized or tools are unavailable, fall back to `rg`, file reads, and existing docs.
5. Do not modify code during this orientation.
6. Summarize the current understanding, risks, and validation options before implementation.

If `.codegraph/` is missing and the task is broad, suggest:

```bash
codegraph init -i
```
