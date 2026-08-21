---
name: design-tools
description: >
  Use for one targeted design pass on UI that **already exists** — typography, colour, spacing,
  responsive, motion, micro-interactions, empty and error states, accessibility, performance,
  Core Web Vitals, SEO, UX copy — or a read-only review, critique, score, or ship verdict.
  Triggers on: "fix the typography", "the colours are off", "it breaks on mobile", "this
  animation stutters", "make it quieter", "add some life to this", "check accessibility",
  "the page is slow", "we don't show up in search", "what would you change here", "score this
  page", "can I merge this", "what's that effect called". It picks exactly one specialist skill
  and delegates. For building a whole new surface from scratch, use `design-pipeline` instead.
metadata:
  version: "0.1.0"
---

# Design Tools

Seventy-six design skills are installed. Almost every request maps to exactly one of them, and the
hard part is not doing the work — it is not doing the work with the wrong tool, or with three tools
when one would have done.

This skill routes. It does not design.

## The five rules

**1. One tool per request.** Name it out loud before calling it: *"typography pass →
`typeset` (ui-craft), because the scale and tracking are the problem, not the colour."* The user is
learning this inventory; a silent route teaches nothing and hides a wrong turn until it is expensive.

**2. Read-only before write on unfamiliar code.** `critique`, `heuristic`, `audit`,
`web-quality-audit`, `improve-animations`, `find-animation-opportunities` and `finalize` change
nothing. On code you have not seen this session, judge first, then edit.

**3. Two write-tools maximum.** A third is the signal that this is not a pass any more. Stop, say
so, and offer `design-pipeline`.

**4. Escalate rather than drift.** "Build the product page", "redesign this section", "make it look
completely different" — these are pipeline work. A router that quietly becomes a conveyor costs the
pipeline's money without the pipeline's gates.

**5. Ask once rather than guess.** "Make it better" and "make it nice" are not routes. One
clarifying question is cheaper than an unwanted write pass.

## Before any write pass

Resolve `BRAND-CONTRACT.md` — the working directory, then each parent. Its tokens, forbidden list,
anti-slop laws and commerce laws outrank the vendor skill's own opinion. If the project has
`.ui-craft/brief.md`, read §6 learned constraints too — ui-craft's own precedence rule puts those
above any pass-level decision.

## Choosing

1. `references/routing.md` — the user's words → the tool. Start here; it is written in the phrasing
   people actually use, in English and Russian.
2. `references/collisions.md` — when two or three vendors cover the same ground. Twelve overlaps,
   each with a rule. **Consult this whenever the route lands on accessibility, performance, motion,
   polish, or review** — those are the contested five.
3. `references/catalog.md` — every tool, what it is for, whether it writes, and when *not* to reach
   for it.
4. `references/stacking.md` — the safe chains, and when a second tool needs a fresh context.

## What this skill never does

- **Art direction.** Any request for a new look, a different feel, or a redesign goes to
  `design-pipeline`. The thirteen orchestrator-class skills are not routed to from here.
- **Its own edits.** If the router "just fixes the spacing while it's in there", the tool it chose
  was wrong and the next session inherits an undocumented change.
- **Two orchestrators in one context.** Not applicable here by construction — none are routed.
