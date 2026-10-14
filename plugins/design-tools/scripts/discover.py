#!/usr/bin/env python3
"""discover.py — run a task through the whole set and print what the model needs to judge it.

    discover.sh "<task in the user's words>" [--top N] [--json]

Prints, in this order:
  task:                 the words as received
  pre-rank:             the top N tools by lexical overlap — a HINT for the model, not a verdict.
                        Each line shows the matched terms so the model can see *why* it ranked.
  whole-vendor options: vendors whose master skill could take the task alone (orchestrator-class)
  index:                every registered tool, one line — vendor · tool · mode · class · routable ·
                        what it does · the skill's own trigger phrases (from its frontmatter, clipped)

Matching is prefix-based on 5 characters so Russian inflection and English plurals match
("заголовки" ~ "заголовок", "animations" ~ "animation"). Sources and weights: tool name 5 ·
phrases.md rows 4 · `does` 3 · vendor 1 · the skill's description 1. The model does the semantic
judgement on top; collisions.md decides between overlapping candidates.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve as R  # noqa: E402

PLUGIN = R.PLUGIN_ROOT
PHRASES = PLUGIN / "skills" / "design-tools" / "references" / "phrases.md"
WEIGHTS = {"name": 5, "phrases": 4, "does": 3, "vendor": 1, "description": 1}
STOP = set("""the and for with this that from into your our are was were have has not but you its it's
make fix check what how why when where которые которая который это этот эта для при как что чтобы
page страница страницу страницы страниц very just some more less than then them they here there""".split())


def tokens(text: str) -> list[str]:
    out = []
    for t in re.findall(r"[\w\-]+", text.lower(), flags=re.UNICODE):
        t = t.strip("-_")
        if len(t) >= 3 and t not in STOP:
            out.append(t)
    return out


def prefix_match(q: str, vocab: list[str]) -> str | None:
    """q matches a vocabulary token when one is a 5-char prefix of the other (or equal)."""
    k = min(5, len(q))
    for v in vocab:
        if v == q or (len(v) >= k and len(q) >= k and v[:k] == q[:k] and (len(q) >= 5 or len(v) >= 5)):
            return v
    return None


def frontmatter_description(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if not text.startswith("---"):
        return ""
    body = text.split("\n", 1)[1]
    end = body.find("\n---")
    fm = body[:end] if end >= 0 else body
    m = re.search(r"^description:\s*(.*)$", fm, flags=re.M)
    if not m:
        return ""
    val = m.group(1).strip()
    if val in (">", "|", ">-", "|-", ""):
        lines = []
        for line in fm[m.end():].splitlines()[1:]:
            if line.startswith((" ", "\t")):
                lines.append(line.strip())
            elif line.strip():
                break
        val = " ".join(lines)
    return val.strip().strip("\"'").replace('\\"', '"')


def phrases_by_tool() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not PHRASES.is_file():
        return out
    for line in PHRASES.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---") or "They say" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        for t in re.findall(r"`([a-z0-9\-:]+)`", cells[1]):
            out.setdefault(t, []).append(cells[0])
    return out


def build_index(reg: dict) -> list[dict]:
    phrases = phrases_by_tool()
    rows = []
    for tool, meta in reg["tools"].items():
        v = reg["vendors"][meta["vendor"]]
        res = R.resolve(tool, reg)
        desc = frontmatter_description(Path(res["skill"])) if res["status"] == "OK" else ""
        rows.append({
            "tool": tool, "vendor": meta["vendor"], "vendor_display": v["display"],
            "mode": meta["mode"], "class": meta["class"], "group": meta["group"],
            "routable": meta["routable"], "does": meta["does"], "for": meta.get("for", ""),
            "not_for": meta.get("not_for", ""), "phrases": phrases.get(tool, []),
            "description": desc, "status": res["status"],
            "command": cmd_name(tool, meta),
        })
    return rows


def cmd_name(tool: str, meta: dict) -> str:
    if meta.get("command"):
        return meta["command"]
    v = meta["vendor"]
    return tool if (tool == v or tool.startswith(v + "-")) else f"{v}-{tool}"


def score(row: dict, q_tokens: list[str]) -> tuple[int, list[str]]:
    fields = {
        "name": tokens(row["tool"].replace("-", " ")),
        "phrases": tokens(" ".join(row["phrases"])),
        "does": tokens(row["does"] + " " + row["for"]),
        "vendor": tokens(row["vendor_display"]),
        "description": tokens(row["description"]),
    }
    total, hits = 0, []
    for q in q_tokens:
        for f, vocab in fields.items():
            m = prefix_match(q, vocab)
            if m:
                total += WEIGHTS[f]
                hits.append(f"{q}→{m}({f[0]})")
                break  # count each query token once, at its best field
    return total, hits


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    top = 12
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
    words = [a for i, a in enumerate(argv) if not a.startswith("--") and not (i > 0 and argv[i - 1] == "--top")]
    task = " ".join(words).strip()
    if not task:
        print(__doc__)
        return 2
    reg = R.load_registry()
    rows = build_index(reg)
    q = tokens(task)
    ranked = []
    for r in rows:
        s, hits = score(r, q)
        ranked.append((s, r, hits))
    ranked.sort(key=lambda x: (-x[0], x[1]["tool"]))
    whole = [(vk, v) for vk, v in reg["vendors"].items()
             if v.get("master") and reg["tools"].get(v["master"], {}).get("class") in ("orchestrator", "base")]

    if as_json:
        print(json.dumps({
            "task": task, "tokens": q,
            "pre_rank": [{"tool": r["tool"], "command": r["command"], "score": s, "matched": h}
                         for s, r, h in ranked[:top] if s > 0],
            "whole_vendor_options": [{"vendor": vk, "display": v["display"], "master": v["master"]} for vk, v in whole],
            "index": rows,
        }, indent=2, ensure_ascii=False))
        return 0

    print(f"task: {task}")
    print(f"tokens: {' '.join(q) or '(none ≥3 chars — rank by meaning alone)'}")
    print(f"\npre-rank (lexical overlap — a hint, not a verdict; top {top}):")
    any_hit = False
    for i, (s, r, h) in enumerate(ranked[:top], 1):
        if s <= 0:
            break
        any_hit = True
        print(f"  {i:>2}. {r['tool']:<28} {r['vendor']:<10} {r['mode']:<3} {r['class']:<12} score {s:<3} "
              f"matched: {', '.join(h[:5])}")
    if not any_hit:
        print("  (no lexical hits — judge from the index below)")
    print("\nwhole-vendor options (one orchestrator alone; never two in one context):")
    for vk, v in whole:
        m = reg["tools"][v["master"]]
        print(f"  - /design-tools:{vk:<24} master {v['master']:<24} — {m['does']}")
    print("\nescalation: a whole new surface (\"build the product page\", \"redesign the homepage\") is "
          "design-pipeline, not a composed prompt.")
    print(f"\nindex ({len(rows)} tools): vendor · tool · mode · class · routable · does · triggers")
    for r in rows:
        trig = (r["description"][:150] + "…") if len(r["description"]) > 150 else r["description"]
        flag = "" if r["status"] == "OK" else "  [MISSING on this machine]"
        print(f"- {r['vendor_display']} · {r['tool']} · {r['mode']} · {r['class']} · "
              f"{'routable' if r['routable'] else 'direct-only'} · {r['does']}"
              + (f" · triggers: {trig}" if trig else "") + flag)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
