# Release check

Review this project before publishing a version.

Checklist:

1. Check `git status --short --branch`.
2. Verify `CHANGELOG.md` matches the intended release.
3. Run the project validation commands.
4. Search for secrets, raw transcripts, temporary files, accidental vendored CodeGraph files, and unrelated generated artifacts.
5. Confirm GitHub issues, pull requests, and release notes are traceable.
6. Summarize release readiness and any blockers.

Do not commit, tag, or push unless explicitly asked.
