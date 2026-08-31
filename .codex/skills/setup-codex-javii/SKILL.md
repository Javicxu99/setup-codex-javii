---
name: setup-codex-javii
description: Preview and initialize Javii's provider-separated Codex and Claude Code project setup, including local instructions, prompts, skills, context docs, optional codebase-memory-mcp registration, and manual health auditing without API credentials.
---

# setup-codex-javii

Use this skill to initialize a trusted repository with a compact, reusable Codex and Claude Code
structure. Python 3.11 or newer is required; no dependency or secret is installed.

## Procedure

1. Detect the target root from `.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod`.
2. Preview the complete plan from the target project:

```bash
python path/to/setup-codex-javii/scripts/setup_codex_javii.py --target .
```

3. Review files to create, files to back up and update, unchanged files, preserved files, and warnings.
4. Select a subset when needed with `--components codex claude docs github shared`.
5. Use `--on-conflict skip` when every existing destination must remain untouched.
6. Apply only after the preview is acceptable:

```bash
python path/to/setup-codex-javii/scripts/setup_codex_javii.py --target . --apply
```

7. Review `AGENTS.md`, `CLAUDE.md`, and `docs/project-context.md` before committing.
8. Run project validation and inspect the resulting diff.

## Generated behavior

- Codex and Claude configuration remain in their own provider directories.
- Full autonomous execution remains enabled for both providers and is intended only for trusted repositories.
- Changed files receive numbered `.bak` copies before atomic replacement.
- Identical content is not rewritten and does not create another backup.
- A full read-only preflight runs before any `--apply` mutation.
- `.mcp.json` is merged additively and never installs the optional server.
- GitHub issue and pull request templates are generated without an AI workflow.
- `.codex/prompts/project-health-audit.md` provides an on-demand, read-only audit for Codex Desktop.
- No `OPENAI_API_KEY`, API call, or external scheduled automation is required.

## Rules

- Do not install dependencies, binaries, plugins, or secrets.
- Do not delete legacy target-project files automatically. Warn when the obsolete scheduled audit remains.
- Do not commit unless explicitly asked.
- Keep `AGENTS.md` and `CLAUDE.md` brief; long context belongs in `docs/`.
- Store curated conversation summaries, not raw transcripts.
- Keep the setup universal; domain-specific context belongs in the generated project docs.
- Treat codebase-memory-mcp as optional and preserve direct file search as the fallback.
- Keep GitHub traceability lightweight with changelog entries, issues, pull requests, and version tags.
