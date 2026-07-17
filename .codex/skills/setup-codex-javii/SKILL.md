---
name: setup-codex-javii
description: Initialize the OpenAI Codex side of Javii's universal project setup. Use when the user wants Codex agent configuration, hooks, prompts, context docs, reusable local skills, codebase-memory-mcp, and daily health automation before starting implementation.
---

# setup-codex-javii

Use this skill to initialize a repository with a clean, compact, and maintainable Codex structure.

## Procedure

1. Detect the target repository root by looking for `.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod`.
2. Run the default bootstrap from the target project root:

```bash
python path/to/setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

3. Create or update:
   - `AGENTS.md`
   - `CHANGELOG.md`
   - `.codex/config.toml`
   - `.codex/agents/` and `.codex/hooks.json`
   - `.codex/prompts/`
   - `.codex/skills/`
   - `.github/`
   - managed `.gitignore` entries for local Codex and codebase-memory state
   - `docs/`
4. Enable official Codex history persistence with `history.persistence = "save-all"`.
5. Create `docs/codex-session-notes.md` for reviewed summaries of important Codex conversations.
6. Configure `codebase-memory-mcp` and create its docs, prompt, and orientation skill.
7. Copy local skills:
   - `project-orientation`
   - `codebase-memory`
   - `update-project-context`
   - `karpathy-guidelines`
8. Add the read-only daily auditor, Ponytail SessionStart hook, and portable scheduled GitHub audit.
9. Create `.bak` backups before overwriting any existing file.
10. Review the final report of created files, files updated with backup, backups, and next steps.

## Rules

- Do not install dependencies.
- Do not schedule the daily GitHub audit until the target has an `OPENAI_API_KEY` Actions secret.
- Do not commit unless explicitly asked.
- Keep `AGENTS.md` brief; long context belongs in `docs/`.
- Store curated conversation summaries in `docs/codex-session-notes.md`, not raw transcripts.
- Do not install binaries automatically; document installation and let the user or environment provide `codebase-memory-mcp`.
- Keep the setup universal; domain-specific project context belongs in the generated `docs/`.
- Keep GitHub traceability lightweight with changelog entries, issues, PRs, and version tags.
