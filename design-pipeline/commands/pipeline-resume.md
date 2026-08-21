---
description: Resume an interrupted pipeline run from its first unresolved gate
argument-hint: "<surface-name>"
---

Resume the `design-pipeline` run for: **$ARGUMENTS**

1. Read `.studio/$ARGUMENTS/STATE.json`. If it does not exist, say so and offer `/pipeline` instead —
   do not start a fresh run silently under a resume command.
2. Print the resolved checklist exactly as it stands, including every `[–]` skipped gate and its cost.
3. Continue from the first gate whose status is `pending` or `running`. A gate marked `running` was
   interrupted mid-flight: verify whether its artifact exists and is complete before re-running it.
4. Never re-run a `done` gate. If the user wants one redone, that is `/pipeline-from`.
