# impeccable — pbakaus

**Repo:** https://github.com/pbakaus/impeccable · **Install:** `npx impeccable skills install`
**In the set:** 1 tool — `impeccable` (v4.0.4, Apache 2.0, `user-invocable: true`).

## What it is

One skill with internal modes, not a suite: `impeccable shape`, `impeccable audit|critique`,
`impeccable animate|bolder|colorize|delight|layout|overdrive|quieter|typeset`,
`impeccable adapt|clarify|distill`, `impeccable harden|onboard|optimize|polish`,
`impeccable init|document|extract|live`. The modes are reference files under `references/`
(36 of them); none is installed as a separate skill. It ships 40+ scripts — image generation,
a live browser overlay, a CSP detector, a doctor.

The strongest authorial point of view in the set. In the group-01 bake-off it drew cedar in CSS
rather than reaching for stock photography — and billed the most: roughly 3× the tool calls of
`design-taste-frontend` (36 tool uses for one hero). It bounds its own QA on purpose ("verify in
bounded passes, not a loop").

## The contract

- **Orchestrator.** Own context; never beside another orchestrator.
- **`impeccable polish` ≠ `polish`.** The installed `polish` is the ui-craft lens and reads
  `.ui-craft/brief.md`. Reach for impeccable's only when the owner names impeccable.
- **Scripts are project-relative** in its `allowed-tools` (`node .claude/skills/impeccable/scripts/*`).
  Loaded from a root, call them by the absolute `dir:` the resolver prints.
- **High variance.** `design-pipeline` uses it for G3 at DESIGN_VARIANCE ≥ 7.

## Engage

- Router: never — orchestrator-class requests escalate to `design-pipeline`.
- Direct: `/design-tools:impeccable <mode> <target>` — the deliberate by-pass.
