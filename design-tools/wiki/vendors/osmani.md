# web-quality-skills — Addy Osmani

**Repo:** https://github.com/addyosmani/web-quality-skills · **Install:** `npx skills add addyosmani/web-quality-skills`
**In the set:** 6 tools — `web-quality-audit` (172 lines, umbrella), `core-web-vitals` (483), `seo` (527), `accessibility` (450, WCAG 2.2), `performance` (400), `best-practices` (641, security/CSP). **MIT** — the one vendor safe to vendor verbatim into `vendors/` if the iCloud path ever becomes a problem.

## What it is

Metrics and compliance. The only vendor in the set that covers SEO and Core Web Vitals — ui-craft
explicitly defers both ("defer SEO strategy to an SEO skill"), which is why `design-pipeline`'s G8
audit gate exists and is owned here.

## The contract

`web-quality-audit` first when the worst axis is unknown; it names the axis, then the named skill
works it (`stacking.md`). Discriminators (`collisions.md` §1–2): a *metric* named → `core-web-vitals`;
*weight and load* → `performance`; a moving thing that is slow → ibelick; a *compliance* question
→ `accessibility`; a named a11y defect → ibelick.

## Engage

- Router: "LCP is bad" → `core-web-vitals`; "we don't rank" → `seo`; "run lighthouse" → `web-quality-audit`.
- Direct: `/design-tools:seo`, `/design-tools:core-web-vitals`, `/design-tools:accessibility`, …
- Whole surfaces: `design-pipeline` G8.
