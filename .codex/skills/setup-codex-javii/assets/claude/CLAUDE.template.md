# {{PROJECT_NAME}}

Initialized {{DATE}} with setup-codex-javii (v2). Primary language: {{PRIMARY_LANGUAGE}}.

Read `docs/project-context.md` for full context before important tasks.

## Project Structure

- `AGENTS.md` - working rules for Codex
- `.codex/config.toml` - Codex configuration
- `.codex/prompts/` - reusable Codex prompts
- `.codex/skills/` - local Codex skills
- `.claude/skills/` - Claude Code skills (karpathy, caveman, codebase-memory, ponytail, audit-web-quality, review-skill-security, archive, release-check)
- `.mcp.json` - MCP server config (codebase-memory-mcp)
- `docs/project-context.md` - main project context
- `docs/architecture.md` - technical architecture
- `docs/task-log.md` - change log with decisions

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
- `/caveman` - switch to maximum-simplicity brutalist mode (no abstractions, just make it work)
- `/codebase-memory` - orient using Codebase Memory MCP knowledge graph before broad tasks
- `/ponytail` - activate lazy-dev mode (YAGNI enforced, shortest working diff)
- `/archive` - summarize this conversation into `docs/codex-session-notes.md`
- `/release-check` - run pre-release validation checklist
- `/audit-web-quality` - audit accessibility, performance, security, compatibility, and SEO with evidence
- `/review-skill-security` - assess external skills before installing or enabling them

## Session Notes

Claude sessions auto-save to `~/.claude/projects/`. Use `/archive` after important
conversations to create a human-readable curated entry in `docs/codex-session-notes.md`.
