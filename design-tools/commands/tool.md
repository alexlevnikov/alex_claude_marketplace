---
description: Route a design request to exactly one specialist skill and run it
argument-hint: "<what you want, in your own words> [file or path]"
---

Use the `design-tools` skill to route: **$ARGUMENTS**

1. Resolve `BRAND-CONTRACT.md` (working directory, then parents) before any write pass.
2. Find the route in `references/routing.md`. If it lands on accessibility, performance, motion,
   polish or review, check `references/collisions.md` before calling.
3. **Say the route out loud** — the tool, the vendor, and the one-sentence reason — before calling it.
4. Run it. Read-only tools first on code you have not seen this session.
5. Report what changed, one line per file.

If the request needs more than two write-tools, or asks for a new look rather than a fix, stop and
offer `design-pipeline` instead. If the request is "make it better" with no aspect named, ask which
aspect is wrong — do not guess.
