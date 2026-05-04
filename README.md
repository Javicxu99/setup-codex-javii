# setup-codex-javii

Personal bootstrap repo for preparing projects with a clean, repeatable Codex setup.

This repository contains a reusable Codex skill named `setup-codex-javii`. It initializes a target project with practical agent instructions, Codex configuration, prompts, project context docs, and local skills that can be customized per project.

## What It Generates

Running the bootstrap script in a target project creates:

- `AGENTS.md`
- `CHANGELOG.md`
- `.codex/config.toml`
- `.codex/prompts/`
- `.codex/skills/`
- `.github/`
- `docs/project-context.md`
- `docs/architecture.md`
- `docs/task-log.md`
- `docs/codex-session-notes.md`
- `docs/README.codex.md`

## Usage

Clone this repo from GitHub and use it as your personal default:

```bash
git clone https://github.com/Javicxu99/setup-codex-javii.git
```

From the root of a target project:

```bash
python path/to/setup-codex-javii/setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

The script detects the project root by looking for `.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod`.

If a destination file already exists, the script creates a backup first: `.bak`, `.bak.1`, `.bak.2`, and so on.

## Generated Codex Config

The generated Codex configuration uses:

```toml
model = "gpt-5.5"
model_provider = "openai"
model_reasoning_effort = "high"
plan_mode_reasoning_effort = "high"
model_reasoning_summary = "auto"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

No MCP or advanced configuration is included by default.

## Codex History

Codex session history is handled by Codex itself through `history.persistence = "save-all"`. Raw Codex state normally lives under the user's Codex home directory, such as `~/.codex`, not inside the project repository.

Use `docs/codex-session-notes.md` for reviewed, human-readable summaries of important Codex conversations. Use `.codex/prompts/archive-session.md` when a conversation creates durable project context, decisions, operating assumptions, follow-ups, or risks.

Raw transcript exports are not created by default. If you manually export raw sessions into the project, keep them out of Git; `.gitignore` excludes common local raw-export paths.

## GitHub Traceability

This repo is prepared for long-term GitHub traceability:

- `VERSION` stores the current bootstrap version.
- `CHANGELOG.md` records user-facing changes by version.
- `docs/release-process.md` documents the release and tagging flow.
- `.github/` contains issue and pull request templates.
- `.codex/prompts/release-check.md` helps review a version before publishing.

Generated projects also receive `CHANGELOG.md` and GitHub issue/PR templates so future work can be tracked from the start.

## Included Local Skills

- `project-orientation`: read context and map the affected area before important work.
- `update-project-context`: update living project docs after meaningful changes.
- `karpathy-guidelines`: Codex-oriented adaptation of principles inspired by `forrestchang/andrej-karpathy-skills`.

This repo also includes `karpathy-guidelines` in `.codex/skills/karpathy-guidelines/` so it can be selected directly while working on this project.

## Install `karpathy-guidelines` Globally

To use the skill across Codex chats and projects, copy it to the global Codex skills directory.

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills\karpathy-guidelines"
Copy-Item -Force ".codex\skills\karpathy-guidelines\SKILL.md" "$env:USERPROFILE\.codex\skills\karpathy-guidelines\SKILL.md"
```

Bash:

```bash
mkdir -p ~/.codex/skills/karpathy-guidelines
cp .codex/skills/karpathy-guidelines/SKILL.md ~/.codex/skills/karpathy-guidelines/SKILL.md
```

## Working With Codex In VS Code

1. Clone or reference this repo from your Codex environment.
2. Open the target project in VS Code.
3. Run the bootstrap script with the default profile.
4. Ask Codex to read `AGENTS.md` and `docs/project-context.md` before important tasks.
5. Use the local skills for orientation, context updates, and implementation discipline.

## Local Validation

From this repo root:

```bash
mkdir tmp/sample-default
cd tmp/sample-default
git init
python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile default
python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

The second run should create `.bak` backups.

## Release Commit

Review generated changes before committing.

```bash
git status
git add .
git commit -m "1.0.1 Make bootstrap universal with history and traceability"
git tag -a v1.0.1 -m "v1.0.1"
git push
git push origin v1.0.1
```
