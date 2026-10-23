#!/usr/bin/env python3
"""Check the marketplace, role catalog, and bundled design inventory."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / ".claude-plugin" / "marketplace.json"
ROLES = ROOT / "roles" / "catalog.json"


def fail(message: str) -> None:
    raise ValueError(message)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")


def check_catalog() -> dict[str, Path]:
    catalog = read_json(CATALOG)
    if not catalog.get("name") or not catalog.get("plugins"):
        fail("marketplace needs a name and at least one plugin")
    installed: dict[str, Path] = {}
    for entry in catalog["plugins"]:
        name, source = entry.get("name"), entry.get("source")
        if not isinstance(name, str) or name in installed:
            fail(f"duplicate or invalid plugin name: {name!r}")
        expected_source = f"./plugins/{name}"
        if isinstance(source, dict):
            if source != {"source": "local", "path": expected_source}:
                fail(f"{name}: local source must point to {expected_source}")
            source_path = source["path"]
        elif source == expected_source:
            source_path = source
        else:
            fail(f"{name}: source must be {expected_source}")
        root = ROOT / source_path
        if root.is_symlink():
            fail(f"{name}: pack directory must not be a symlink")
        manifest_path = root / ".claude-plugin" / "plugin.json"
        manifest = read_json(manifest_path)
        if manifest.get("name") != name:
            fail(f"{name}: manifest name differs from marketplace")
        if entry.get("version") is not None and manifest.get("version") != entry["version"]:
            fail(f"{name}: manifest and marketplace versions differ")
        if not manifest.get("version"):
            fail(f"{name}: manifest version is missing")
        skills = list((root / "skills").glob("*/SKILL.md"))
        if not skills:
            fail(f"{name}: no top-level skills")
        for directory in (root / "skills").iterdir():
            if directory.is_dir() and not (directory / "SKILL.md").is_file():
                fail(f"{name}: {directory.name} has no SKILL.md")
        if (root / ".mcp.json").is_file():
            read_json(root / ".mcp.json")
        installed[name] = root
    actual = {path.name for path in (ROOT / "plugins").iterdir() if path.is_dir()}
    if actual != set(installed):
        fail(f"plugin directories differ from marketplace: {sorted(actual ^ set(installed))}")
    print(f"Catalog OK: {len(installed)} packs")
    return installed


def check_roles(packs: dict[str, Path]) -> None:
    roles = read_json(ROLES)
    if roles.get("schema_version") != 1:
        fail("unsupported roles/catalog.json schema")
    seen: set[str] = set()
    for role in roles.get("roles", []):
        role_id = role.get("id")
        if not isinstance(role_id, str) or role_id in seen:
            fail(f"duplicate or invalid role id: {role_id!r}")
        seen.add(role_id)
        guide = role.get("guide")
        if guide != f"roles/{role_id}.md" or not (ROOT / guide).is_file():
            fail(f"{role_id}: missing role guide")
        required = role.get("requires") or []
        optional = role.get("optional") or []
        if not required or len(set(required + optional)) != len(required + optional):
            fail(f"{role_id}: invalid or duplicate pack dependency")
        if set(required + optional) - packs.keys():
            fail(f"{role_id}: references an unknown pack")
        for entry in role.get("entry_skills", []):
            plugin, separator, skill = entry.partition(":")
            if not separator or plugin not in packs:
                fail(f"{role_id}: invalid entry skill {entry}")
            if plugin not in required + optional:
                fail(f"{role_id}: entry skill {entry} is not a dependency")
            if not (packs[plugin] / "skills" / skill / "SKILL.md").is_file():
                fail(f"{role_id}: missing entry skill {entry}")
    if not seen:
        fail("role catalog is empty")
    print(f"Roles OK: {len(seen)} guides")


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    try:
        packs = check_catalog()
        check_roles(packs)
        hermes = packs["hermes-agent-architect"]
        run(sys.executable, "-B", "-m", "unittest", "discover", "-s", str(hermes / "tests"), "-v")
        run(sys.executable, "-B", str(hermes / "skills/hermes-agent-architect/scripts/validate_knowledge.py"))
        run(sys.executable, "-B", str(hermes / "skills/openviking-memory/scripts/verify_docs.py"))
        design = packs["design-tools"] / "scripts"
        run(sys.executable, str(design / "check_bundle.py"))
        run(sys.executable, str(design / "build.py"), "--check")
        run(sys.executable, str(design / "export_vendor_plugins.py"), "--check")
        # Vendored snapshots are pinned by hash. Preserve upstream whitespace;
        # check authored files here and let check_bundle/export verify copies.
        authored = (
            "--", ".", ":(exclude,glob)plugins/design-*/vendors/**",
            ":(exclude,glob)plugins/hermes-agent-architect/skills/openviking-memory/references/upstream/**",
        )
        run("git", "diff", "--check", *authored)
        run("git", "diff", "--cached", "--check", *authored)
        print("Library OK")
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"Library check failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
