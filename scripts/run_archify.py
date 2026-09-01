#!/usr/bin/env python3
"""Run the vendored Archify CLI with a clear optional-Node preflight."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


MIN_NODE = (18, 0, 0)


def node_candidates() -> list[str]:
    candidates: list[str] = []
    configured = os.environ.get("ARCHIFY_NODE", "").strip()
    if configured:
        candidates.append(configured)
    discovered = shutil.which("node")
    if discovered:
        candidates.append(discovered)
    return list(dict.fromkeys(candidates))


def probe_node(candidate: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [candidate, "-p", "process.versions.node"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, str(exc)
    version = result.stdout.strip()
    try:
        parts = tuple(int(part) for part in version.split(".")[:3])
    except ValueError:
        return False, version or result.stderr.strip() or "could not read version"
    if result.returncode == 0 and parts >= MIN_NODE:
        return True, version
    return False, version or result.stderr.strip() or "could not start"


def resolve_node() -> tuple[str, str]:
    diagnostics: list[str] = []
    for candidate in node_candidates():
        valid, detail = probe_node(candidate)
        if valid:
            return candidate, detail
        diagnostics.append(f"{candidate}: {detail}")
    checked = "; ".join(diagnostics) if diagnostics else "no node executable found"
    raise RuntimeError(
        "Archify requires optional Node.js 18 or newer. Install Node.js or set "
        f"ARCHIFY_NODE to node.exe. Checked: {checked}."
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        args = ["doctor"]
    project_root = Path(__file__).resolve().parents[1]
    cli = project_root / "third_party" / "archify" / "bin" / "archify.mjs"
    if not cli.is_file():
        print(f"ERROR: vendored Archify CLI is missing: {cli}", file=sys.stderr)
        return 1
    try:
        node, _version = resolve_node()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    try:
        result = subprocess.run([node, str(cli), *args], check=False)
    except OSError as exc:
        print(f"ERROR: could not start Archify: {exc}", file=sys.stderr)
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
