# Emil Kowalski skills — emilkowalski

**Repo:** https://github.com/emilkowalski/skills · **Install:** `npx skills add emilkowalski/skills`
**In the set:** 9 tools — `emil-design-eng`, `apple-design`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `animation-vocabulary`, `pick-ui-library`, `ask-sonner`, `prototype`. Live list: [README](../README.md#vendors).

> `motion-design` in this inventory is **LottieFiles**, not Emil — see [lottiefiles.md](lottiefiles.md). Earlier notes attributed it here; `skills-lock.json` says otherwise.

## What it is

The motion reference. `emil-design-eng` (674 lines): the philosophy of polish, spring animations,
component contracts, a review format. `apple-design` (282): gestures, interruptibility, velocity
handoff, momentum — direct manipulation. Two read-only planners: `improve-animations` audits all
motion and writes a plan for other agents; `find-animation-opportunities` finds where motion is
missing but earned. `animation-vocabulary` is the reverse dictionary — "that bouncy thing" → *Pop
in*. `review-animations` judges animation code against Emil's bar ("default to flagging; approval
is earned"). `prototype` builds several genuinely different versions behind a visual picker.

## The contract

Taste lives here; performance lives with [ibelick](ibelick.md). `prototype` and `review-animations`
carry `disable-model-invocation: true` — they run only when named, which is exactly what the
per-tool commands do.

## Engage

- Router: FEEL routes — "this component feels cheap" → `emil-design-eng`; "the drawer should follow my finger" → `apple-design`; "add some motion" → `find-animation-opportunities` then a write tool.
- Direct: `/design-tools:emil-design-eng`, `/design-tools:review-animations`, `/design-tools:prototype`, …
