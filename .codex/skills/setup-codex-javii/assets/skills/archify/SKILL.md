---
name: archify
description: Create validated architecture, workflow, sequence, data-flow, and lifecycle diagrams as standalone interactive HTML. Use for system maps, infrastructure, technical processes, API sequences, pipelines, state machines, or Mermaid conversion.
license: MIT
metadata:
  version: "2.16.0-setup.1"
  upstream: tt-a1i/archify@199360cc6687a7857b54dd188d4922b09e466a4b
---

# Archify

Use the vendored deterministic renderer in `third_party/archify`. Node.js 18+ is optional for the
project but required while this skill runs. Start with:

```text
python scripts/run_archify.py doctor
```

Stop with the printed installation guidance if the doctor cannot run.

## Authoring route

1. Choose `architecture`, `workflow`, `sequence`, `dataflow`, or `lifecycle` from the request.
2. Read only the matching file in `third_party/archify/schemas/`, `common.schema.json`, and one
   matching JSON example. Use examples for shape, never for project facts.
3. Inspect repository evidence when the map must describe real code. Write the candidate JSON
   before exploring renderer internals. Keep stable IDs, one clear main path, sparse labels, and at
   most 12 primary nodes unless the user requests dense detail.
4. Validate after each edit and immediately before delivery:

   ```text
   python scripts/run_archify.py validate <type> <candidate.json> --quality showcase --json
   ```

5. Apply only the reported subject and supported fix. Stop truthfully if two correction rounds do
   not improve the best error count. A passing final candidate is frozen.
6. Deliver once:

   ```text
   python scripts/run_archify.py deliver <type> <candidate.json> <output.html> --quality showcase --json
   ```

Do not claim success for a non-zero command. Return the HTML path, diagram type, validation and
delivery receipts, and any remaining uncertainty.

## Boundaries

- Static output is the default. Run `preview` or add `--open` only when the user requests it.
- No automatic version check is included in this adaptation. Never download or install updates.
- Use bundled brand IDs by default. `brands capture <url>` performs an explicit network fetch;
  run it only when the user explicitly asks to fetch that official brand URL.
- `visual-check` is optional and needs a compatible local Chrome/Chromium. Its screenshots prove
  bounded browser behavior, not perceptual approval.
- Archify output belongs in a user-selected project path, never inside `third_party/archify`.

Read `third_party/archify/references/authoring-contract.md` only for field enums, geometry repair,
repository evidence, or mode placement. Read `delivery-contract.md` for browser evidence, preview,
exports, or opening. Read `viewer-runtime.md` only for share cards, motion, stories, deep links,
presentation, or advanced viewer features.

Provenance, restrictions, and the update procedure are in `docs/third-party/archify.md`.
