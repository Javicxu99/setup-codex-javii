# setup-codex-javii

Dependency-free bootstrap for starting trusted projects with coordinated but strictly separated
Codex and Claude Code environments.

## Requirements

- Git.
- Python 3.11 or newer. Python 3.10 reaches end of support in October 2026, so it is no longer a sensible baseline for new projects.
- Codex Desktop, Codex CLI, or the IDE extension signed in with ChatGPT for Codex work. No OpenAI API key is required or used by this repository.
- Claude Code only when the optional Claude component is wanted.

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
python -m py_compile scripts\setup_codex_javii.py
python -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

The standard-library test suite covers preview immutability, explicit apply, atomic backup-safe
updates, idempotent repeats, conflict preservation, component selection, invalid MCP preflight,
provider boundaries, hook execution, and the removal of the scheduled workflow.

## Current documentation basis

Behavior was reviewed on 2026-08-31 against primary documentation:

- [OpenAI authentication](https://learn.chatgpt.com/docs/auth) for ChatGPT sign-in without an API key.
- [Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [Codex hooks](https://learn.chatgpt.com/docs/hooks).
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config), [settings](https://code.claude.com/docs/en/settings), and [permission modes](https://code.claude.com/docs/en/permission-modes).
- [Python version status](https://devguide.python.org/versions/) for the Python 3.11 minimum.

The existing candidate assessment remains in
[`docs/notion-candidate-audit.md`](docs/notion-candidate-audit.md); this release does not import
any new repository or Notion content.
