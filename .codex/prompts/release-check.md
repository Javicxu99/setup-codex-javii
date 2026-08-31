# Release check

Review this repo before publishing a version.

Checklist:

1. Check `git status --short --branch`.
2. Verify `VERSION` and `CHANGELOG.md` match the intended release.
3. Run compile, unit, end-to-end preview/apply, and `git diff --check` validation from `README.md`.
4. Confirm provider model identifiers and autonomy settings have not crossed directories.
5. Search for secrets, API-key requirements, scheduled model workflows, raw transcripts, temporary files, and accidental graph database files.
6. Confirm template/live-copy synchronization checks pass.
7. Confirm `docs/release-process.md` matches the branch and pull-request flow.
8. Summarize release readiness and any blockers.

Do not commit, tag, or push unless explicitly asked.
