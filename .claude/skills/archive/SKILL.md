---
description: Archive this Claude conversation by appending a curated human-readable summary to docs/codex-session-notes.md. Captures decisions, files changed, validation run, and remaining risks.
---

# Archive Session

Summarize this Claude conversation into `docs/codex-session-notes.md`.

## What to Write

Append a new entry to `docs/codex-session-notes.md` with this structure:

```
## Session - {{DATE}}

**Topic:** one-line summary of what was worked on

**Context:**
- Key background information that informed decisions
- State of the project at the start

**Decisions:**
- Decision 1: what and why
- Decision 2: what and why

**Files Affected:**
- path/to/file.ext - what changed and why

**Validation Run:**
- What was checked and the result

**Follow-ups:**
- Pending items or risks

**Risks Remaining:**
- Known risks not addressed in this session
```

## Rules

- Write curated project memory, not a raw transcript.
- Include only information that will be useful when onboarding future work.
- Do not include secrets, credentials, private tokens, or unreviewed transcript dumps.
- Do not invent results. If something was not validated, say so.
- If this conversation produced no durable project context, write a one-line note: "Session on {{DATE}}: [brief topic]. No durable context generated."
- Keep entries short enough to scan. One entry per conversation.

## Note on Session Storage

Claude sessions auto-save to `~/.claude/projects/` as JSONL files with full conversation
history. This skill creates a human-readable curated summary for the repository.
The full session data is accessible from `~/.claude/projects/` if you need to review raw history.
