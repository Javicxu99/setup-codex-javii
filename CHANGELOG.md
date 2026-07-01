# Changelog

All notable changes to `setup-codex-javii` are documented here.

This project follows semantic versioning for Git tags and GitHub releases.

## [Unreleased]

- No unreleased changes.

## [2.1.0] - 2026-07-01

### Added
- `codebase-memory-mcp` replaces CodeGraph as the knowledge-graph engine (99.2% token reduction, sub-ms queries, 158 languages, zero dependencies).
- `.mcp.json` at project root: registers `codebase-memory-mcp` for all team members; `CBM_CACHE_DIR` points graph storage to `grafo/` inside the project.
- `.claude/skills/codebase-memory/SKILL.md`: `/codebase-memory` skill with orientation procedure and MCP setup instructions.
- `.claude/skills/ponytail/SKILL.md`: `/ponytail` skill — lazy-dev mode (YAGNI enforced, shortest working diff, lite/full/ultra levels).
- `.codex/skills/codebase-memory/SKILL.md`: Codex-native codebase-memory orientation skill.
- `.codex/skills/ponytail/SKILL.md`: Codex-native ponytail skill with full ladder and rules.
- `.codex/prompts/codebase-memory-orient.md`: orientation prompt replacing codegraph-orient.
- Bootstrap assets: all new skills and templates added so generated projects include codebase-memory and ponytail out of the box.
- `settings.json` and template: `claude-sonnet-5`, `bypassPermissions` default mode, full tool allowlist, ponytail marketplace+plugin, `enableAllProjectMcpServers`.

### Changed
- `setup_codex_javii.py`: replaced all CodeGraph references with codebase-memory-mcp; added `.mcp.json` generation; added ponytail skill generation for both `.claude/` and `.codex/`.
- `CLAUDE.md` template and project root: updated skill list and structure to reflect codebase-memory and ponytail.
- `.gitignore`: replaced `.codegraph/` with `grafo/`.

### Removed
- CodeGraph (`colbymchenry/codegraph`) — replaced by codebase-memory-mcp. Reason: 7 critical graph-traversal bugs open on removal date; codebase-memory-mcp is 120× more token-efficient.

## [2.0.0] - 2026-05-19

### Added
- `CLAUDE.md` (root): always-on Claude Code context with embedded Karpathy guidelines - loaded every conversation.
- `.claude/settings.json`: project-level Claude Code config (model: claude-sonnet-4-6, effortLevel: high, shared safety denies, Stop hook for session logging).
- `.claude/skills/karpathy/SKILL.md`: `/karpathy` skill to re-anchor coding discipline mid-conversation.
- `.claude/skills/caveman/SKILL.md`: `/caveman` skill for maximum-simplicity brutalist mode - deliberate counterpoint to Karpathy.
- `.claude/skills/codegraph/SKILL.md`: `/codegraph` skill with complete MCP setup instructions for Claude Code.
- `.claude/skills/archive/SKILL.md`: `/archive` skill for curated session archiving to `docs/codex-session-notes.md`.
- `.claude/skills/release-check/SKILL.md`: `/release-check` skill for pre-release validation.
- All skill files include frontmatter `description` for proper discovery in the Claude Code `/` dropdown.
- Bootstrap now generates the full `.claude/` infrastructure in target projects.
- New `assets/claude/` template subtree: `CLAUDE.template.md`, `settings.template.json`, and all 5 skill files.

### Changed
- `setup_codex_javii.py`: extended with Claude Code bootstrap capability for `CLAUDE.md`, `.claude/settings.json`, and 5 project skills.
- `MANAGED_GITIGNORE_BLOCK`: added `.claude/settings.local.json` and `.claude/session-log.txt` to managed local state.
- Bootstrap completion message updated to "Bootstrap complete (Codex + Claude Code)."
- `AGENTS.md`: added Claude Code working rules.
- `README.md`: new "Claude Code Support" section; updated "What It Generates".
- `.gitignore`: added `.claude/settings.local.json` and `.claude/session-log.txt`.

### Breaking
- Version 2.0.0 bootstrap generates `.claude/` alongside existing Codex setup. Running v2 on a v1-bootstrapped project will create new `.claude/` files and update `.gitignore`. Existing `.codex/`, `AGENTS.md`, and `docs/` are unaffected (backups created as always before any overwrite).

## [1.0.3] - 2026-05-19

- Added optional CodeGraph-ready documentation, prompt, and local orientation skill.
- Added target-project `.gitignore` management for local graph, transcript, temp, and backup artifacts.
- Kept CodeGraph setup user-controlled with `codegraph init -i`; no dependencies are installed by the bootstrap.
- Added `iniciar-setup` Windows launcher and `comando.md` as a concise command cheat sheet for the repo.

## [1.0.2] - 2026-05-04

- Moved the main bootstrap skill into `.codex/skills/setup-codex-javii/` for a more direct Codex project layout.
- Kept bootstrap assets, scripts, prompts, and references inside the Codex-local skill package.
- Updated usage docs and validation prompts to use the Codex-native path.

## [1.0.1] - 2026-05-04

- Converted the bootstrap content to English.
- Refocused the bootstrap as a universal default setup.
- Removed the domain-specific profile from the active bootstrap.
- Added official Codex history persistence and curated session notes.
- Added GitHub traceability templates and release process documentation.

## [1.0.0] - 2026-05-04

- Initial Codex bootstrap skill.
- Added default Codex config, prompts, docs, templates, and local skills.
- Added `project-orientation`, `update-project-context`, and `karpathy-guidelines`.
- Added backup behavior for existing target-project files.
