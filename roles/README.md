# Roles

A role is a way to use one or more installed packs for a recurring job. It is
lightweight: the role guide gives an entry skill, handoffs, and dependencies.
It does not copy vendor skills or imply a persistent autonomous agent. Install
the required packs from the [marketplace](../README.md); optional packs add
capabilities when a task needs them.

| Role | Required pack | Optional pack | Start with |
| --- | --- | --- | --- |
| [Interface builder](interface-builder.md) | `design-tools` | `browser-lab` | `design-tools` for an existing UI; `design-pipeline` for a new surface |
| [Web researcher](web-researcher.md) | `web-harvest` | `browser-lab` | `web-harvest` for retrieval; hand off to `browser-lab` for live interaction |

The machine-readable [catalog](catalog.json) records each role's pack
dependencies and entry skills. `scripts/check.py` verifies them against the
marketplace. Add a native Claude or Codex agent only after a representative
workflow shows that separate context or delegation improves the result.
