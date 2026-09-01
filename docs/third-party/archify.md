# Archify provenance and security review

## Pinned source

- Project: [tt-a1i/archify](https://github.com/tt-a1i/archify)
- Default branch reviewed: `main`
- Immutable revision: `199360cc6687a7857b54dd188d4922b09e466a4b`
- Upstream release: `2.16.0`
- Local adaptation: `2.16.0-setup.1`
- License: MIT; the complete upstream notice is retained in `third_party/archify/LICENSE`.
- Acquisition: the system `skill-installer` helper fetched path `archify` at the pinned revision
  into an isolated staging directory. No `.git` data was copied.

## Included and adapted

The vendored runtime contains the CLI, template, schemas, standalone validators, renderers,
scenario guide, JSON examples, progressive references, brand catalog, migration and deterministic
delivery checks. It requires Node.js 18 or newer only when invoked; ordinary bootstrap operation
remains Python 3.11 standard-library-only. `scripts/run_archify.py` performs the portable Node
preflight and invokes the CLI without a shell.

The local Codex and Claude skills share this neutral runtime and use identical trigger semantics.
They activate manually or by description; no hook, background process, scheduled job, API key, or
automatic model call was added.

Local restrictions relative to upstream:

- the automatic update checker, release manifest, development dependencies, tests, generated
  promotional HTML and repository-only release tooling are not redistributed;
- the HTML template uses its system-font fallback and contains no automatic Google Fonts request;
- remote brand capture remains an explicit CLI capability and may run only when the user asks to
  fetch a specific official brand URL; built-in brand IDs are the offline default;
- preview is opt-in and loopback-only; `visual-check` is opt-in and uses a temporary isolated
  browser profile when compatible Chrome/Chromium is available.

## Security conclusion

Decision: **accept with restrictions**.

Manual review found no secret access, telemetry, arbitrary shell execution, privilege escalation,
or background service. Child processes use fixed Node or platform opener commands with argument
arrays and `shell: false`. Output checks reject input/output aliases and unsafe symlink paths.
Recursive deletion is limited to temporary preview/browser directories created by Archify.
Remote brand capture rejects credentials, private/reserved destinations, non-standard ports,
unbounded responses and mutable unpinned output; it is nevertheless disabled by policy unless the
user explicitly requests that network operation. SkillSpector was not installed, so no optional
scanner was added; the conclusion rests on pinned-source review, static searches and executable
tests, not on a claim of perfect safety.

Upstream package checks for generated brand marks and validators passed. Its packaged `npm test`
is not standalone because release/gallery scripts and documentation live above the exported skill
directory. The directly executed test files confirmed the core CLI, doctor, installed-without-
node_modules delivery, schemas, renderers and output safety; repository-context tests and Windows
symlink tests cannot pass from the helper-exported package. The local suite therefore adds a clean
doctor plus real demo/validate/deliver coverage against the exact vendored payload.

## Update procedure

1. Resolve the new upstream default branch and immutable commit.
2. Fetch only `archify` with:

   ```text
   python <CODEX_HOME>\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo tt-a1i/archify --path archify --ref <commit> --dest <safe-staging>
   ```

3. Compare against this vendored subset; never copy `.git`, `node_modules`, update-notifier state,
   repository-only tooling or promotional artifacts.
4. Reapply and document local offline restrictions, retain the MIT notice, rerun the security
   review, Archify smoke tests, bootstrap suite and Windows E2E, then update this pinned revision.
