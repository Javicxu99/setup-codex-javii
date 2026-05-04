# Release Process

Use this process when publishing a new version of `setup-codex-javii`.

## Versioning

- Use semantic versioning: `MAJOR.MINOR.PATCH`.
- Update `VERSION` with the new version.
- Move relevant `CHANGELOG.md` entries from `Unreleased` into the new version section.
- Keep commit messages concise and outcome-oriented.
- Use Git tags for published versions: `v1.0.1`, `v1.1.0`, etc.

## Pre-Release Checklist

1. Review `git status --short --branch`.
2. Run the bootstrap validation from `README.md`.
3. Verify `CHANGELOG.md` and `VERSION` match the intended release.
4. Confirm no secrets, temporary files, or raw transcripts are staged.
5. Commit the release changes.
6. Tag the release.
7. Push the branch and tag to GitHub.

## Commands

```bash
git status
git add .
git commit -m "1.0.2 Move bootstrap skill into Codex native layout"
git tag -a v1.0.2 -m "v1.0.2"
git push
git push origin v1.0.2
```

After pushing, create a GitHub Release from the tag and paste the matching `CHANGELOG.md` entry.
