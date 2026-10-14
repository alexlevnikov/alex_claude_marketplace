#!/usr/bin/env python3
"""Refresh the bundled skill snapshot from pinned, checked-out upstream repos.

Usage: python3 scripts/update_vendors.py /path/to/vendor-checkouts

The directory must contain one checkout per registry vendor key. Each registry
tool has an upstream_path pointing to its vendor's SKILL.md. This script copies
that skill's directory and resources, pins each source commit, and replaces the
bundle only after all 87 tools have been staged successfully.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from vendor_utils import DEST, PLUGIN, REGISTRY, ignore, tree_hash


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    checkouts = Path(sys.argv[1]).resolve()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    revisions: dict[str, str] = {}
    for vendor, meta in registry["vendors"].items():
        repo = checkouts / vendor
        if not repo.is_dir():
            raise ValueError(f"Missing checkout: {repo}")
        remote = git(repo, "remote", "get-url", "origin").removesuffix(".git")
        if not remote.endswith(meta["repo"].removesuffix(".git").split("github.com/")[-1]):
            raise ValueError(f"Unexpected upstream for {vendor}: {remote}")
        if git(repo, "status", "--porcelain"):
            raise ValueError(f"Dirty upstream checkout: {repo}")
        revisions[vendor] = git(repo, "rev-parse", "HEAD")

    with tempfile.TemporaryDirectory(prefix="design-vendors-stage-", dir=PLUGIN) as temporary:
        stage = Path(temporary) / "vendors"
        stage.mkdir()
        entries = {}
        for name, meta in registry["tools"].items():
            vendor = meta["vendor"]
            source_path = Path(meta["upstream_path"])
            if source_path.is_absolute() or ".." in source_path.parts or source_path.name != "SKILL.md":
                raise ValueError(f"Invalid upstream_path for {name}: {source_path}")
            repo = checkouts / vendor
            source = repo / source_path
            if not source.is_file() or not source.resolve().is_relative_to(repo):
                raise ValueError(f"Missing or out-of-tree upstream skill for {name}: {source}")
            target = stage / name
            shutil.copytree(source.parent, target, symlinks=False, ignore=ignore)
            if not (target / "SKILL.md").is_file():
                raise ValueError(f"No SKILL.md after copying {name}")
            adaptations = []
            if name == "shape":
                skill = target / "SKILL.md"
                old = "../skills/ui-craft/references/state-design.md"
                new = "../ui-craft/references/state-design.md"
                body = skill.read_text(encoding="utf-8")
                if old not in body:
                    raise ValueError("shape's upstream state-design link changed; review the adaptation")
                skill.write_text(body.replace(old, new), encoding="utf-8")
                adaptations.append("Point the state-design link at the bundled ui-craft skill")
            if name == "ui-craft":
                skill = target / "SKILL.md"
                old = "../../examples/animation-storyboard.md"
                new = "examples/animation-storyboard.md"
                body = skill.read_text(encoding="utf-8")
                if old not in body:
                    raise ValueError("ui-craft's storyboard link changed; review the adaptation")
                skill.write_text(body.replace(old, new), encoding="utf-8")
                example = repo / "examples" / "animation-storyboard.md"
                if not example.is_file():
                    raise ValueError(f"Missing ui-craft storyboard: {example}")
                (target / "examples").mkdir(exist_ok=True)
                shutil.copy2(example, target / "examples" / example.name)
                adaptations.append("Bundle and relink the upstream animation storyboard example")
            entries[name] = {
                "vendor": vendor,
                "upstream": registry["vendors"][vendor]["repo"],
                "upstream_revision": revisions[vendor],
                "upstream_path": source_path.as_posix(),
                "sha256": tree_hash(target),
            }
            if adaptations:
                entries[name]["local_adaptations"] = adaptations
        (stage / "LOCK.json").write_text(
            json.dumps({
                "schema_version": 2,
                "source": "current upstream vendor checkouts",
                "previous_tested_inventory": {
                    "repository": "alexlevnikov/design-studio",
                    "revision": "fdfb2460c4d4cf3c986065932106ff79c8074a4d",
                },
                "tools": entries,
            }, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        backup = Path(temporary) / "previous-vendors"
        if DEST.exists():
            os.rename(DEST, backup)
        try:
            os.rename(stage, DEST)
        except Exception:
            if backup.exists():
                os.rename(backup, DEST)
            raise
    print(f"Updated {len(entries)} skills from {len(revisions)} upstream revisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
