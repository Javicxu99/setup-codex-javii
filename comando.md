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

The available components are `codex`, `claude`, `docs`, `github`, `compliance`, `archify`, and
`shared`.

`-NoCodebaseMemory` and `-NoCodeGraph` only skip the optional post-install command check.

## Manual health audit

Open the target in Codex Desktop and ask:

```text
Run the read-only audit in .codex/prompts/project-health-audit.md and report findings only.
```

No OpenAI API key or GitHub Actions workflow is used.

## EU AI Act governance

```powershell
python scripts\check_eu_ai_act.py --root .
python scripts\check_eu_ai_act.py --root . --as-of-date 2026-08-31 --json
```

Exit codes: `0` PASS, `1` WARNING, `2` LEGAL_REVIEW_REQUIRED, `3` BLOCKED. Complete
`docs/compliance/eu-ai-act/intake.json` first. This is governance evidence, not legal advice or
certification.

## Archify diagrams

```powershell
python scripts\run_archify.py doctor
python scripts\run_archify.py validate architecture third_party\archify\examples\web-app.architecture.json --quality showcase --json
python scripts\run_archify.py deliver architecture path\to\diagram.json path\to\diagram.html --quality showcase --json
```

Node.js 18+ is optional and used only for these commands. The bootstrap installs no package and the
normal Archify path performs no update check or remote request.

## Codebase Memory

Install from https://github.com/DeusData/codebase-memory-mcp only when wanted, restart Codex,
then use `index_repository`, `get_architecture`, `search_graph`, `trace_path`, and
`detect_changes`. Direct file search remains the fallback.

## Validation

```powershell
python -m py_compile scripts\setup_codex_javii.py scripts\check_eu_ai_act.py scripts\run_archify.py
python -m unittest discover -s tests -v
python scripts\check_eu_ai_act.py --root . --as-of-date 2026-09-01
python scripts\run_archify.py doctor
git diff --check
git status --short --branch
```

## Release branch

```powershell
git add .
git commit -m "Release 3.2.0 Archify integration"
git push -u origin HEAD
```

Create and merge a pull request before tagging the release on `main`.
