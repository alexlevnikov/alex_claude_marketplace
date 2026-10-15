#!/usr/bin/env python3
"""Search the authored Hermes component library and research files."""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH_ROOTS = (ROOT / "references", ROOT / "docs")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="Words to find in the authored corpus")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()
    terms = [term.casefold() for term in args.query]
    count = 0
    for folder in SEARCH_ROOTS:
        for path in sorted(folder.rglob("*.md")):
            body = path.read_text(encoding="utf-8")
            if not all(term in body.casefold() or term in path.name.casefold() for term in terms):
                continue
            lines = body.splitlines()
            heading_at = next((i for i, line in enumerate(lines) if line.startswith("# ")), -1)
            title = lines[heading_at][2:] if heading_at >= 0 else path.stem
            match = next((line.strip() for line in lines[heading_at + 1:] if any(term in line.casefold() for term in terms)), "")
            print(f"{path.relative_to(ROOT)}: {title}")
            if match:
                print("  " + re.sub(r"\s+", " ", match)[:220])
            count += 1
            if count >= args.limit:
                return
    if not count:
        print("No authored knowledge matches; try scripts/find_docs.py for official documentation.")


if __name__ == "__main__":
    main()
