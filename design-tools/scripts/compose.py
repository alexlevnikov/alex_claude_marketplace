#!/usr/bin/env python3
"""compose.py — turn a selected set of tools into a prompt skeleton with resolved load blocks.

    compose.sh <tool|command …> [--task "<words>"] [--slug <slug>] [--project <dir>] [--json]

Accepts tool names (`typeset`) or command names (`ui-craft-typeset`). Prints the skeleton of
`.design-tools/<slug>.prompt.md` as specified in DESIGN-TOOLS-DISCOVERY.md §4: everything that is
mechanical — ordering (read-only → modifiers → writes, ui-craft base first), `Load:` lines from the
resolver, guardrails, report format — is filled in; everything that needs judgement is left as an
`<angle-bracket>` placeholder for the model to fill before writing the file.

Exit 2 on: an unknown name, two orchestrator-class tools in one set, no tools.
A tool the resolver cannot find is kept, with `Load: MISSING — …`, and counted in the summary line
so the discovery step can flag it before offering to run.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve as R  # noqa: E402

ORDER = {"judge": 0, "lookup": 0, "modifier": 1, "pass": 2, "technique": 2, "phase": 2,
         "preset": 3, "base": 3, "orchestrator": 3}


def cmd_name(tool: str, meta: dict) -> str:
    if meta.get("command"):
        return meta["command"]
    v = meta["vendor"]
    return tool if (tool == v or tool.startswith(v + "-")) else f"{v}-{tool}"


def to_tool(name: str, reg: dict) -> str | None:
    tools = reg["tools"]
    if name in tools:
        return name
    for t, m in tools.items():
        if cmd_name(t, m) == name:
            return t
    # vendor key alone → that vendor's master
    v = reg["vendors"].get(name)
    if v and v.get("master"):
        return v["master"]
    return None


def slugify(text: str) -> str:
    words = re.findall(r"[\w]+", text.lower(), flags=re.UNICODE)
    s = "-".join(words[:6]) or "task"
    return re.sub(r"-+", "-", s).strip("-")[:60]


def find_up(start: Path, rel: str) -> Path | None:
    cur = start.resolve()
    while True:
        cand = cur / rel
        if cand.exists():
            return cand
        if cur.parent == cur:
            return None
        cur = cur.parent


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    opts = {"--task": "", "--slug": "", "--project": ""}
    names: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in opts:
            opts[a] = argv[i + 1] if i + 1 < len(argv) else ""
            i += 2
            continue
        if not a.startswith("--"):
            names.append(a)
        i += 1
    if not names:
        print(__doc__)
        return 2

    reg = R.load_registry()
    project = Path(opts["--project"] or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
    task = opts["--task"]
    slug = opts["--slug"] or slugify(task)

    selected: list[str] = []
    unknown: list[str] = []
    for n in names:
        t = to_tool(n, reg)
        (selected if t else unknown).append(t or n)
    if unknown:
        print(f"error: unknown tool/command name(s): {', '.join(unknown)} — see wiki/README.md or "
              f"`bash scripts/resolve.sh --all`", file=sys.stderr)
        return 2
    # de-duplicate, keep first occurrence
    seen = set()
    selected = [t for t in selected if not (t in seen or seen.add(t))]

    metas = {t: reg["tools"][t] for t in selected}
    orchestrators = [t for t in selected if metas[t]["class"] in ("orchestrator", "base", "preset")]
    if len(orchestrators) > 1:
        print(f"error: {len(orchestrators)} orchestrator-class tools selected ({', '.join(orchestrators)}) — "
              f"one per context. Pick one, or split into two prompts.", file=sys.stderr)
        return 2

    ordered = sorted(selected, key=lambda t: (ORDER.get(metas[t]["class"], 2), selected.index(t)))
    # ensure full-output-enforcement is present when anything long will be written
    writers = [t for t in ordered if metas[t]["mode"].startswith("W") and metas[t]["class"] not in ("lookup", "judge")]
    foe_needed = bool(writers) and "full-output-enforcement" not in ordered
    foe_res = R.resolve("full-output-enforcement", reg) if foe_needed else None

    blocks = []
    missing = []
    for n, t in enumerate(ordered, 1):
        m = metas[t]
        v = reg["vendors"][m["vendor"]]
        res = R.resolve(t, reg)
        rw = "read-only" if (not m["mode"].startswith("W") or m["class"] in ("lookup", "judge")) else "writes"
        if m["mode"] == "W/R":
            rw = "writes (build mode) / read-only (audit mode)"
        if res["status"] == "OK":
            load = f"{res['load']} · {res['skill']}"
            if res.get("base") and res["base"] != "MISSING":
                load += f" · base first: {res['base']}"
            elif res.get("base") == "MISSING":
                load += " · base MISSING (ui-craft not installed — the lens will run without its rules)"
        else:
            load = "MISSING — not installed on this machine; install it or add its directory to DESIGN_TOOLS_ROOTS before running"
            missing.append(t)
        note = ""
        if m["class"] in ("orchestrator", "base", "preset"):
            note = "\nRuns as the vendor designed it — its own discovery, modes, knobs and report; the other tools serve around it."
        if m["class"] == "modifier":
            note = "\nModifier — keep in force for every write below."
        blocks.append(f"""### {n}. {t} — {v['display']} — {rw}
Role in this task: <one sentence: what this tool is expected to do for THIS task>
Command: /design-tools:{cmd_name(t, m)}
Load: {load}
Does: {m['does']}{note}""")

    brand = find_up(project, "BRAND-CONTRACT.md")
    brief = find_up(project, ".ui-craft/brief.md")
    out_path = project / ".design-tools" / f"{slug}.prompt.md"

    guard = [
        "- One orchestrator-class tool at most" + (f" — here: `{orchestrators[0]}`, and it runs as the vendor designed it." if orchestrators else "; none selected — this is a composition of passes."),
        "- Read-only tools run first and their findings are carried into every write.",
    ]
    if writers:
        guard.append("- full-output-enforcement is in force for every write: no placeholders, no `// rest here`, no truncated files."
                     + (f"\n  Load: {foe_res['load']} · {foe_res['skill']}" if foe_res and foe_res["status"] == "OK" else ""))
    guard += [
        "- Change no files outside the target; say so if a tool wants to.",
        "- A tool whose Load line says MISSING is not run and not improvised — report it as skipped.",
    ]

    text = f"""# <Task title — five words or fewer>
Written by design-tools discover on {date.today().isoformat()}. Tools selected by the user from the discovery list.

## Task
<the request restated in one paragraph; every assumption made explicit>
Original words: {task or '<paste the user’s words>'}

## Context
- Brand contract: {brand if brand else 'none found walking up from ' + str(project) + ' — ask before any write'}
- Target: <files / URL / component — exact paths>
- Project memory: {brief if brief else 'no .ui-craft/brief.md found'}
- Working directory: {project}

## Tools, in order
{chr(10).join(blocks)}

## Procedure
1. Read the brand contract and the project memory above; they outrank every tool's own opinion.
2. Run the read-only tools first, in the order listed; carry their findings forward as the brief for the writes.
3. Run each write tool on its Role, one at a time, re-reading the brand contract between tools.
4. <task-specific verification — measure the file, screenshot, run the tests, whatever proves it>
5. Report.

## Guardrails
{chr(10).join(guard)}

## Report
One line per file changed · findings from the read-only tools · what was not done and why.
"""
    summary = {
        "write_to": str(out_path), "slug": slug, "tools": ordered, "orchestrator": orchestrators[0] if orchestrators else None,
        "missing": missing, "brand_contract": str(brand) if brand else None,
    }
    if as_json:
        print(json.dumps({**summary, "skeleton": text}, indent=2, ensure_ascii=False))
        return 0
    print(text)
    print("---")
    print(f"write_to: {out_path}")
    print(f"tools: {', '.join(ordered)}")
    if missing:
        print(f"missing: {', '.join(missing)}  ← flag this before offering to run")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
