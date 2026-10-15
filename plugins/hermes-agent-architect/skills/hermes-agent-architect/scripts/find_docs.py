#!/usr/bin/env python3
"""Search the Hermes documentation catalog and show tagged local files."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "docs-catalog.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Words to match in title, section or URL")
    parser.add_argument("--tag-only", action="store_true", help="Only docs found in the pinned tag")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = catalog["entries"]
    words = [word.casefold() for word in args.query]
    for entry in entries:
        if args.tag_only and not entry["tag_doc_path"]:
            continue
        searchable = " ".join([entry["title"], entry["url"], *entry["sections"]]).casefold()
        if not all(word in searchable for word in words):
            continue
        print(f"{entry['title']} [{', '.join(entry['sections'])}]")
        print(f"  current: {entry['url']}")
        if entry["tag_doc_path"]:
            print(f"  v2026.9.14: {ROOT / 'upstream/hermes-agent/website/docs' / entry['tag_doc_path']}")
        else:
            print("  v2026.9.14: no matching documentation path; verify in source")
    indexed_paths = {entry["tag_doc_path"] for entry in entries}
    for path in catalog["tag_documents"]:
        if path in indexed_paths or not all(word in path.casefold() for word in words):
            continue
        print(f"Tagged-only document: {path}")
        print(f"  v2026.9.14: {ROOT / 'upstream/hermes-agent/website/docs' / path}")


if __name__ == "__main__":
    main()
