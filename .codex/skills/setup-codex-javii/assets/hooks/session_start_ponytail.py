#!/usr/bin/env python3
"""Inject the local Ponytail discipline at the start of agent sessions."""

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        payload = {}

    event_name = payload.get("hook_event_name") or payload.get("hookEventName")
    if event_name not in (None, "SessionStart"):
        return 0

    context = (
        "Ponytail Lite is active for this conversation. Load and apply the "
        "project-local ponytail skill before implementation: enforce YAGNI, prefer "
        "the shortest maintainable diff, preserve existing behavior, and validate "
        "in proportion to risk. Project instructions and user requirements remain "
        "higher priority."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
