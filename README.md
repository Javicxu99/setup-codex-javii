# setup-codex-javii

Reusable bootstrap for starting projects with a consistent Codex and Claude Code setup.

## Defaults

Generated Codex projects use:

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

`gpt5.6sol` is the requested human-facing name; the supported Codex identifier is `gpt-5.6-sol`. Full access is deliberate for a personal bootstrap and should only be used in trusted repositories. Organization requirements can still restrict it.

## What it generates

- `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, and a managed `.gitignore` block.
- `.codex/config.toml`, a Ponytail `SessionStart` hook, reusable prompts, skills, and a read-only high-reasoning auditor agent.
- `.claude/settings.json`, matching skills and auditor agent, and the Pragmatic output style.
- `.mcp.json` with `codebase-memory-mcp`, preserving other configured servers.
- Project context, architecture, task log, graph guidance, and curated session notes under `docs/`.
- Lightweight GitHub templates and an optional daily project-health workflow.

Included Codex skills:

- `project-orientation`: establish context before broad changes.
- `update-project-context`: keep living documentation synchronized.
- `karpathy-guidelines`: small, surgical, empirically validated changes.
- `codebase-memory`: graph-first code discovery with a documented fallback.
- `ponytail`: optional YAGNI-focused implementation mode.
- `audit-web-quality`: evidence-led web accessibility, performance, security, compatibility, and SEO review.
- `review-skill-security`: supply-chain review before adopting external skills, plugins, or MCP bundles.

## Quick start

Clone the bootstrap once:

```powershell
git clone https://github.com/Javicxu99/setup-codex-javii.git
```

From the target repository root:

```powershell
C:\path\to\setup-codex-javii\iniciar-setup.cmd
```

Or run the dependency-free Python entry point:

```powershell
python C:\path\to\setup-codex-javii\.codex\skills\setup-codex-javii\scripts\setup_codex_javii.py --profile default
```

The script detects `.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod`. Before overwriting a managed destination it creates `.bak`, `.bak.1`, and later backups. When `.mcp.json` already exists, including UTF-8 files with a BOM, it preserves its servers and adds or updates only `codebase-memory-mcp`.

## Codebase Memory MCP

Source: https://github.com/DeusData/codebase-memory-mcp (MIT).

Install the binary once per machine using the upstream instructions. The generated `.mcp.json` registers:

```json
{
  "mcpServers": {
    "codebase-memory-mcp": {
      "command": "codebase-memory-mcp"
    }
  }
}
```

After installation, restart Codex and index the target repository with the MCP `index_repository` tool. Agents should prefer:

1. `search_graph` for symbols and routes.
2. `trace_path` for callers, callees, and impact.
3. `get_code_snippet` after resolving an exact qualified name.
4. `query_graph` for complex relationships.
5. `get_architecture` for a high-level map.

Use `rg` and direct file reads for literals, configuration, non-code files, or when the graph is unavailable.

## Claude Code

The generated settings use the exact model accepted by the installed Claude CLI, `claude-fable-5`, with `high` effort, the `Pragmatic` output style, project MCP enablement, and `bypassPermissions`. Secret reads remain denied explicitly. This autonomy is intended only for trusted repositories. Caveman remains available in the template for provenance but is disabled through `skillOverrides`; Ponytail is injected at startup, resume, and clear through the shared SessionStart hook.

## Daily project health

`.github/workflows/daily-project-health.yml` runs every day at 03:17 UTC and can also be started manually. It invokes `gpt-5.6-sol` with `high` reasoning in a read-only sandbox, audits agent definitions first and then the complete repository, uploads a 30-day report, and opens or updates an issue only for actionable findings.

After bootstrap, add an `OPENAI_API_KEY` Actions secret to the target repository. Without that secret the workflow fails safely with an explicit message. A Codex desktop scheduled task is not generated because desktop tasks are machine-local and require the target checkout to be registered in the app; the repository workflow is portable and versioned.

## Validation

From this repository:

```powershell
python -m py_compile .codex\skills\setup-codex-javii\scripts\setup_codex_javii.py
```

For an end-to-end check, create a temporary Git repository, run the bootstrap twice, and verify that the second run creates backups. Also test a pre-existing `.mcp.json` to confirm that unrelated MCP servers remain intact.

```powershell
git diff --check
git status --short --branch
```

## Design constraints

- Standard Python only; no runtime package dependency.
- Universal, dormant-on-demand skills rather than domain-specific scaffolding or installed toolchains.
- Small operational `AGENTS.md`; durable context belongs in `docs/`.
- No automatic binary installation or secret handling.
- Generated local state and raw transcripts remain outside version control.

The complete assessment of projects considered for this setup is in [`docs/notion-candidate-audit.md`](docs/notion-candidate-audit.md).
