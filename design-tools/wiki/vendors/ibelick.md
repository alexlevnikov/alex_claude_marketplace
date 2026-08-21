# ui-skills — ibelick

**Repo:** https://github.com/ibelick/ui-skills · **Install:** `npx skills add ibelick/ui-skills`
**In the set:** 3 tools — `baseline-ui` (90 lines), `fixing-accessibility` (140), `fixing-motion-performance` (156).

## What it is

Three short, prescriptive checklists. Their niche is the fast targeted fix when a 450-line doctrine
is overkill: a missing focus ring, a tab order, an animation that janks because it animates
`height`. `baseline-ui` is the base-tidiness list — spacing, alignment, contrast, consistency.

## The contract

Minutes, not hours. The moment the question becomes *compliance* (WCAG level, client requirement,
pre-launch) it belongs to [osmani](osmani.md); the moment it becomes *how should this feel* it
belongs to [emil](emil.md). `collisions.md` §1 and §2 encode exactly this.

## Engage

- Discovery: "keyboard navigation is broken" → `fixing-accessibility`; "it stutters" → `fixing-motion-performance`.
- Direct: `/design-tools:fixing-accessibility`, `/design-tools:fixing-motion-performance`, `/design-tools:baseline-ui`.
