# Isolation

## Why

The inventory holds thirteen orchestrator-class skills — `impeccable`, `design-taste-frontend`,
`high-end-visual-design`, `craft`, `sddesign`, the three `ui-craft-*` presets, `frontend-god-mode`,
`awwwards`, `design`, `calm-design`, `redesign`. They auto-trigger on overlapping language, and two
in one context produce a surface that is arguing with itself: two heroes' worth of ideas, neither
committed to.

Passes do not have this problem. `typeset`, `unhappy`, `seo` and their kind operate on one aspect
and compose cleanly.

There is a second, independent reason to isolate, and the first version of this file missed it:
**context cost**. A pass that reads a 100 KB built surface spends as much of the orchestrator's
context as an orchestrator does. Isolation is decided by what a gate *reads*, not only by what class
its owner belongs to.

## The rules

1. **G3 and G5 run in a subagent.** Non-negotiable — their owners are orchestrator-class.
2. **One orchestrator per subagent**, named explicitly, with an instruction not to invoke others.
3. **Gates that read the built artifact — G6, G8, G9 — are `subagent-if-large`:** inline while the
   surface is under 25 KB, dispatched above it. Measure the file; do not estimate. The orchestrator
   must finish the run, and a gate that exhausts its context mid-pipeline costs more than a dispatch.
4. **Gates that read only their own small inputs run inline** — G0, G1, G4.
5. **Never dispatch an orchestrator speculatively.** If a gate is already closed by an artifact,
   the gate is skipped, not re-run "to compare".
6. **The subagent gets artifacts, not conversation.** Everything it needs is in the files listed
   in its prompt. It cannot see this conversation and must not be assumed to.
7. **The dispatching gate verifies what comes back.** A subagent's report is a claim about the
   artifact, not the artifact. See *A gate closes on a verified artifact* in `gates.md`.

## Dispatch template — G3 DIRECTION

> You are producing an **art-direction document only. Do not write any code.**
>
> Read, in this order:
> 1. `<path>/BRAND-CONTRACT.md` — tokens, forbidden list, anti-slop laws, commerce laws. Highest
>    authority after accessibility. §1, §3 and §5 cannot be broken.
> 2. `.studio/<surface>/00-intake.md` — what this surface must do.
> 3. `.ui-craft/brief.md` — project principles, §6 learned constraints.
> 4. `.studio/<surface>/refs/` — reference images, if present.
>
> Use **only** the `<VENDOR>` skill. Do not invoke any other design skill — not `craft`, not
> `impeccable`, not `ui-craft`. If another skill would auto-trigger, ignore it.
>
> Write `.studio/<surface>/03-DIRECTION.md` with exactly these six sections: Thesis · Palette in use
> · Type pair with scale · Composition principle · Signature detail · Forbidden for this surface.
>
> If your direction needs to break an anti-slop law from brand contract §4, name the law and argue
> for it in the Thesis. Return the path you wrote and a two-sentence summary of the direction. Your
> final message is the return value — no preamble.

## Dispatch template — G5 BUILD

> You are building one surface. Read, in this order:
> 1. `<path>/BRAND-CONTRACT.md`
> 2. `.studio/<surface>/03-DIRECTION.md` — the direction is settled. Execute it; do not redesign.
> 3. `.ui-craft/spec.md`, section `## Surface: <surface>` — composition, components, state list,
>    acceptance bar. Every acceptance-bar item must be green before you report done.
> 4. `.studio/<surface>/00-intake.md` — sale mode and data reality.
>
> Build target: `<detected target>`. Match the project's existing patterns; do not introduce a
> second styling system.
>
> Use **only** the `craft` skill from ui-craft, with `full-output-enforcement` active. No
> placeholders, no truncated files, no "rest of implementation" comments. Build the direction's
> signature detail in this pass — not later.
>
> Do not invoke another orchestrator. Report: files written, acceptance-bar items green, and
> anything you could not do and why.

## Verifying isolation held

After G3 and G5, check the subagent's report for evidence that a second orchestrator ran — a second
art direction, an unrequested restyle, a palette that is not the contract's. If found, the gate did
not close: discard the output and re-dispatch with the constraint restated. Cheaper than shipping it.
