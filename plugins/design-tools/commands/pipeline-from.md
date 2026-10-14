---
description: Re-run the pipeline from a specific gate, keeping earlier artifacts
argument-hint: "<G0-G9> <surface-name>"
---

Re-run `design-pipeline` starting at the named gate for: **$ARGUMENTS**

1. Read `.studio/<surface>/STATE.json` and confirm the gates before the named one are `done`. If an
   earlier gate is missing, say which, and ask whether to run it first or accept the degradation.
2. Mark the named gate and everything after it as `pending`, then walk forward normally.
3. Artifacts from re-run gates are **overwritten**, not appended. Say which files you are about to
   replace before replacing them.

Use this when a direction needs reworking (`G3`), a spec changed (`G4`), or an audit must be redone
after fixes (`G8`). For one targeted fix on the built surface, use `design-tools` instead — a
pipeline re-run is the expensive way to change a font size.
