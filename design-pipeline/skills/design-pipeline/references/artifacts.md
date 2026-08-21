# Artifacts

Two directories, two owners, both in the **current project**.

```
.ui-craft/                  ← ui-craft owns. Never hand-edit; call the phase command.
├── brief.md                   durable project design brief (§6 = learned constraints)
└── spec.md                    one "## Surface: <name>" section per surface

.studio/<surface>/          ← this pipeline owns
├── 00-intake.md
├── 02-refs.md   + refs/*.png
├── 03-DIRECTION.md
├── 08-AUDIT.md
├── 09-SHIP.md
└── STATE.json
```

## STATE.json

The file that makes a run resumable. Written after every gate resolves.

```json
{
  "surface": "product-page",
  "started": "2026-08-20T22:40:00-07:00",
  "mode": "full",
  "design_variance": 6,
  "sale_mode": "both",
  "build_target": "self-contained-html",
  "brand_contract": "/Users/…/alex.levnikov.root/BRAND-CONTRACT.md",
  "gates": {
    "G0": { "status": "done" },
    "G1": { "status": "done", "vendor": "ui-craft:brief+tokens" },
    "G2": { "status": "skipped", "cost": "no visual target for the build to hit" },
    "G3": { "status": "done", "vendor": "design-taste-frontend" },
    "G4": { "status": "running" }
  }
}
```

`status` ∈ `pending | running | done | skipped`. A `skipped` gate always carries a `cost` string —
that string is what gets printed in the ship verdict. Timestamps come from `date`, never invented.

## 00-intake.md

The six answers from G0, verbatim, plus the resolved brand-contract path and the detected build
target. Short. It exists so G9 can check the result against what was actually asked for.

## 03-DIRECTION.md

Six required sections — thesis, palette in use, type pair with scale, composition principle,
signature detail, forbidden-for-this-surface. No code. See `gates.md` G3.

## 08-AUDIT.md

```markdown
# Audit — <surface>            2026-08-20 · seo + core-web-vitals + accessibility

## Critical
- [SEO] No Product structured data on the buy panel. → add JSON-LD Product + Offer.

## Serious
- [CWV] Hero image 1.8 MB unoptimised, LCP 4.1s measured. → responsive srcset + AVIF.

## Minor
…

## Measured
LCP 4.1s · INP 180ms · CLS 0.02   (Lighthouse, mobile throttled)
— or: "not measured: no local server available for this surface."
```

## 09-SHIP.md

The `finalize` verdict verbatim, then the resolved gate checklist, then every skipped gate with its
cost, then the two extra checks from `gates.md` G9 — brand-contract compliance and direction
compliance — each answered yes/no with a reason.
