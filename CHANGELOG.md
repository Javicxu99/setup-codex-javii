# Changelog

All notable changes to `setup-codex-javii` are documented here.

This project follows semantic versioning for Git tags and GitHub releases.

## [Unreleased]

- No unreleased changes.

## [3.1.0] - 2026-08-31

### Added

- Default, independently selectable `compliance` component with a dated EU AI Act source baseline,
  proportional intake/evidence templates, and inactive-until-needed high-risk preparation.
- Dependency-free `scripts/check_eu_ai_act.py` gate with `PASS`, `WARNING`,
  `LEGAL_REVIEW_REQUIRED`, and `BLOCKED` results plus distinct exit codes.
- Manual `eu-ai-act-governance` Codex/Claude skills and Codex intake prompt; no model-backed or
  API-key-backed legal automation.
- Deterministic scenarios for no AI, coding assistants, public chatbots, deepfakes, CV screening,
  workplace emotion recognition, critical unknowns, and legal-baseline milestones.

### Changed

- Release, pull-request, project-health, project-context, and agent instructions now link to the
  canonical conditional governance record instead of duplicating legal text.
- The later Notion row `Legislacion de IA` is recorded as a secondary lead and checked against
  official EU and Spanish parliamentary sources without importing Notion content.
- Default bootstrap output now includes the additive compliance files; existing preview, backup,
  atomic-write, provider-boundary, and full-autonomy behavior is unchanged.
- Project-owned compliance intake and evidence files are create-only, so later bootstrap updates
  preserve recorded decisions while managed law/checker files remain backup-safe.

### Compatibility

- No CLI option is removed or renamed. Targets that do not want governance files can omit the
  `compliance` component explicitly.
- A newly generated intake starts as `UNKNOWN_BLOCKED` until a human records the classification;
  this is an intentional release gate, not a claim of legal non-compliance.

## [3.0.0] - 2026-08-31

### Added

- Read-only preview as the default CLI behavior, explicit `--apply`, target selection, component
  selection, and `backup` or `skip` conflict policies.
- Full preflight before every apply, atomic per-file replacement, unchanged-file detection, and
  clear reporting for created, updated, unchanged, preserved, and legacy files.
- Manual Codex Desktop project-health prompt and on-demand provider-specific auditor definitions.
- Python launcher diagnostics that reject incompatible or non-runnable interpreters clearly.
- End-to-end regression coverage for preview immutability, idempotency, selective installs,
  conflict preservation, invalid MCP preflight, provider boundaries, and retired automation.

### Changed

- Python 3.11 is now the minimum supported version; Python 3.10 reaches end of support in October 2026.
- Existing files are backed up only when their rendered content will actually change.
- The Windows launcher previews every plan before applying it and accepts Spanish or English
  confirmation; `-Apply` skips the question but not the preview.
- Hook commands resolve from the Git root so Codex sessions started in subdirectories remain valid.
- Release guidance now uses a branch and pull request before tagging merged `main`.
- Full trusted-repository autonomy remains intentional for both Codex and Claude Code.

### Removed

- The scheduled GitHub Actions project-health workflow and its duplicate bootstrap assets.
- The `OPENAI_API_KEY` requirement. Manual audits use the signed-in Codex Desktop/ChatGPT session
  and no external automation attempts to reuse that session.

### Breaking

- Running the Python entry point without `--apply` now previews instead of writing.
- Python 3.10 and older are rejected.
- Existing target projects are not modified destructively: legacy
  `.github/workflows/daily-project-health.yml` files must be reviewed and removed manually.

## [2.4.0] - 2026-07-16

### Added
- Coordinated read-only daily auditor agents for Codex and Claude Code.
- Ponytail SessionStart hook shared by both agent environments.
- Portable scheduled GitHub audit using `gpt-5.6-sol`, high reasoning, and immutable action pins.
- Pragmatic Claude output style and bootstrap regression coverage for the new infrastructure.

### Changed
- Claude Code now uses the CLI-supported `claude-fable-5` model with high effort and `bypassPermissions`.
- Caveman is explicitly disabled to avoid overlap with Karpathy and automatically activated Ponytail.
- The Notion audit partially adapts production-readiness ideas from Agents Towards Production and no-mistakes without importing their runtimes.
- Enforced provider boundaries: Claude templates and hooks now live under `.claude`, Codex and Claude auditors own only their respective agent directories, and tests prevent model identifiers from crossing providers.

## [2.3.0] - 2026-07-16

### Added
- Compact `audit-web-quality` skill for evidence-led accessibility, Core Web Vitals, performance, security, compatibility, and SEO reviews.
- Universal `review-skill-security` gate for third-party skills, with optional local SkillSpector static analysis.
- Standard-library regression coverage for generated skills, repeat runs, and additive BOM-encoded MCP configuration.

### Changed
- Bootstrap now generates both new skills for Codex and Claude Code without installing additional runtime dependencies.
- Notion audit decisions now reflect the deeper source, dependency, license, portability, and maintenance review.
- Existing `.mcp.json` files with a UTF-8 BOM are now merged safely instead of failing JSON parsing.

## [2.2.0] - 2026-07-15

### Added
- Exhaustive Notion candidate audit in `docs/notion-candidate-audit.md`.

### Changed
- Codex defaults now use `gpt-5.6-sol`, medium reasoning, medium verbosity, and full autonomous local execution.
- Completed the migration from CodeGraph guidance to `codebase-memory-mcp` across launchers, skills, templates, and docs.
- Bootstrap now merges the Codebase Memory server into an existing `.mcp.json` with a backup instead of silently skipping it.
- Claude Code reasoning effort is aligned to `medium`.

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
