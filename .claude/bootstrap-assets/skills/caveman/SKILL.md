---
description: Switch to maximum-simplicity brutalist mode. No abstractions, no patterns, just make it work. Use when stuck overthinking or for trivial tasks that need unblocking fast.
---

# Caveman Mode

You are now in caveman mode. Abandon sophistication. Make it work.

Caveman mode is the deliberate counterpoint to karpathy. Where karpathy is disciplined and
methodical, caveman is brutalist. Use it when you are stuck overthinking, when a task is
genuinely trivial, or when you need to unblock fast.

## The Caveman Philosophy

You do not need:
- Abstractions
- Interfaces or base classes for one use
- Helper utilities used in one place
- Configuration for hypothetical futures
- Error handling for impossible paths
- Docstrings before the code runs
- Refactoring before the feature works

You need:
- Code that runs
- Output that matches the requirement
- The shortest path from here to done

## Caveman Rules

1. Write the simplest possible implementation. Inline everything that is used once.
2. No new files unless the task literally requires a file.
3. No new functions unless you need the same block twice in the same task.
4. Hard-code values. Generalize only when the second use case actually exists.
5. If it works, it is done. Do not polish before the task is complete.
6. Run it. If it blows up, fix only the thing that blew up.
7. Do not consider edge cases that have not been observed yet.

## When To Exit Caveman Mode

Caveman mode gets you unblocked. It is not a production design strategy.

When the thing works, switch back to karpathy for cleanup:
- Use `/karpathy` to re-engage disciplined review.
- Then decide what actually needs cleaning up (often: less than you think).

## What Caveman Mode Is NOT

Not an excuse for unsafe code. No secrets in files, no injection vectors, no
broken auth. Simplicity is the goal, not sloppiness.

Not an excuse to skip running the code. Caveman validates empirically too - by
just running the thing and checking the output.
