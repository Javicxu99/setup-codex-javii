# Working With Codex: {{PROJECT_NAME}}

This project was initialized with `setup-codex-javii` using profile `{{PROFILE}}`.

## Start A Task

1. Read `AGENTS.md`.
2. Read `docs/project-context.md`.
3. Use `.codex/skills/project-orientation` for important work.
4. Use `.codex/skills/codegraph-orientation` when `.codegraph/` exists and the task needs dependency or impact context.
5. Make small, focused changes.
6. Validate with the available commands.
7. Update `docs/task-log.md` after important changes.
8. Update `docs/codex-session-notes.md` when a conversation creates durable project context.
9. Update `CHANGELOG.md` when a change affects project behavior or release notes.

## Session Notes

Codex stores official session history through its own history mechanism, usually under the user's Codex home directory. This project uses `history.persistence = "save-all"` so Codex can preserve session transcripts through the official mechanism.

Use `docs/codex-session-notes.md` for reviewed summaries that are worth keeping in the repo. Do not commit raw transcripts, secrets, credentials, or unreviewed logs. Use `.codex/prompts/archive-session.md` to create a concise entry after an important conversation.

## Local Skills

- `project-orientation`: understand context before changing code.
- `codegraph-orientation`: use optional CodeGraph context before broad code changes.
- `update-project-context`: update context after relevant changes.
- `karpathy-guidelines`: keep work simple, empirical and readable.

## Optional CodeGraph

This project includes `docs/codegraph.md` and `.codex/prompts/codegraph-orient.md` for optional graph-based code orientation.

Official setup starts with the CodeGraph installer:

```bash
npx @colbymchenry/codegraph
```

Then initialize this project only when you want local graph support:

```bash
codegraph init -i
```

Do not commit `.codegraph/`. It is generated local state.

## GitHub Traceability

- Use GitHub issues for bugs and change requests.
- Use pull requests for reviewable work.
- Keep `CHANGELOG.md` focused on user-facing project changes.
- Use Git tags for published versions when the project starts releasing.

## Project Facts

- Project: `{{PROJECT_NAME}}`
- Primary language: `{{PRIMARY_LANGUAGE}}`
- Profile: `{{PROFILE}}`
- Initialized: `{{DATE}}`
