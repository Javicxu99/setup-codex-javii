# CodeGraph

This project is prepared for optional CodeGraph usage.

CodeGraph builds a local code knowledge graph so agents can inspect symbols, dependencies, callers, callees, and impact before making changes. It is optional project-local state and is not required for normal Codex work.

Source: https://github.com/colbymchenry/codegraph

## Initialize

Use the official CodeGraph installer in your environment first:

```bash
npx @colbymchenry/codegraph
```

Restart your agent if the installer asks for it.

Then run this from the project root when you want graph-based code orientation:

```bash
codegraph init -i
```

This creates `.codegraph/` in the project. Treat that directory as generated local state. It should stay out of Git.

## Setup Notes

The upstream project also documents `codegraph install` for non-interactive setup and `codegraph install --print-config codex` for inspecting Codex configuration snippets. Do not add those commands to project scripts unless the team explicitly wants automated CodeGraph setup.

## Agent Workflow

When `.codegraph/` exists:

- Prefer `.codex/skills/codegraph-orientation` before large implementation or refactor tasks.
- Use graph context to identify entry points, dependencies, impact radius, and relevant files.
- Use direct file reads only for the files that matter after the graph has narrowed the search.
- Keep normal validation as the source of truth.

When `.codegraph/` does not exist:

- Continue with normal `AGENTS.md`, `docs/project-context.md`, and file search orientation.
- Suggest `codegraph init -i` only when graph-based orientation would clearly help.

## Notes

- Do not commit `.codegraph/`.
- Do not paste raw graph output into tracked docs unless it has been reviewed and summarized.
- Do not assume CodeGraph replaces tests, builds, or manual review.
