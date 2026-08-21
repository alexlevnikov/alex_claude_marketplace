# ui-craft — educlopez

**Repo:** https://github.com/educlopez/ui-craft · **Install:** `npx skills add educlopez/ui-craft`
**In the set:** 29 tools — the base, three presets, eight phase commands, fourteen passes, three judges. Live list: [README → Vendors](../README.md#vendors). Two review *agents* ship with it too (`ui-craft:design-reviewer`, `ui-craft:a11y-auditor`); they are agents, not skills, and have no command here.

## What it is

Not one vendor among many — the substrate. Stars measure the repository's popularity (265★, the
lowest in the inventory), not its depth: ui-craft supplies the ladder (Ask → Direct → Persist →
Enforce), four knobs (`CRAFT_LEVEL`, `MOTION_INTENSITY`, `VISUAL_DENSITY`, `DESIGN_VARIANCE`), the
anti-slop "Top 12", a ~45-row routing table of its own, the Craft Report format, thirty-three
reference files, a six-gate conveyor (`sddesign`), and the only **durable project memory** in the
set: `.ui-craft/brief.md` and `.ui-craft/spec.md`.

A dashboard in design-studio mis-attributed twelve of its lenses (`polish, typeset, colorize,
clarify, distill, extract, harden, unhappy, delight, quieter, finalize, redesign`) to impeccable.
Every one of those files carries the marker *"this sub-skill is one lens of the broader ui-craft
skill"*. They are ui-craft.

## The contract

**A lens loads its base first.** Each lens is 30–60 lines and opens with "if `ui-craft` is installed,
read its SKILL.md first". Without the base a lens has no anti-slop rules, no knobs, no report
format. The resolver prints `base:` for every lens — load it.

**Phase commands are interactive.** `brief` asks five questions, `tokens` asks which file to write,
`shape` asks three to five more. Unattended runs must carry the answers in; `design-pipeline` does.

**`.ui-craft/brief.md` §6 outranks any pass.** Learned constraints and the a11y floor win over a
lens's own opinion — ui-craft's rule, not ours.

## Where it is strong / weak

Strong: gates and artifacts, anti-slop discipline, knobs, honesty about skipped steps, review
format. Weak: SEO and Core Web Vitals are explicitly out of scope ("defer SEO strategy to an SEO
skill"); motion is one reference file against Emil's nine skills; no image generation; art
direction is `craft-intent.md` against taste-skill's 1206-line doctrine. `craft` has recipes for
dashboard, landing and auth — **no e-commerce recipe**, and it refuses to improvise one.

## Engage

- Router: almost every LOOK / FIX / JUDGE route lands on a ui-craft lens.
- Direct: `/design-tools:typeset`, `/design-tools:unhappy`, `/design-tools:finalize`, …
- Whole surfaces: `design-pipeline` wraps `brief → tokens → shape → craft → unhappy → harden → finalize` as gates G1–G9.
