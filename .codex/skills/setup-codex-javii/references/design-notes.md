# Design Notes

## Intent

`setup-codex-javii` should be a personal bootstrapper that is easy to copy across projects and simple enough to maintain without accumulating debt.

## Decisions

- Standard Python 3.11+ only, to avoid dependencies while staying on a supported baseline.
- Templates live in `assets/` so the skill can copy resources without loading every file into context.
- Keep `AGENTS.md` short and put long context in `docs/`.
- Preview by default, preflight every apply, create `.bak` backups before changed-file replacement,
  and skip byte-equivalent rendered content.
- Use atomic per-file replacement so a failed write cannot leave a partial destination.
- Keep full agent autonomy for trusted personal repositories; installation safety is enforced by
  the bootstrap's preview and backup controls rather than agent approval prompts.
- Run project health audits manually from Codex Desktop with the signed-in ChatGPT session.
- Keep the active bootstrap universal: specialist skills may be present when they are dormant until relevant and add no required toolchain.
- Keep EU AI Act governance conditional: JSON for deterministic inputs, Markdown for human evidence,
  official dated sources, fail-closed unknowns, and high-risk templates inactive until classified.
- Vendor Archify at an exact reviewed commit as a provider-neutral selectable component; exclude its
  updater and development-only repository context, require Node only at use time, and never manage
  project-owned diagram inputs or outputs.

## Non-Goals

- Manage only the shared, credential-free `codebase-memory-mcp` registration and preserve existing MCP servers.
- Do not install tools.
- Do not require API credentials or generate scheduled model calls.
- Do not create a plugin framework.
- Do not assume a single architecture for every project.
- Do not install domain-specific toolchains or generate framework scaffolding before a project needs them.
- Do not present governance checks as legal advice, certification, automatic compliance, conformity
  assessment, or a replacement for privacy and sector-specific law.
