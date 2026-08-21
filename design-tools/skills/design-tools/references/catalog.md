# Catalog

Every routable tool, grouped by verb. `W` writes to code · `R` reports only. Verified present
2026-08-20 in `design-studio/.claude/skills/`.

Orchestrator-class skills are deliberately absent from this catalog — they belong to
`design-pipeline`.

## LOOK — how it looks

| Tool | Vendor | | For | Not for |
|---|---|---|---|---|
| `typeset` | ui-craft | W | type scale, tracking, optical size, hierarchy | choosing a typeface for a new brand |
| `colorize` | ui-craft | W | palette application, theming, dark mode | inventing a palette — the contract owns that |
| `adapt` | ui-craft | W | breakpoints, mobile layout, container queries | a layout that is wrong at every width |
| `distill` | ui-craft | W | cutting noise from an over-built surface | a surface that is under-built |
| `bolder` | ui-craft | W | amplifying personality within the direction | a new direction |
| `quieter` | ui-craft | W | restraint, toning down, reducing accent load | fixing a genuinely broken hierarchy |
| `extract` | ui-craft | W | pulling repeated markup into components/tokens | first-time token setup |
| `high-end-visual-design` | taste-skill | W | making an existing surface read as expensive | wholesale redesign |
| `shape` | ui-craft | W* | wireframing one new section (*writes a spec, not code) | a whole surface — that is the pipeline |

## FEEL — how it moves

| Tool | Vendor | | For | Not for |
|---|---|---|---|---|
| `motion-design` | emil | W | timing, easing, choreography from scratch | fixing jank — that is performance |
| `emil-design-eng` | emil | W | component feel, springs, the invisible details | page-level motion planning |
| `apple-design` | emil | W | gestures, drag, sheets, interruptibility, momentum | non-interactive entrance animation |
| `delight` | ui-craft | W | purposeful micro-interactions | a motion system |
| `animate` | ui-craft | W | animation inside the project's motion tokens | taste questions — use emil |
| `fixing-motion-performance` | ibelick | W | jank, layout thrashing, reduced-motion, budgets | how it should feel |
| `design-motion-principles` | Kowalski/Krehel/Tompkins | W/R | build **or** audit motion; audit emits an HTML report with looping demos | when a plain text answer is wanted |
| `find-animation-opportunities` | emil | **R** | where motion is missing but earned | improving motion that exists |
| `improve-animations` | emil | **R** | audit all motion, produce a plan for other agents | one component |
| `animation-vocabulary` | emil | R | naming an effect you can only describe | designing one |

## FIX — make it survive production

| Tool | Vendor | | For | Not for |
|---|---|---|---|---|
| `unhappy` | ui-craft | W | states before the happy path, state machines | cosmetic error styling |
| `harden` | ui-craft | W | skeletons, empty, error, partial, i18n, offline, permissions | greenfield state design — `unhappy` first |
| `clarify` | ui-craft | W | UX copy: errors, empty states, CTAs, voice | marketing copy |
| `fixing-accessibility` | ibelick | W | fast keyboard / focus / ARIA fixes | a compliance audit |
| `accessibility` | osmani | W | full WCAG 2.2, POUR, conformance | a one-line focus-ring fix |
| `core-web-vitals` | osmani | W | LCP, INP, CLS by name | general page weight |
| `performance` | osmani | W | payload, critical path, fonts, images, caching | a named Core Web Vital |
| `seo` | osmani | W | meta, structured data, sitemap, robots, on-page | copywriting for humans |
| `best-practices` | osmani | W | security headers, CSP, modernisation | design questions |

## JUDGE — decide, change nothing

| Tool | Vendor | | For |
|---|---|---|---|
| `critique` | ui-craft | R | UX critique, no code changes |
| `heuristic` | ui-craft | R | 0–100 score, PM-ready audit, personas |
| `audit` | ui-craft | R | technical a11y audit inside a build session |
| `web-quality-audit` | osmani | R | umbrella: performance + a11y + SEO + best practices |
| `finalize` | ui-craft | R | READY / NOT READY / BLOCKED before merge |
| `ui-craft:design-reviewer` + `ui-craft:a11y-auditor` | ui-craft | R | two fresh-context reviewers in parallel on a diff |

## LOOKUP — answer, don't act

`baseline-ui` (ibelick — the base tidiness checklist) · `pick-ui-library` · `ask-sonner` ·
`animation-vocabulary` · `threejs-*` (ten skills: fundamentals, loaders, materials, lighting,
shaders, geometry, textures, animation, interaction, postprocessing) ·
`context7` MCP for current library docs · `figma-dev-mode-mcp-server` MCP for a Figma entry point,
which needs Figma running locally.

## MODIFIER

`full-output-enforcement` (taste-skill) — bans placeholders and truncated output. Turn it on
whenever the chosen tool will write a long file.

## Absent — do not route here

`gsap-core`, `gsap-react`, `ui-ux-pro-max` (enabled in settings, unresolvable in session) ·
`theme-factory`, `brand-guidelines`, `canvas-design`, `web-artifacts-builder`, `webapp-testing`
(not in this harness) · `review-animations` (in the registry, never installed).
