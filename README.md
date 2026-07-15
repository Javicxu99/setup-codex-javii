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
approval_policy = "never"
sandbox_mode = "danger-full-access"
history.persistence = "save-all"
```

`gpt5.6sol` is the requested human-facing name; the supported Codex identifier is `gpt-5.6-sol`. Full access is deliberate for a personal bootstrap and should only be used in trusted repositories. Organization requirements can still restrict it.

## What it generates

- `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, and a managed `.gitignore` block.
- `.codex/config.toml`, reusable prompts, and project-local skills.
- `.claude/settings.json` and matching Claude Code skills.
- `.mcp.json` with `codebase-memory-mcp`, preserving other configured servers.
- Project context, architecture, task log, graph guidance, and curated session notes under `docs/`.
- Lightweight GitHub issue and pull-request templates.

Included Codex skills:

- `project-orientation`: establish context before broad changes.
- `update-project-context`: keep living documentation synchronized.
- `karpathy-guidelines`: small, surgical, empirically validated changes.
- `codebase-memory`: graph-first code discovery with a documented fallback.
- `ponytail`: optional YAGNI-focused implementation mode.

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

The script detects `.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod`. Before overwriting a managed destination it creates `.bak`, `.bak.1`, and later backups. When `.mcp.json` already exists, it preserves its servers and adds or updates only `codebase-memory-mcp`.

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

The bootstrap also generates Claude Code infrastructure with medium effort, broad local permissions, explicit secret-read denials, project MCP enablement, and matching Karpathy, codebase-memory, Ponytail, archive, and release-check skills.

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
- Universal defaults rather than domain-specific scaffolding.
- Small operational `AGENTS.md`; durable context belongs in `docs/`.
- No automatic binary installation or secret handling.
- Generated local state and raw transcripts remain outside version control.

The complete assessment of projects considered for this setup is in [`docs/notion-candidate-audit.md`](docs/notion-candidate-audit.md).
