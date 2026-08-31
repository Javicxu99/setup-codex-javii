# Release Process

Use semantic versioning and publish releases through a reviewed branch.

## Prepare

1. Create a focused branch from current `main`.
2. Update `VERSION` and move the matching `CHANGELOG.md` entry out of `Unreleased`.
3. Confirm the README, command reference, setup skill, generated templates, and tests describe the same behavior.
4. Confirm no secret, API-key requirement, scheduled model workflow, raw transcript, backup, or temporary file is tracked.

## Validate

Use Python 3.11 or newer:

```powershell
python -m py_compile scripts\setup_codex_javii.py
python -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

The tests must include an end-to-end temporary repository run covering default preview,
explicit apply, repeat idempotency, backup creation for a changed file, conflict preservation,
component isolation, invalid MCP preflight, provider boundaries, and absence of the retired
scheduled workflow.

Inspect both `git diff` and `git diff --stat` before committing.

## Publish the change

```powershell
git add .
git commit -m "Release 3.0.0 safe bootstrap workflow"
git push -u origin HEAD
```

Open a pull request into `main` with the behavior change, validation evidence, compatibility
notes, and remaining risks. Do not tag from the feature branch.

## Publish the release after merge

1. Update local `main` from the remote.
2. Verify `VERSION` and the changelog entry match the merged code.
3. Re-run the release validation.
4. Create an annotated `v<version>` tag on the merged `main` commit.
5. Push the tag and create a GitHub Release using the matching changelog section.

Tags and GitHub Releases are intentionally separate from the pull request so an unmerged commit
cannot become the published release accidentally.
