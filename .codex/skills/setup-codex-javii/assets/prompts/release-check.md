# Release check

Review this project before publishing a version.

Checklist:

1. Check `git status --short --branch`.
2. Verify `CHANGELOG.md` matches the intended release.
3. Run the project validation commands and inspect the complete diff.
4. Search for secrets, API-key requirements, scheduled model workflows, raw transcripts, temporary files, accidental graph database files, and unrelated generated artifacts.
5. Confirm provider boundaries and intended autonomy settings remain explicit.
6. Confirm GitHub issues, pull requests, and release notes are traceable.
7. Summarize release readiness and any blockers.

Do not commit, tag, or push unless explicitly asked.
