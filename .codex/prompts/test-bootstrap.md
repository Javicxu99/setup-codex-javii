# Test bootstrap

Test the bootstrap script in temporary projects.

Expected steps:

1. Create `tmp/sample-default`.
2. Initialize git inside it.
3. Run `python ../../.codex/skills/setup-codex-javii/scripts/setup_codex_javii.py --profile default`.
4. Run it again and verify `.bak` backups.
5. Verify that the expected universal Codex structure exists.
6. Verify that `docs/codegraph.md`, `.codex/prompts/codegraph-orient.md`, and `.codex/skills/codegraph-orientation/SKILL.md` were generated.
7. Verify that `CHANGELOG.md` and `.github/` templates were generated.
8. Confirm the second run created backups before overwriting files.
9. Confirm that a managed `.gitignore` block is created or appended without duplication.
10. Confirm that unsupported profiles are rejected by argparse.
11. Summarize created files, backups, and any failures.

Do not commit.
