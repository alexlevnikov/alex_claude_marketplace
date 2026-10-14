#!/usr/bin/env python3
"""Resolve an explicit design-tools vendor or vendor:skill selection.

Usage: python3 scripts/invoke.py [design-tools:]<vendor>[:<skill>]
"""

from __future__ import annotations

import sys

import resolve


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    selector = argv[0].lstrip("/")
    if selector.startswith("design-tools:"):
        selector = selector[len("design-tools:"):]
    parts = selector.split(":")
    if len(parts) not in (1, 2) or not all(parts):
        print(f"Invalid selector: {argv[0]}", file=sys.stderr)
        return 2
    vendor = parts[0]
    registry = resolve.load_registry()
    info = registry["vendors"].get(vendor)
    if info is None:
        print(f"Unknown vendor: {vendor}. Available: {', '.join(registry['vendors'])}", file=sys.stderr)
        return 2
    if len(parts) == 1:
        print(f"selector: design-tools:{vendor}")
        print(f"vendor: {info['display']}")
        if info.get("master"):
            print(f"entry: master skill {info['master']}")
            result = resolve.resolve(info["master"], registry)
            print(resolve.fmt_text(result))
            return 0 if result["status"] == "OK" else 1
        names = [name for name, meta in registry["tools"].items() if meta["vendor"] == vendor]
        print("entry: vendor hub — choose one of these skills:")
        for name in names:
            print(f"  design-tools:{vendor}:{name}")
        return 0
    tool = parts[1]
    meta = registry["tools"].get(tool)
    if meta is None or meta["vendor"] != vendor:
        print(f"Unknown skill for {vendor}: {tool}", file=sys.stderr)
        return 2
    print(f"selector: design-tools:{vendor}:{tool}")
    result = resolve.resolve(tool, registry)
    print(resolve.fmt_text(result))
    return 0 if result["status"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
