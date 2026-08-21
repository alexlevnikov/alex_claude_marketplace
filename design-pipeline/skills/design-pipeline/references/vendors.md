# Vendor contracts

Verified present 2026-08-20 in `design-studio/.claude/skills/` (76 working skills). Before a run in
a **different** project, confirm the skills exist there — the pipeline is portable, the inventory is
not. A gate whose owner is missing uses its fallback and records the substitution in its artifact.

## ui-craft (educlopez) — the substrate

Owns G1, G4, G5, G6, G9. Twenty-five installed skills, thirty-three reference files, and the only
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

G3 at VARIANCE ≥7. One skill with internal modes (`impeccable shape`, `impeccable audit`, …),
Apache 2.0, ships `scripts/` including image generation. Roughly 3× the tool calls of
`design-taste-frontend`; in the group-01 bake-off it produced the most distinctive result and the
highest bill. Never in the same context as another orchestrator.

## emil-kowalski — motion (G7)

`motion-design` (timing, easing, choreography) → `emil-design-eng` (component feel, springs) →
`apple-design` only when the surface has gestures, drag, or sheets. Read-only planners
`improve-animations` and `find-animation-opportunities` are `design-tools` territory, not gates.

## ibelick/ui-skills — motion performance (G7)

`fixing-motion-performance` closes G7: compositor-only properties, perf budget,
`prefers-reduced-motion`. Short and prescriptive by design.

## web-quality / Addy Osmani — audit (G8)

`seo` · `core-web-vitals` · `accessibility` · with `performance`, `best-practices`, and the umbrella
`web-quality-audit` available. MIT licensed — the only vendor here safe to vendor verbatim.

## Availability notes (2026-08-20)

- **Present and wired:** every skill named above.
- **Repaired this session:** ten `threejs-*` skills and `design-motion-principles` were installed as
  nested repositories and invisible to Claude Code; now symlinked into `.claude/skills/`.
- **Absent despite being enabled:** `gsap-core` / `gsap-react` (greensock plugin) and
  `ui-ux-pro-max` — listed in `.claude/settings.json`, not resolvable in session. Do not route to them.
- **Absent in this harness:** `theme-factory`, `brand-guidelines`, `canvas-design`,
  `web-artifacts-builder`, `webapp-testing` (Anthropic local). `frontend-design` is available in
  plugin form only.
- **Deliberately not installed:** `epic-design` (a general-purpose mega-repo — kubernetes, finance,
  compliance; not a design vendor), `ux-ui-agent-skills` (five hard name collisions with installed
  skills), `styleseed` and `ux-skill` (already available as plugins).
