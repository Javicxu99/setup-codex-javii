# Commands

## Bootstrap

The launcher always previews first and asks before applying:

```powershell
.\iniciar-setup.cmd
.\iniciar-setup.ps1
```

Preview and apply without the launcher question:

```powershell
.\iniciar-setup.ps1 -Apply
```

The Python entry point previews by default:

```powershell
python scripts\setup_codex_javii.py --target C:\path\to\project
python scripts\setup_codex_javii.py --target C:\path\to\project --apply
```

Selective installation and conflict preservation:

```powershell
python scripts\setup_codex_javii.py --target C:\path\to\project --components codex docs github --on-conflict skip --apply
```

`-NoCodebaseMemory` and `-NoCodeGraph` only skip the optional post-install command check.

## Manual health audit

Open the target in Codex Desktop and ask:

```text
Run the read-only audit in .codex/prompts/project-health-audit.md and report findings only.
```

No OpenAI API key or GitHub Actions workflow is used.

## Codebase Memory

Install from https://github.com/DeusData/codebase-memory-mcp only when wanted, restart Codex,
then use `index_repository`, `get_architecture`, `search_graph`, `trace_path`, and
`detect_changes`. Direct file search remains the fallback.

## Validation

```powershell
python -m py_compile scripts\setup_codex_javii.py
python -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

## Release branch

```powershell
git add .
git commit -m "Release 3.0.0 safe bootstrap workflow"
git push -u origin HEAD
```

Create and merge a pull request before tagging the release on `main`.
