#!/usr/bin/env python3
"""Verify the curated design inventory and its attribution before packaging."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from vendor_utils import PLUGIN, REGISTRY, tree_hash


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    lock = json.loads((PLUGIN / "vendors" / "LOCK.json").read_text(encoding="utf-8"))
    vendors = PLUGIN / "vendors"
    expected = set(registry["tools"])
    actual = {p.name for p in vendors.iterdir() if p.is_dir()}
    errors = []
    if expected != actual or expected != set(lock["tools"]):
        errors.append(f"inventory mismatch: registry={len(expected)}, dirs={len(actual)}, lock={len(lock['tools'])}")
    for name in sorted(expected & actual & set(lock["tools"])):
        directory = vendors / name
        entry = lock["tools"][name]
        if not (directory / "SKILL.md").is_file():
            errors.append(f"{name}: SKILL.md missing")
        if any(p.is_symlink() for p in directory.rglob("*")):
            errors.append(f"{name}: contains symlink")
        if tree_hash(directory) != entry["sha256"]:
            errors.append(f"{name}: content differs from pinned upstream snapshot")
        if entry["vendor"] != registry["tools"][name]["vendor"]:
            errors.append(f"{name}: vendor differs from registry")
        if entry.get("upstream_path") != registry["tools"][name].get("upstream_path"):
            errors.append(f"{name}: upstream path differs from registry")
        if len(entry.get("upstream_revision", "")) != 40:
            errors.append(f"{name}: upstream revision missing")
    ledger = (PLUGIN / "third-party" / "README.md").read_text(encoding="utf-8")
    for vendor in registry["vendors"]:
        if f"| `{vendor}` |" not in ledger:
            errors.append(f"{vendor}: attribution missing")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    revisions = {x["upstream_revision"] for x in lock["tools"].values()}
    print(f"Bundle OK: {len(expected)} skills from {len(revisions)} pinned upstream revisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
