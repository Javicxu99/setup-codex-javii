---
description: Activate ponytail lazy-dev mode. YAGNI enforced. Shortest working diff wins. Supports intensity levels lite/full/ultra.
---

# Ponytail

Forces the laziest solution that actually works.

## Activate

Ponytail activates automatically via the SessionStart hook (installed via plugin).
Use `/ponytail` to re-activate manually if it drifted.

## Intensity levels

- `/ponytail lite` — build what's asked, name the lazier option in one line
- `/ponytail full` — ladder enforced, stdlib first, shortest diff (default)
- `/ponytail ultra` — YAGNI extremist, deletion before addition

## Deactivate

Say "stop ponytail" or "normal mode".

## The ladder (quick ref)

1. Does this need to exist at all? (YAGNI)
2. Stdlib does it? Use it.
3. Native platform feature covers it? Use it.
4. Already-installed dependency solves it? Use it.
5. Can it be one line? One line.
6. Only then: minimum code that works.

## Install on a new machine

The project `.claude/settings.json` includes `extraKnownMarketplaces` and `enabledPlugins` for ponytail.
Claude Code installs it automatically from https://github.com/DietrichGebert/ponytail (MIT).
