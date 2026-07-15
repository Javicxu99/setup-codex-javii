# Design Notes

## Intent

`setup-codex-javii` should be a personal bootstrapper that is easy to copy across projects and simple enough to maintain without accumulating debt.

## Decisions

- Standard Python only, to avoid dependencies.
- Templates live in `assets/` so the skill can copy resources without loading every file into context.
- Keep `AGENTS.md` short and put long context in `docs/`.
- Create `.bak` backups before overwriting existing files.
- Keep the active bootstrap universal and domain-neutral.

## Non-Goals

- Manage only the shared, credential-free `codebase-memory-mcp` registration and preserve existing MCP servers.
- Do not install tools.
- Do not create a plugin framework.
- Do not assume a single architecture for every project.
- Do not include domain-specific profiles in the active bootstrap until they are explicitly needed.
