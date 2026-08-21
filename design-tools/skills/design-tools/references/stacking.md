# Stacking

## Safe chains — one context, in this order

- `unhappy` → `harden` — state model first, production matrix second.
- `find-animation-opportunities` (R) → `motion-design` (W) — propose, then implement.
- `improve-animations` (R) → `fixing-motion-performance` (W) — plan, then enforce the budget.
- `audit` (R) → `fixing-accessibility` (W) — find, then fix.
- `web-quality-audit` (R) → one of `seo` / `core-web-vitals` / `accessibility` (W) — the umbrella
  names the worst axis, then you work that axis.
- `typeset` → `colorize` — type settles the hierarchy, colour then reinforces it. Not the reverse:
  colour chosen against a hierarchy you are about to change is wasted work.
- `critique` (R) → any single W tool it recommends.

## The rules

1. **Read-only before write** on any code you have not seen this session.
2. **Two write-tools maximum per request.** The third means escalate.
3. **Never chain two tools that own the same aspect.** `typeset` then `high-end-visual-design` is
   two type opinions fighting; pick one.
4. **Re-read the brand contract between tools** if the first one wrote a lot. Vendors drift toward
   their own defaults over a long file — the contract is what pulls it back.
5. **After any write pass, say what changed** in one line per file. A pass whose diff nobody
   describes is a pass nobody can undo.

## When a fresh context is required

Not for passes — they compose. Only for orchestrator-class skills, and this plugin routes to none.
If a request genuinely needs one (`impeccable`, `design-taste-frontend`, `craft`), that is the
escalation signal, not a stacking question: hand it to `design-pipeline`, which dispatches
orchestrators in isolated subagents by design.

## The escalation sentence

When the threshold is hit, say it plainly and stop:

> This is three passes deep — typography, colour and layout are all wrong together, which usually
> means the direction is wrong rather than the details. That is `design-pipeline` work: it will
> settle the direction first and hold it while the surface gets rebuilt. Want me to start a run,
> or should I keep going one pass at a time?

Then wait. Do not start the pipeline unasked — it is a much larger spend.
