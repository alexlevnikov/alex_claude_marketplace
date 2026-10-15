#!/usr/bin/env python3
"""Search current documentation URLs and verify matching pinned local files."""

import argparse
import json
from pathlib import Path
import sys

from resolve_upstream import UpstreamUnavailable, resolve_upstream, verified_file


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/docs-catalog.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Words to match in title, section or URL")
    parser.add_argument("--tag-only", action="store_true", help="Only docs cataloged in the pinned tag")
    parser.add_argument("--require-upstream", action="store_true", help="Fail if pinned local evidence is unavailable")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    try:
        source = resolve_upstream()
    except UpstreamUnavailable as exc:
        print(str(exc), file=sys.stderr)
        source = None
    missing = source is None

    def show_pinned(path: str) -> None:
        nonlocal missing
        if source:
            try:
                print(f"  {catalog['pinned_tag']}: {verified_file(source, 'website/docs/' + path)}")
                return
            except UpstreamUnavailable as exc:
                print(str(exc), file=sys.stderr)
                missing = True
        print(f"  {catalog['pinned_tag']}: unavailable locally (catalog path: {path})")

    words = [word.casefold() for word in args.query]
    for entry in catalog["entries"]:
        if args.tag_only and not entry["tag_doc_path"]:
            continue
        searchable = " ".join([entry["title"], entry["url"], *entry["sections"]]).casefold()
        if not all(word in searchable for word in words):
            continue
        print(f"{entry['title']} [{', '.join(entry['sections'])}]")
        print(f"  current: {entry['url']}")
        if entry["tag_doc_path"]:
            show_pinned(entry["tag_doc_path"])
        else:
            print(f"  {catalog['pinned_tag']}: no cataloged documentation match; verify in source")
    indexed_paths = {entry["tag_doc_path"] for entry in catalog["entries"]}
    for path in catalog["tag_documents"]:
        if path in indexed_paths or not all(word in path.casefold() for word in words):
            continue
        print(f"Tagged-only document: {path}")
        show_pinned(path)
    return 2 if args.require_upstream and missing else 0


if __name__ == "__main__":
    sys.exit(main())
