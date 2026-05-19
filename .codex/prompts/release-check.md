# Release check

Review this repo before publishing a version.

Checklist:

1. Check `git status --short --branch`.
2. Verify `VERSION` and `CHANGELOG.md` match the intended release.
3. Run the bootstrap validation in `README.md`.
4. Validate skills with `quick_validate.py`.
5. Search for secrets, raw transcripts, temporary files, domain-specific leftovers, and accidental vendored CodeGraph files.
6. Confirm `docs/release-process.md` has the correct commands.
7. Summarize release readiness and any blockers.

Do not commit, tag, or push unless explicitly asked.
