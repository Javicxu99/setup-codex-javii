# setup-codex-javii

Dependency-free bootstrap for starting trusted projects with coordinated but strictly separated
Codex and Claude Code environments.

## Requirements

- Git.
- Python 3.11 or newer. Python 3.10 reaches end of support in October 2026, so it is no longer a sensible baseline for new projects.
- Codex Desktop, Codex CLI, or the IDE extension signed in with ChatGPT for Codex work. No OpenAI API key is required or used by this repository.
- Claude Code only when the optional Claude component is wanted.
- Node.js 18 or newer only when the optional Archify diagram runtime is used after bootstrap.

The bootstrap itself never installs tools, dependencies, models, plugins, or secrets.

## Trusted-repository autonomy

Generated Codex projects deliberately use full local autonomy:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
plan_mode_reasoning_effort = "medium"
model_reasoning_summary = "auto"
model_verbosity = "medium"
personality = "pragmatic"
approval_policy = "never"
sandbox_mode = "danger-full-access"
history.persistence = "save-all"

[features]
hooks = true
multi_agent = true
```

Claude uses `claude-fable-5`, high effort, the Pragmatic output style, and
`bypassPermissions`. These settings avoid confirmation prompts by design. Use this bootstrap only
for personal repositories whose contents, hooks, MCP configuration, and dependencies you trust.
Organization policy can still impose stricter controls.

## Generated components

The default installation includes every component. `--components` can select any subset:

| Component | Generated scope |
| --- | --- |
| `codex` | `AGENTS.md`, `.codex/config.toml`, Codex-only agents, hooks, prompts, and skills |
| `claude` | `CLAUDE.md`, `.claude/settings.json`, Claude-only agents, hooks, output style, and skills |
| `docs` | Project context, architecture, task log, graph guidance, and curated session notes |
| `github` | Pull request and issue templates only |
| `compliance` | Dated EU AI Act baseline, conditional intake/evidence, deterministic checker, and manual provider skills |
| `archify` | Pinned offline-first diagram renderer, portable runner, provider skills, examples, schemas, and provenance |
| `shared` | `CHANGELOG.md`, managed `.gitignore` entries, and additive `.mcp.json` registration |

Provider boundaries are strict: OpenAI models and Codex configuration never enter `.claude/`,
and Anthropic models and Claude configuration never enter `.codex/`. Shared repository context
and the credential-free `.mcp.json` remain provider-neutral.

## Safe installation

Clone the bootstrap once:

```powershell
git clone https://github.com/Javicxu99/setup-codex-javii.git
```

From the target repository root, run the Windows launcher:

```powershell
C:\path\to\setup-codex-javii\iniciar-setup.cmd
```

The launcher finds a compatible Python, prints a complete preview, and asks before applying it.
Use `-Apply` to keep the preview but skip the launcher question:

```powershell
C:\path\to\setup-codex-javii\iniciar-setup.ps1 -Apply
```

The Python entry point is also preview-only by default:

```powershell
python C:\path\to\setup-codex-javii\scripts\setup_codex_javii.py --target C:\path\to\project
```

Apply the reviewed plan explicitly:

```powershell
python C:\path\to\setup-codex-javii\scripts\setup_codex_javii.py --target C:\path\to\project --apply
```

Install only selected scopes or preserve every existing conflicting file:

```powershell
python C:\path\to\setup-codex-javii\scripts\setup_codex_javii.py --target C:\path\to\project --components codex docs github --on-conflict skip --apply
```

Behavior is deterministic:

- Preview mode performs all template, text-decoding, and JSON-merge checks without writing.
- `--apply` repeats that full preflight before the first mutation.
- Changed existing files are copied to `.bak`, `.bak.1`, and later numbered backups before replacement.
- Each replacement is atomic. A write failure does not leave a partially written destination.
- Identical files are left untouched and do not create another backup.
- `--on-conflict skip` preserves every existing destination and creates only missing files.
- `.mcp.json` is merged additively, including UTF-8 files with a BOM; unrelated servers remain intact.

`-NoCodebaseMemory` and its legacy alias `-NoCodeGraph` suppress only the launcher's optional
post-install availability check. Use `--components` when you want to omit generated scopes.

## Archify diagrams

The default bootstrap includes [Archify](https://github.com/tt-a1i/archify) 2.16.0 pinned to
commit `199360cc6687a7857b54dd188d4922b09e466a4b` under its MIT license. The bootstrap does not
install Node.js or packages. When Node.js 18+ is already available, verify and use it with:

```powershell
python scripts\run_archify.py doctor
python scripts\run_archify.py validate architecture path\to\diagram.json --quality showcase --json
python scripts\run_archify.py deliver architecture path\to\diagram.json path\to\diagram.html --quality showcase --json
```

The Codex and Claude Code `archify` skills guide schema-first authoring and validation. Automatic
update checks and web-font requests were removed. Remote brand capture and browser-opening commands
are allowed only when explicitly requested; the normal workflow is local. Store diagram sources and
HTML in project-owned paths, not `third_party/archify`. See
[`docs/third-party/archify.md`](docs/third-party/archify.md) for the audit, exact source, adaptation,
license, residual risks, and pinned update procedure.

## EU AI Act governance

The default bootstrap includes a lightweight governance component dated `2026-08-31`. It uses
JSON for the machine-read legal baseline and intake, Markdown for human evidence, and only the
Python 3.11 standard library. It does not call a model, use an API key, or contact a legal service.
It is a preparation and evidence tool, not legal advice, certification, conformity assessment,
CE marking, or a promise of compliance.

### Quick route for a project without AI

1. Set `assessment.ai_system` to `no` in `docs/compliance/eu-ai-act/intake.json`.
2. Record the real purpose, owner, date, and `NOT_APPLICABLE` decision.
3. Run `python scripts/check_eu_ai_act.py --root .` and retain its `PASS` result for release.

### Conditional route for a project with AI

1. Record EU scope, intended purpose/context, operator role, prohibited-practice signals,
   transparency triggers, possible high risk/GPAI status, and critical unknowns in `intake.json`.
2. Complete only the applicable sections of `controls.md` and `release-evidence.md`.
3. Run the checker. Its classifications are `NOT_APPLICABLE`, `BASELINE`,
   `TRANSPARENCY_REQUIRED`, `HIGH_RISK_REVIEW`, `PROHIBITED_BLOCKED`, and `UNKNOWN_BLOCKED`.
4. Stop release on `BLOCKED` or `LEGAL_REVIEW_REQUIRED`. Resolve and document `WARNING` results.
5. Activate `high-risk/README.md` only for possible high-risk systems and obtain qualified
   human/legal review.

The checker uses exit codes `0` PASS, `1` WARNING, `2` LEGAL_REVIEW_REQUIRED, and `3` BLOCKED.
Source code produced with a coding assistant is outside Article 50's marking obligation according
to the Commission FAQ; that does not exempt other output types or uses. The baseline warns after
90 days and when a recorded future legal milestone is reached without a refresh.

Use `.codex/prompts/eu-ai-act-intake.md`, the `eu-ai-act-governance` Codex/Claude skill, and
[`docs/compliance/eu-ai-act/README.md`](docs/compliance/eu-ai-act/README.md) for the manual flow.

### Migration from 3.1.0

Version 3.2.0 is additive. A default apply creates the `archify` runtime, runner, documentation,
and provider skills. Targets that do not want it can omit `archify` with `--components`. Existing
project diagram inputs and outputs are never managed by the bootstrap. No Node.js installation,
package installation, automatic network request, or background process is introduced.

### Migration from 3.0.0

Version 3.1.0 is additive. A default apply creates the new `compliance` files with backup-safe
behavior. The generated intake starts as `UNKNOWN_BLOCKED` so a release cannot silently assume
facts. Project-owned intake, controls, release evidence, and high-risk records are create-only and
remain untouched on later bootstrap runs. Existing automation remains unchanged; explicitly omit
`compliance` with `--components` when a target does not want the governance files.

## Manual project health audit

The previous scheduled GitHub Actions audit has been removed. It required
`OPENAI_API_KEY`, failed when the secret was absent, and could not reuse a Codex Desktop/ChatGPT
session. This project does not replace it with another external automation.

To audit a project without an API key:

1. Open the target repository in Codex Desktop while signed in with ChatGPT.
2. Ask: `Run the read-only audit in .codex/prompts/project-health-audit.md and report findings only.`
3. Review the result before asking Codex to implement any finding.

The prompt and the `project-health-auditor` agent are read-only. They do not install, edit,
publish, or call external services.

### Migration from 2.4 or earlier

The bootstrap never deletes target-project files. If an older generated project still contains
`.github/workflows/daily-project-health.yml`, review and delete that file manually to stop its
scheduled API-key failures. The new bootstrap prints a warning when it detects that legacy file.

## Optional Codebase Memory MCP

Source: https://github.com/DeusData/codebase-memory-mcp (MIT).

Install it separately only if the project benefits from graph-based orientation. The generated
`.mcp.json` registers the `codebase-memory-mcp` command but does not install or execute it.
Direct file search remains the documented fallback.

## Validation

From this repository:

```powershell
python -m py_compile scripts\setup_codex_javii.py scripts\check_eu_ai_act.py scripts\run_archify.py
python -m unittest discover -s tests -v
python scripts\check_eu_ai_act.py --root . --as-of-date 2026-09-01
python scripts\run_archify.py doctor
python scripts\run_archify.py validate architecture third_party\archify\examples\web-app.architecture.json --quality showcase --json
git diff --check
git status --short --branch
```

The standard-library test suite covers preview immutability, explicit apply, atomic backup-safe
updates, idempotent repeats, conflict preservation, component selection, invalid MCP preflight,
provider boundaries, hook execution, the retired scheduled workflow, eight required legal
scenarios, baseline/milestone freshness, Archify component isolation, renderer syntax, showcase
validation, HTML delivery, offline policy, and useful missing-Node diagnostics.

## Current documentation basis

Behavior was reviewed on 2026-08-31 against primary documentation:

- [OpenAI authentication](https://learn.chatgpt.com/docs/auth) for ChatGPT sign-in without an API key.
- [Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [Codex hooks](https://learn.chatgpt.com/docs/hooks).
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config), [settings](https://code.claude.com/docs/en/settings), and [permission modes](https://code.claude.com/docs/en/permission-modes).
- [Python version status](https://devguide.python.org/versions/) for the Python 3.11 minimum.
- [Consolidated Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX%3A02024R1689-20260727), [Article 50 guidance and FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), [AI literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers), and the [official implementation timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline).

The existing candidate assessment remains in
[`docs/notion-candidate-audit.md`](docs/notion-candidate-audit.md). The later “Legislacion de IA”
row is recorded there as a secondary discovery lead; no Notion content or external runtime is
imported.
