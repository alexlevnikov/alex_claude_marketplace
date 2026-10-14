# Vendor contracts

The 87-skill inventory is bundled from pinned current upstream revisions recorded in
`vendors/LOCK.json`. Before each gate, resolve its owner with `scripts/resolve.sh <tool>`, read
the returned `skill:` file (and `base:` first for ui-craft lenses), and resolve relative references
against `dir:`. Pass the gate's task to that loaded procedure. A missing owner is a broken package;
stop and report it rather than silently substituting another vendor.

## ui-craft (educlopez) — the substrate

Owns G1, G4, G5, G6, G9. Twenty-nine bundled skills, thirty-four base reference files, and the only
vendor with durable project memory (`.ui-craft/brief.md`, `.ui-craft/spec.md`).

| Gate | Skill | Note |
|---|---|---|
| G1 | `brief`, `tokens` | writes `.ui-craft/brief.md`; `tokens` establishes the 3-layer spine |
| G4 | `shape` | wireframe + state lattice → `.ui-craft/spec.md` |
| G5 | `craft` | recipes exist for dashboard / landing / auth; e-commerce falls back to standard build mode |
| G6 | `unhappy` → `harden` | state machine first, production matrix second |
| G9 | `finalize` | READY / NOT READY / BLOCKED, findings only, never edits |

**Contract:** every ui-craft lens opens by asking to read `ui-craft/SKILL.md` first — let it. A lens
without its base loses the anti-slop rules, the knobs, and the Craft Report format.

**Interactive by design — carry the answers in.** These lenses stop and wait for a human unless the
invocation pre-empts them. An unattended run that dispatches them bare will stall.

| Lens | What it stops on | What the gate must supply |
|---|---|---|
| `brief` | five questions, then "show before writing" | product purpose · primary user · 3–5 principles · success metric · out of scope — all derivable from `00-intake.md` and the brand contract. Plus: write without confirmation. |
| `tokens` | "ask which file to write to", then confirm before writing | the target file, resolved from the build target. Plus: these primitives are canon, do not propose alternatives. |
| `shape` | three to five clarifying questions; spec persist is opt-in | primary action · default-visible vs disclosed · what success looks like · who the user is. Plus: the persist is auto-confirmed. |
| `craft` | declares a Craft Read, then builds | the direction is settled — execute it, do not re-derive. |
| `finalize` | nothing — read-only, findings only | pointers to the acceptance bar, direction and audit so it does not re-derive them. |

**Recipe coverage is partial.** `craft` ships `recipe-dashboard.md`, `recipe-landing.md` and
`recipe-auth.md`. **There is no e-commerce recipe** — `craft` says so and refuses to improvise one,
falling back to standard build mode. That is the right behaviour, and G5 compensates by treating the
G4 acceptance bar as the recipe. Authoring a local `recipe-ecommerce.md` is the durable fix once a
second commerce surface exists to generalise from.

**Knobs** to pass from intake: `CRAFT_LEVEL` (7 default, 5 in ship-fast), `MOTION_INTENSITY`
(1–3 when G7 is off), `VISUAL_DENSITY`, `DESIGN_VARIANCE`.

**Known gap:** SEO strategy is explicitly out of scope — that is why G8 exists.

## taste-skill (Leonxlnx) — direction and references

| Gate | Skill | Note |
|---|---|---|
| G2 | `imagegen-frontend-web` | one horizontal image per section; needs image generation |
| G2 | `brandkit` | identity boards, logo systems — only for brand work, not surfaces |
| G3 | `design-taste-frontend` | default direction vendor at VARIANCE ≤6 |
| G3 fallback | `high-end-visual-design` | shorter, blunter; use if the primary is unavailable |
| all | `full-output-enforcement` | modifier — on for every gate writing a long file |

## impeccable (pbakaus) — high-variance direction

G3 at VARIANCE ≥7. One v4.5.2 skill with internal modes (`impeccable shape`,
`impeccable audit`, …), Apache 2.0, and a launcher at `<dir>/scripts/impeccable`.
The launcher can download its upstream binary on first use. The earlier bake-off
used v4.0.4, so its cost and quality comparison does not validate this revision.
Never put it in the same context as another orchestrator.

## emil-kowalski — motion (G7)

`motion-design` (timing, easing, choreography) → `emil-design-eng` (component feel, springs) →
`apple-design` only when the surface has gestures, drag, or sheets. Read-only planners
`improve-animations` and `find-animation-opportunities` are `design-tools` territory, not gates.

## ibelick/ui-skills — motion performance (G7)

`fixing-motion-performance` closes G7: compositor-only properties, perf budget,
`prefers-reduced-motion`. Short and prescriptive by design.

## web-quality / Addy Osmani — audit (G8)

`seo` · `core-web-vitals` · `accessibility` · with `performance`, `best-practices`, and the umbrella
`web-quality-audit` available. See `third-party/README.md` for redistribution attribution.

## Availability

Every owner named above must resolve from this plugin's bundled inventory. Image generation and
browser-based verification still require the relevant runtime tools. Check those capabilities before
starting a gate that needs them.
