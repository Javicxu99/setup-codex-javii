# setup-codex-javii

Bootstrap framework that generates standardized Codex + Claude Code infrastructure for any project.
Run `iniciar-setup.ps1` (or the Python script directly) to bootstrap a target project.

Read `docs/project-context.md` (if it exists) for full context before important tasks.

## Project Structure

- `AGENTS.md` - working rules for Codex
- `.codex/config.toml` - Codex configuration (model, reasoning, history)
- `.codex/agents/` - read-only high-reasoning project auditor
- `.codex/prompts/` - reusable Codex prompts (archive-session, codebase-memory-orient, release-check)
- `.codex/skills/` - local Codex skills (karpathy-guidelines, codebase-memory, ponytail, setup-codex-javii)
- `.claude/settings.json` - Claude Code configuration (`claude-fable-5`, high, Pragmatic, bypassPermissions)
- `.claude/agents/` - matching read-only project auditor
- `.claude/output-styles/` - concise Pragmatic output style
- `.claude/skills/` - Claude Code skills (karpathy, caveman, codebase-memory, ponytail, audit-web-quality, review-skill-security, archive, release-check)
- `.mcp.json` - MCP server config (codebase-memory-mcp)
- `.codex/skills/setup-codex-javii/scripts/setup_codex_javii.py` - main bootstrap script (Python, no deps)
- `.codex/skills/setup-codex-javii/assets/` - templates for generated project files

## Active Guidelines (Karpathy)

These principles apply to all non-trivial coding work in this session.

**1. Think Before Coding**
- State important assumptions before changing code.
- Ask or present the tradeoff when multiple interpretations exist.
- Push back when a simpler approach satisfies the request.
- Name confusion when context contradicts the request.

**2. Simplicity First**
- Prefer the smallest design that solves the current problem.
- Do not add features, abstractions, or configurability that were not requested.
- Do not add error handling for impossible or unobserved paths.
- If a solution feels large, look for the smaller version first.

**3. Surgical Changes**
- Every changed line traces back to the user's request.
- Touch only the files needed. Match existing style and patterns.
- Do not reformat or refactor adjacent code as a side effect.
- Mention unrelated issues instead of fixing them silently.

**4. Goal-Driven Execution**
- Convert vague tasks into concrete, verifiable success criteria.
- For bug fixes: reproduce the failure before changing behavior.
- For multi-step work: keep a short plan with a validation path per step.

**5. Empirical Validation**
- Run tests, builds, type checks, linters, or manual checks when available.
- If validation cannot run, say exactly why and what risk remains.
- Do not claim something works unless it was checked.

## Claude Code Skills Available

- `/karpathy` - re-anchor to full karpathy discipline (useful after long conversations drift)
- `/caveman` - retained for provenance but disabled by default in `skillOverrides`
- `/codebase-memory` - orient using Codebase Memory MCP knowledge graph before broad tasks
- `/ponytail` - activate lazy-dev mode (YAGNI enforced, shortest working diff)
- `/archive` - summarize this conversation into `docs/codex-session-notes.md`
- `/release-check` - run pre-release validation checklist
- `/audit-web-quality` - audit accessibility, performance, security, compatibility, and SEO with evidence
- `/review-skill-security` - assess external skills before installing or enabling them

Ponytail Lite is injected automatically by the shared SessionStart hook. The scheduled GitHub
audit uses `gpt-5.6-sol` with high reasoning and remains read-only.

## Session Notes

Claude sessions auto-save to `~/.claude/projects/`. Use `/archive` after important
conversations to create a human-readable curated entry in `docs/codex-session-notes.md`.
