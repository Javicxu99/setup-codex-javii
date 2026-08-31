# Test bootstrap

Test the bootstrap script in temporary projects.

Expected steps:

1. Create `tmp/sample-default`.
2. Initialize git inside it.
3. Run `python ../../scripts/setup_codex_javii.py --target . --profile default` and verify no files change.
4. Re-run with `--apply` and verify expected Codex and Claude structures.
5. Change one managed file, preview, apply, and verify a `.bak` copy exists.
6. Repeat without changes and verify no additional backup appears.
7. Verify component selection and `--on-conflict skip` preserve excluded or existing files.
8. Verify `docs/codebase-memory.md`, the manual health prompt, and provider-specific agents.
9. Confirm that no scheduled AI workflow or API-key requirement is generated.
10. Confirm the managed `.gitignore` block is created or appended without duplication.
11. Confirm invalid MCP JSON fails during preflight without partial writes.
12. Confirm unsupported profiles are rejected by argparse.
13. Summarize created files, backups, preserved files, and failures.

Do not commit.
