#!/usr/bin/env python3
"""resolve.py — find where a design tool's SKILL.md actually lives, and say how to load it.

The router (skills/design-tools) and every generated command (commands/<tool>.md) call this at the
moment a tool has been chosen. It prints a small manifest the model reads: the absolute SKILL.md
path, its directory (so the skill's relative `references/` resolve), the ui-craft base when the tool
is a lens, and whether the tool can be invoked by name with the Skill tool or must be read and
followed.

Search order (first hit wins):
  1. $DESIGN_TOOLS_ROOTS            colon-separated directories, each holding <tool>/SKILL.md
  2. .claude/design-tools.local.md  walk-up from $CLAUDE_PROJECT_DIR or $PWD; YAML `roots:` list
  3. project scope                  <dir>/.claude/skills/<tool>/SKILL.md, walking up from cwd
  4. user scope                     ~/.claude/skills/<tool>/SKILL.md
  5. plugin-vendored                <plugin>/vendors/<tool>/SKILL.md
  6. registry roots                 registry/tools.json → roots[].path

Hits in 3 and 4 are visible to the Skill tool by name (`load: skill`); everything else is
`load: read` — open the file and follow it.

Usage:
  resolve.py <tool>            text manifest, exit 0 on hit, 1 on MISSING
  resolve.py <tool> --json     same, as JSON
  resolve.py --all [--json]    one line per registry tool; exit 1 if any is MISSING
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = PLUGIN_ROOT / "registry" / "tools.json"


def load_registry() -> dict:
    with REGISTRY.open(encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- roots -------------------------

def _walk_up(start: Path):
    cur = start.resolve()
    while True:
        yield cur
        if cur.parent == cur:
            return
        cur = cur.parent


def _project_start() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env) if env else Path.cwd()


def _local_settings_roots() -> list[tuple[str, Path]]:
    """`.claude/design-tools.local.md` — YAML frontmatter with a `roots:` list. Minimal parser:
    we only need a list of scalars under one key."""
    for d in _walk_up(_project_start()):
        f = d / ".claude" / "design-tools.local.md"
        if not f.is_file():
            continue
        roots: list[tuple[str, Path]] = []
        in_fm = False
        in_roots = False
        for raw in f.read_text(encoding="utf-8").splitlines():
            line = raw.rstrip()
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if not in_fm:
                continue
            if line.startswith("roots:"):
                in_roots = True
                continue
            if in_roots:
                s = line.strip()
                if s.startswith("- "):
                    p = s[2:].strip().strip("\"'")
                    roots.append((f"local:{f}", Path(os.path.expanduser(p))))
                elif s and not line.startswith((" ", "\t")):
                    in_roots = False
        return roots
    return []


def candidate_roots(reg: dict) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    env = os.environ.get("DESIGN_TOOLS_ROOTS", "")
    for p in filter(None, env.split(":")):
        out.append(("env:DESIGN_TOOLS_ROOTS", Path(os.path.expanduser(p))))
    out += _local_settings_roots()
    home = Path.home().resolve()
    for d in _walk_up(_project_start()):
        if d == home or home not in d.parents:
            break  # do not climb to or past $HOME — user scope is listed separately below
        out.append(("project", d / ".claude" / "skills"))
    out.append(("user", Path.home() / ".claude" / "skills"))
    out.append(("vendored", PLUGIN_ROOT / "vendors"))
    for r in reg.get("roots", []):
        out.append((f"root:{r['name']}", Path(os.path.expanduser(r["path"]))))
    return out


# ---------------------------------------------------------------- resolve -----------------------

def find_skill(tool: str, roots: list[tuple[str, Path]]):
    for kind, root in roots:
        f = root / tool / "SKILL.md"
        if f.is_file():
            return kind, f.resolve()
    return None, None


def resolve(tool: str, reg: dict) -> dict:
    tools = reg.get("tools", {})
    meta = tools.get(tool)
    vendors = reg.get("vendors", {})
    roots = candidate_roots(reg)
    kind, skill = find_skill(tool, roots)

    out: dict = {
        "tool": tool,
        "known": meta is not None,
    }
    if meta:
        v = vendors.get(meta["vendor"], {})
        out.update({
            "vendor": meta["vendor"],
            "vendor_repo": v.get("repo"),
            "mode": meta["mode"],
            "class": meta["class"],
            "group": meta["group"],
            "routable": meta["routable"],
            "for": meta.get("for"),
            "not_for": meta.get("not_for"),
        })
    if skill is None:
        out["status"] = "MISSING"
        out["searched"] = [f"{k} → {p}" for k, p in roots]
        return out

    out["status"] = "OK"
    out["skill"] = str(skill)
    out["dir"] = str(skill.parent)
    out["found_in"] = kind
    out["load"] = "skill" if kind in ("project", "user") else "read"

    base = meta.get("base") if meta else None
    if base:
        bkind, bskill = find_skill(base, roots)
        out["base"] = str(bskill) if bskill else "MISSING"
        out["base_found_in"] = bkind
    return out


# ---------------------------------------------------------------- output ------------------------

def fmt_text(r: dict) -> str:
    lines = [f"tool: {r['tool']}"]
    if r.get("known"):
        lines.append(f"vendor: {r['vendor']} ({r.get('vendor_repo') or '?'})")
        lines.append(f"mode: {r['mode']}   class: {r['class']}   group: {r['group']}   "
                     f"routable: {'yes' if r['routable'] else 'no — direct engagement only'}")
    else:
        lines.append("vendor: ? (not in registry/tools.json — add it, then run scripts/build.py)")
    if r["status"] == "MISSING":
        lines.append("status: MISSING — no <root>/%s/SKILL.md in any root searched:" % r["tool"])
        lines += [f"  - {s}" for s in r["searched"]]
        lines.append("hint: install into the project (design-studio/scripts/skillset.sh install …), "
                     "or add the directory that holds it to DESIGN_TOOLS_ROOTS or "
                     ".claude/design-tools.local.md `roots:`.")
        return "\n".join(lines)
    lines.append(f"status: OK   found_in: {r['found_in']}")
    lines.append(f"skill: {r['skill']}")
    lines.append(f"dir: {r['dir']}")
    if r["load"] == "skill":
        lines.append("load: skill — invocable by name with the Skill tool (project/user scope)")
    else:
        lines.append("load: read — Read the `skill:` file and follow it as if invoked; "
                     "relative references resolve against `dir:`")
    if "base" in r:
        lines.append(f"base: {r['base']}   ← ui-craft lens: read the base FIRST"
                     + ("" if r["base"] != "MISSING" else "  (MISSING — the lens will run without its anti-slop rules)"))
    if r.get("for"):
        lines.append(f"for: {r['for']}")
    if r.get("not_for"):
        lines.append(f"not_for: {r['not_for']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    reg = load_registry()

    if "--all" in argv:
        results = [resolve(t, reg) for t in reg["tools"]]
        if as_json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            w = max(len(r["tool"]) for r in results)
            for r in results:
                where = r.get("found_in", "-")
                print(f"{r['tool']:<{w}}  {r['status']:<7}  {where:<22}  {r.get('skill', '')}")
            missing = [r["tool"] for r in results if r["status"] == "MISSING"]
            print(f"\n{len(results) - len(missing)}/{len(results)} resolved"
                  + (f"; MISSING: {', '.join(missing)}" if missing else ""))
        return 1 if any(r["status"] == "MISSING" for r in results) else 0

    if not args:
        print(__doc__)
        return 2
    r = resolve(args[0], reg)
    print(json.dumps(r, indent=2, ensure_ascii=False) if as_json else fmt_text(r))
    return 0 if r["status"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
