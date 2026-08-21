---
name: design-tools
description: >
  Use for one targeted design pass on UI that **already exists** — typography, colour, spacing,
  responsive, motion, micro-interactions, empty and error states, accessibility, performance,
  Core Web Vitals, SEO, UX copy — or a read-only review, critique, score, or ship verdict.
  Triggers on: "fix the typography", "the colours are off", "it breaks on mobile", "this
  animation stutters", "make it quieter", "add some life to this", "check accessibility",
  "the page is slow", "we don't show up in search", "what would you change here", "score this
  page", "can I merge this", "what's that effect called". It picks exactly one specialist skill,
  resolves where that skill is installed, loads it, and runs it. Also use when the user names a
  tool from the set outright ("run impeccable on this", "use typeset") — `/design-tools:<vendor>` runs
  a vendor's master skill as designed, `/design-tools:<vendor>-<tool>` engages one tool directly. For building a whole new surface from scratch, use `design-pipeline`.
metadata:
  version: "0.3.0"
---

# Design Tools

Eighty-seven design skills are in the set. Almost every request maps to exactly one of them, and
the hard part is not doing the work — it is not doing the work with the wrong tool, with three
tools when one would have done, or with a tool's *name* and none of its text.

This skill routes, then loads. It does not design.

## The six rules

**1. One tool per request.** Name it out loud before calling it: *"typography pass →
`typeset` (ui-craft), because the scale and tracking are the problem, not the colour."* The user is
learning this inventory; a silent route teaches nothing and hides a wrong turn until it is expensive.

**2. A name is not a skill until it is loaded.** The vendor skills live in design-studio's project
scope; from any other project the Skill tool cannot see them by name. After choosing, run the
resolver and load what it points at — `references/loading.md`. A route into an unloaded skill
produces generic work with a specialist's name on it, which is the failure this plugin exists to
prevent.

**3. Read-only before write on unfamiliar code.** `critique`, `heuristic`, `audit`,
`web-quality-audit`, `improve-animations`, `find-animation-opportunities`, `review-animations` and
`finalize` change nothing. On code you have not seen this session, judge first, then edit.

**4. Two write-tools maximum.** A third is the signal that this is not a pass any more. Stop, say
so, and offer `design-pipeline`.

**5. Escalate rather than drift.** "Build the product page", "redesign this section", "make it look
completely different" — these are pipeline work. A router that quietly becomes a conveyor costs the
pipeline's money without the pipeline's gates.

**6. Ask once rather than guess.** "Make it better" and "make it nice" are not routes. One
clarifying question is cheaper than an unwanted write pass.

## Before any write pass

Resolve `BRAND-CONTRACT.md` — the working directory, then each parent. Its tokens, forbidden list,
anti-slop laws and commerce laws outrank the vendor skill's own opinion. If the project has
`.ui-craft/brief.md`, read §6 learned constraints too — ui-craft's own precedence rule puts those
above any pass-level decision.

## Choosing, then loading

1. `references/routing.md` — the user's words → the tool. Start here; it is written in the phrasing
   people actually use, in English and Russian.
2. `references/collisions.md` — when two or three vendors cover the same ground. Twelve overlaps,
   each with a rule. **Consult this whenever the route lands on accessibility, performance, motion,
   polish, or review** — those are the contested five.
3. `references/catalog.md` — every routable tool, what it is for, whether it writes, and when *not*
   to reach for it.
4. `references/stacking.md` — the safe chains, and when a second tool needs a fresh context.
5. `references/loading.md` — **now load it**: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh" <tool>`,
   read the manifest, invoke by name (`load: skill`) or read-and-follow (`load: read`), base first
   for ui-craft lenses. `status: MISSING` means stop and say so, not improvise.

## Direct engagement

When the user names a tool — "run `impeccable` on the hero", "do a `typeset` pass" — there is nothing
to route. Every tool in the set has a command, named **vendor-first** so the picker groups them:
`/design-tools:ui-craft-typeset`, `/design-tools:osmani-seo`, `/design-tools:emil-apple-design`
(no double prefix when the tool already carries the vendor key: `emil-design-eng`, `threejs-shaders`).
Each resolves, loads and runs that one tool under the same discipline.

Every vendor also has an **entry command**, `/design-tools:<vendor>`. Where the vendor has a master
skill — `ui-craft`, `impeccable`, `taste` (→ `design-taste-frontend`), `lottie` (→ `motion-design`),
the single-skill vendors — it runs that skill **as the vendor designed it**: its own discovery,
modes, knobs and report, with the router's pass discipline deliberately not layered on top; only
the brand contract (as the answer to its brand questions) and "say what changed" survive. Where the
vendor has no master — `emil`, `osmani`, `ibelick`, `iart`, `threejs` — the command lists and
dispatches. Orchestrator-class tools are reachable these ways *only* — the router never lands on
them. The wiki (`wiki/README.md`, `wiki/vendors/`, `wiki/tools/`) is the reference for what each one is.

## What this skill never does

- **Art direction.** Any request for a new look, a different feel, or a redesign goes to
  `design-pipeline`. Orchestrator-class skills are not routed to from here.
- **Its own edits.** If the router "just fixes the spacing while it's in there", the tool it chose
  was wrong and the next session inherits an undocumented change.
- **Run a tool it did not load.** The name in the catalog is a pointer; the skill is the file.
- **Two orchestrators in one context.** Not by routing — and not by direct engagement either.
