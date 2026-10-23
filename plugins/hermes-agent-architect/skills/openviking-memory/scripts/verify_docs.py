#!/usr/bin/env python3
"""Verify the pinned OpenViking documentation copy against Git blob hashes."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "references" / "upstream"


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    expected = {item["path"]: item["blob_sha"] for item in manifest["files"]}
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md")}
    errors = []
    for path in sorted(expected):
        file = ROOT / path
        if not file.is_file():
            errors.append(f"missing: {path}")
        elif blob_sha(file.read_bytes()) != expected[path]:
            errors.append(f"hash mismatch: {path}")
    for path in sorted(actual - set(expected)):
        errors.append(f"unexpected: {path}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Verified {len(expected)} OpenViking docs at {manifest['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
