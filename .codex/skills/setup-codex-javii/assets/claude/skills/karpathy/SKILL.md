---
description: Re-anchor to Karpathy coding discipline: think before coding, simplicity first, surgical changes, goal-driven execution, and empirical validation. Use mid-conversation when work has drifted.
---

# Karpathy Guidelines

Re-anchor to the karpathy coding discipline for the remainder of this conversation.

Use this as a behavioral guardrail for non-trivial coding work. It is intentionally small
so it can be applied often without burying project-specific instructions.

Tradeoff: these guidelines bias toward caution and verification. For obvious one-line edits,
use judgment and keep the response lightweight.

## 1. Think Before Coding

Do not silently choose an interpretation when the task is ambiguous.

- State important assumptions before changing code.
- If multiple interpretations would lead to different implementations, ask or present the tradeoff.
- Push back gently when a simpler approach satisfies the request.
- Stop and name confusion when local context contradicts the request.

## 2. Simplicity First

Prefer the smallest design that solves the current problem.

- Do not add features that were not requested.
- Do not create abstractions for one known use.
- Do not add configurability for hypothetical future needs.
- Do not add broad error handling for impossible or unobserved paths.
- If a solution feels large, look for the smaller version before continuing.

## 3. Surgical Changes

Every changed line should trace back to the user's request.

- Touch only the files needed for the task.
- Match the existing style and local patterns.
- Do not reformat, rename, or refactor adjacent code as a side effect.
- Mention unrelated dead code or design issues instead of fixing them silently.
- Remove only unused code created by the current change unless asked otherwise.

## 4. Goal-Driven Execution

Turn work into verifiable outcomes.

- Convert vague tasks into concrete success criteria.
- For bug fixes, prefer reproducing the failure before changing behavior.
- For refactors, preserve behavior and run checks before and after when practical.
- For multi-step work, keep a short plan where each step has a validation path.

## 5. Empirical Validation

Close with evidence, not confidence.

- Run tests, builds, type checks, linters, scripts, or manual checks when available.
- If validation cannot run, say exactly why and what risk remains.
- Do not claim something works unless it was checked.
- Keep iterating when validation exposes a real issue.

## Practical Checklist

Before finishing, be able to answer:

- What assumption mattered?
- What is the smallest useful change?
- Which files were intentionally touched?
- What validation ran?
- What risk remains?

## Attribution

Adapted for Claude Code from: `forrestchang/andrej-karpathy-skills` (MIT license)
https://github.com/forrestchang/andrej-karpathy-skills
