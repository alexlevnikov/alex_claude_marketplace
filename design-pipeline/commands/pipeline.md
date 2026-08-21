---
description: Build a complete surface end to end through the ten design gates
argument-hint: "<surface-name> [ship-fast] [+motion] [+refs]"
---

Run the `design-pipeline` skill for: **$ARGUMENTS**

Start at G0 INTAKE. Resolve `BRAND-CONTRACT.md` by walking up from the working directory before
anything else — if none is found, stop and ask rather than building unbranded.

Flags in the arguments:
- `ship-fast` → mode `ship-fast`: CRAFT_LEVEL 5, G2 and G7 forced off.
- `+motion` → enable G7 MOTION.
- `+refs` → enable G2 REFERENCE (check image generation is actually available first).

Print the gate checklist at the start and after every gate resolves. Dispatch G3 and G5 as
subagents per `references/isolation.md`. Write `STATE.json` after each gate so the run is resumable.
