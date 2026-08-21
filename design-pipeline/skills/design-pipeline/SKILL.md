---
name: design-pipeline
description: >
  Use when building or redesigning a **whole** web surface from scratch — a page, a screen,
  a section, a landing, a product page, a checkout. Triggers on: "build the product page",
  "design the catalog", "redesign the homepage", "make a landing for X", "we need the
  configurator page", "start the new surface". It runs ten gates end to end — intake, brief,
  tokens, references, art direction, wireframe, build, states, motion, audit, ship verdict —
  dispatching one vendor skill per gate and writing an artifact at each, so the run is
  resumable and the result is defensible. For a single targeted pass on UI that already
  exists — typography, colour, motion, states, a11y, performance, SEO, or a read-only review
  — use `design-tools` instead.
metadata:
  version: "0.1.0"
---

# Design Pipeline

Ten gates, one vendor per gate, an artifact at every gate. The point is not that the work gets
done — a single good skill can do that. The point is that it gets done **the same way twice**,
that every stage leaves something the next stage can read, and that a run interrupted at gate six
resumes at gate six.

## The three laws

**1. Orchestrate only.** This skill sequences other skills. It never re-implements what a vendor
already does. No composition rules, no easing tables, no WCAG criteria live in this plugin — they
live in the vendor skills, and the gate calls them. When in doubt: call the phase, don't inline it.

**2. One orchestrator per context.** The inventory holds thirteen orchestrator-class skills. Two of
them in one context fight over art direction and the output goes muddy. Gates G3 and G5 therefore
run in **their own subagent**, each told to use exactly one named skill. See `references/isolation.md`.

**3. Degraded honesty.** A skipped gate is marked `[–]` and its downstream cost is printed in the
ship verdict. Never present a run with skipped gates as a clean run.

## The gates

```
G0 INTAKE → G1 FOUNDATION → [G2 REFERENCE] → G3 DIRECTION → G4 SHAPE → G5 BUILD
   → G6 STATES → [G7 MOTION] → G8 AUDIT → G9 SHIP
```

| Gate | Owner | Produces |
|---|---|---|
| G0 INTAKE | this skill | `.studio/<surface>/00-intake.md` |
| G1 FOUNDATION | `brief` → `tokens` (ui-craft) | `.ui-craft/brief.md` + token spine |
| G2 REFERENCE *(opt, default off)* | `imagegen-frontend-web` / `brandkit` | `.studio/<surface>/refs/` |
| G3 DIRECTION | `design-taste-frontend` **or** `impeccable` | `.studio/<surface>/03-DIRECTION.md` |
| G4 SHAPE | `shape` (ui-craft) | `.ui-craft/spec.md` |
| G5 BUILD | `craft` (ui-craft) + `full-output-enforcement` | the surface |
| G6 STATES | `unhappy` → `harden` (ui-craft) | states in code |
| G7 MOTION *(opt, default off)* | `motion-design` → `emil-design-eng` → `fixing-motion-performance` | motion in code |
| G8 AUDIT | `seo` + `core-web-vitals` + `accessibility` (Osmani) | `.studio/<surface>/08-AUDIT.md` |
| G9 SHIP | `finalize` (ui-craft) | `.studio/<surface>/09-SHIP.md` |

Full specification of every gate — precondition, exact invocation, isolation, bar, skip cost,
fallback — is in `references/gates.md`. **Read it before running any gate.**

## Running

1. **Resolve the brand contract.** Look for `BRAND-CONTRACT.md` in the working directory, then in
   each parent directory. It is the highest authority after the a11y floor: its tokens, forbidden
   list, and commerce laws override any vendor's opinion. If none is found, say so and ask before
   proceeding — building a branded surface without the contract is how drift starts.
2. **Resolve state.** If `.studio/<surface>/STATE.json` exists, this is a resume: print the
   checklist, continue from the first unresolved gate. Never silently re-run a closed gate.
3. **Print the checklist** at the start and after every gate resolves:

```
[✓] G0 intake  [✓] G1 foundation  [–] G2 reference  [>] G3 direction  [ ] G4 shape …
```

`[✓]` closed · `[>]` running · `[–]` skipped, cost recorded · `[ ]` pending.

4. **Walk the gates.** Each gate: check its precondition, dispatch its owner, verify its bar,
   write its artifact, update `STATE.json`, print the checklist.
5. **Report the verdict** from G9 with the full resolved checklist and every skipped gate's cost.

## Where things are written

`.ui-craft/` belongs to ui-craft — `brief.md` and `spec.md`. Never hand-edit it; call the phase
command that owns it. `.studio/<surface>/` belongs to this pipeline. Both live in the **current
project**, so a bake-off in `design-studio` and production work in `yoursaunas-site` never collide.
Schemas and examples: `references/artifacts.md`.

## Defaults

- **Art direction (G3)** is chosen by `DESIGN_VARIANCE` from intake: `≤6` → `design-taste-frontend`
  (cheaper, predictable); `≥7` → `impeccable` (stronger point of view, roughly 3× the tool calls).
- **Build target (G5)** is auto-detected. `astro.config.mjs` present → Astro components matching the
  project's existing patterns. No framework → one self-contained `index.html`, Tailwind via CDN.
- **G2 and G7 are off** unless the intake asks for them. Motion is a deliberate second pass on
  commercial surfaces, not a default cost on every page.
- `full-output-enforcement` is on for every gate that writes a long file. No placeholders, no
  "// rest of the implementation here".

## When not to use this

One pass on existing code — "fix the typography", "check a11y", "make it quieter" — is
`design-tools`. If a run reaches G5 and the only actual change needed is a single pass, stop, say
so, and hand it down. A conveyor run on a one-line problem costs the user real money.

## References

- `references/gates.md` — the ten gate specifications. Authoritative.
- `references/vendors.md` — vendor contracts: invocation, input, output, fallback, licence.
- `references/artifacts.md` — artifact schemas with minimal examples.
- `references/isolation.md` — subagent dispatch templates and the collision rules.
