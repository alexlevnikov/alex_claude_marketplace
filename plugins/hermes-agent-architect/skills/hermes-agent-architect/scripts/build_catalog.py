#!/usr/bin/env python3
"""Build a version-aware directory of official Hermes documentation URLs."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


INDEX_URL = "https://hermes-agent.nousresearch.com/docs/llms.txt"
DOC_LINK = re.compile(r"^- \[([^]]+)\]\((https://hermes-agent\.nousresearch\.com/docs/[^)]+)\)")


def locate_tag_doc(docs_root: Path, url: str) -> str | None:
    slug = urlparse(url).path.removeprefix("/docs/").rstrip("/")
    candidates = (
        f"{slug}.md",
        f"{slug}.mdx",
        f"{slug}/index.md",
        f"{slug}/index.mdx",
    )
    return next((candidate for candidate in candidates if (docs_root / candidate).is_file()), None)


def git_commit(upstream: Path, revision: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(upstream), "rev-parse", "--verify", revision],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def build_catalog(index_bytes: bytes, upstream: Path, captured_at: str, tag: str) -> dict:
    docs_root = upstream / "website" / "docs"
    if not docs_root.is_dir():
        raise ValueError(f"Hermes documentation directory not found: {docs_root}")
    commit = git_commit(upstream, "HEAD")
    if git_commit(upstream, f"{tag}^{{commit}}") != commit:
        raise ValueError(f"Checkout HEAD does not match {tag}")
    section = ""
    entries_by_url: dict[str, dict] = {}
    for line in index_bytes.decode("utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:]
            continue
        match = DOC_LINK.match(line)
        if not match:
            continue
        title, url = match.groups()
        if url in entries_by_url:
            if section not in entries_by_url[url]["sections"]:
                entries_by_url[url]["sections"].append(section)
            continue
        entries_by_url[url] = {
            "title": title,
            "url": url,
            "sections": [section],
            "tag_doc_path": locate_tag_doc(docs_root, url),
        }
    return {
        "schema_version": 1,
        "captured_at_utc": captured_at,
        "source_index_url": INDEX_URL,
        "source_index_sha256": hashlib.sha256(index_bytes).hexdigest(),
        "pinned_tag": tag,
        "pinned_commit": commit,
        "tag_documents": sorted(
            str(path.relative_to(docs_root))
            for path in docs_root.rglob("*")
            if path.is_file() and path.suffix in {".md", ".mdx"}
        ),
        "entries": list(entries_by_url.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index-file", required=True, type=Path)
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--captured-at", required=True, help="UTC ISO-8601 timestamp")
    parser.add_argument("--tag", default="v2026.9.14", help="Tag checked out in upstream")
    args = parser.parse_args()
    catalog = build_catalog(args.index_file.read_bytes(), args.upstream, args.captured_at, args.tag)
    print(json.dumps(catalog, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
