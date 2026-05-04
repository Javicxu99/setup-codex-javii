# setup-codex-javii

This repo is a Codex skill bootstrapper for initializing projects with my personal Codex setup.

## Working Rules

- Keep changes small, clear, and reviewable.
- Do not add external dependencies.
- Do not overengineer scripts, templates, or workflows.
- Do not break CLI compatibility without documenting it.
- Validate `setup-codex-javii/scripts/setup_codex_javii.py` before closing changes.
- Keep `AGENTS.md` and templates short, operational, and easy to adapt.
- Always respect `.bak` backups when writing into target projects.
- Apply `.codex/skills/karpathy-guidelines` by default for non-trivial coding tasks.
- After important Codex conversations, update `docs/codex-session-notes.md` or `docs/task-log.md`.
- For release-relevant changes, update `CHANGELOG.md` and `VERSION`.
- Use `.github/` templates to keep GitHub issues and PRs traceable.
- Never paste raw secrets or unreviewed transcripts into tracked docs.
- Do not commit unless explicitly asked.

## Done

- The expected structure exists.
- The script works with `--profile default`.
- A second run creates backups before overwriting files.
- The README contains reproducible commands.
