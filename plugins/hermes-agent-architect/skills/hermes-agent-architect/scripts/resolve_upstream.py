#!/usr/bin/env python3
"""Locate and verify the catalog-pinned Hermes source without changing it."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/docs-catalog.json"
SUBMODULE = Path("plugins/hermes-agent-architect/upstream/hermes-agent")


class UpstreamUnavailable(RuntimeError):
    """No safe local source is available for a pinned-source claim."""


def git(root: Path, *args: str) -> str:
    # Reading a skill must also work in a read-only Codex session. Do not let
    # Git refresh the index or inherit a caller's unrelated Git worktree.
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(root), *args],
            env=env, text=True, capture_output=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise UpstreamUnavailable("Git verification could not run") from exc
    if result.returncode:
        raise UpstreamUnavailable("Git verification failed")
    return result.stdout.strip()


def resolve_upstream(override: str | None = None) -> dict[str, str]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    chosen = override or os.environ.get("HERMES_ARCHITECT_UPSTREAM")
    if chosen:
        candidates = [Path(chosen).expanduser()]
    else:
        candidates = [ROOT.parents[1] / "upstream/hermes-agent",
                      Path.home() / ".local/share/alex-claude-marketplace" / SUBMODULE]
    rejected = []
    for path in dict.fromkeys(p.resolve() for p in candidates):
        try:
            # rev-parse alone would accept an empty submodule directory by
            # walking up to its parent marketplace repository.
            if not (path / ".git").exists() or Path(git(path, "rev-parse", "--show-toplevel")).resolve() != path:
                raise UpstreamUnavailable("not an initialized Git repository root")
            commit = git(path, "rev-parse", "HEAD")
            if commit != catalog["pinned_commit"]:
                raise UpstreamUnavailable(f"commit {commit} differs from required {catalog['pinned_commit']}")
            if not (path / "website/docs").is_dir():
                raise UpstreamUnavailable("website/docs is missing")
            flags = git(path, "ls-files", "-v", "-z").split("\0")
            if any(item and (item[0].islower() or item[0] == "S") for item in flags):
                raise UpstreamUnavailable("index flags can hide local changes; use a full, ordinary checkout")
            if git(path, "status", "--porcelain=v1", "--untracked-files=all"):
                raise UpstreamUnavailable("local changes exist; source left untouched")
            return {"status": "available", "tag": catalog["pinned_tag"],
                    "commit": commit, "root": str(path), "docs": str(path / "website/docs")}
        except UpstreamUnavailable as exc:
            rejected.append(f"{path}: {exc}")
    raise UpstreamUnavailable(
        f"Pinned upstream unavailable ({catalog['pinned_tag']} / {catalog['pinned_commit']}). "
        + "; ".join(rejected)
        + ". See the plugin README for external-checkout setup. Current docs and catalog metadata are not pinned-source evidence."
    )


def verified_file(source: dict[str, str], relative: str) -> Path:
    root = Path(source["root"])
    requested = Path(relative)
    file = (root / requested).resolve()
    if requested.is_absolute() or ".." in requested.parts or not file.is_relative_to(root):
        raise UpstreamUnavailable("file must be a relative path inside pinned upstream")
    if not file.is_file():
        raise UpstreamUnavailable(f"pinned file is missing: {relative}")
    # Verify actual bytes as well as HEAD: assume-unchanged/ignored worktree
    # content must never pass for a file from the pinned commit.
    expected = git(root, "rev-parse", f"{source['commit']}:{requested.as_posix()}")
    if git(root, "hash-object", "--no-filters", "--", str(file)) != expected:
        raise UpstreamUnavailable(f"pinned file has local changes: {relative}")
    return file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", help="Explicit upstream root (otherwise environment, bundled source, then standard checkout)")
    parser.add_argument("--file", help="Verify and print a file relative to the upstream root")
    parser.add_argument("--json", action="store_true", help="Print verification evidence as JSON")
    args = parser.parse_args()
    try:
        source = resolve_upstream(args.upstream)
        if args.file:
            source["file"] = str(verified_file(source, args.file))
    except (UpstreamUnavailable, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        if args.json:
            print(json.dumps({"status": "unavailable", "reason": str(exc)}))
        return 2
    print(json.dumps(source, indent=2) if args.json else source.get("file", source["root"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
