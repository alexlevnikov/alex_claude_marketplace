"""Shared paths and hashing for the bundled vendor snapshot."""

from __future__ import annotations

import hashlib
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
REGISTRY = PLUGIN / "registry" / "tools.json"
DEST = PLUGIN / "vendors"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {".git", ".DS_Store", "__pycache__"}}
