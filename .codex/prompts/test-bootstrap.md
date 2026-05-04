# Test bootstrap

Test the bootstrap script in temporary projects.

Expected steps:

1. Create `tmp/sample-default`.
2. Initialize git inside it.
3. Run `python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile default`.
4. Run it again and verify `.bak` backups.
5. Verify that the expected universal Codex structure exists.
6. Verify that `CHANGELOG.md` and `.github/` templates were generated.
7. Confirm the second run created backups before overwriting files.
8. Confirm that unsupported profiles are rejected by argparse.
9. Summarize created files, backups, and any failures.

Do not commit.
