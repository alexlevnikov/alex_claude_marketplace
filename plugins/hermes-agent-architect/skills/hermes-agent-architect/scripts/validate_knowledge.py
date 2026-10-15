#!/usr/bin/env python3
"""Validate Hermes knowledge records, links, pinned source and public hygiene."""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT.parents[1]
KINDS = {
    "components": ("component", {"verified", "provisional", "retired"}),
    "decisions": ("decision", {"proposed", "accepted", "superseded"}),
    "patterns": ("pattern", {"draft", "verified", "retired"}),
}
LOCAL_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
LEAKS = {
    "machine checkout path": re.compile(r"/(?:srv/repos|home/ubuntu)/"),
    "tailnet DNS name": re.compile(r"\b[\w-]+\.tail[0-9a-f]+\.ts\.net\b", re.I),
    "Tailscale IP": re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
}


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unclosed frontmatter") from exc
    result = {}
    for line in lines[1:end]:
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def check_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for target in LOCAL_LINK.findall(text):
        target = target.strip().split(" ", 1)[0]
        parts = urlsplit(target)
        if parts.scheme or target.startswith(("#", "/")):
            continue
        local = (path.parent / unquote(parts.path)).resolve()
        if not local.exists():
            errors.append(f"{path.relative_to(PLUGIN)}: missing local link {target}")


def main() -> int:
    errors = []
    catalog = json.loads((ROOT / "data/docs-catalog.json").read_text(encoding="utf-8"))
    pinned_tag = catalog["pinned_tag"]
    upstream = PLUGIN / "upstream/hermes-agent"
    if upstream.is_dir() and not (upstream / "website/docs").is_dir():
        errors.append("pinned upstream exists without website/docs")
    if (upstream / ".git").exists():
        result = subprocess.run(["git", "-C", str(upstream), "rev-parse", "HEAD"], capture_output=True, text=True)
        if result.returncode or result.stdout.strip() != catalog["pinned_commit"]:
            errors.append("pinned upstream commit differs from catalog")
    for folder, (kind, statuses) in KINDS.items():
        for path in sorted((ROOT / "references" / folder).glob("*.md")):
            if path.name == "index.md":
                continue
            try:
                meta = frontmatter(path)
                for key in ("id", "kind", "status", "pinned_tag", "verified_utc"):
                    if not meta.get(key):
                        raise ValueError(f"missing {key}")
                if meta["id"] != path.stem or meta["kind"] != kind:
                    raise ValueError("id or kind mismatch")
                if meta["status"] not in statuses:
                    raise ValueError("invalid status")
                if meta["pinned_tag"] != pinned_tag:
                    raise ValueError("pinned tag differs from catalog")
                date.fromisoformat(meta["verified_utc"])
                if "https://" not in path.read_text(encoding="utf-8") and kind == "component":
                    raise ValueError("component has no primary source URL")
            except ValueError as exc:
                errors.append(f"{path.relative_to(PLUGIN)}: {exc}")
            check_links(path, errors)
    for path in sorted(ROOT.rglob("*.md")):
        if "upstream" not in path.parts and (path.parent.name in {"components", "decisions", "patterns"} or path.name == "SKILL.md"):
            check_links(path, errors)
    for folder, dirs, files in os.walk(PLUGIN):
        dirs[:] = [name for name in dirs if name != "upstream" and name != "__pycache__"]
        for name in files:
            path = Path(folder) / name
            if path.suffix not in {".md", ".py", ".json", ".yaml"}:
                continue
            data = path.read_text(encoding="utf-8")
            for leak_name, pattern in LEAKS.items():
                if pattern.search(data):
                    errors.append(f"{path.relative_to(PLUGIN)}: possible {leak_name}")
    if errors:
        print("Knowledge validation failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print("- " + error, file=sys.stderr)
        return 1
    print("Hermes knowledge OK: records, links, pinned layout and public hygiene")
    return 0


if __name__ == "__main__":
    sys.exit(main())
