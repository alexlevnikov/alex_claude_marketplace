# Collisions

Twelve places where more than one vendor covers the same ground. Without a rule the router picks by
coin flip, and the user learns nothing from the answer. Each rule below is a *discriminator* — a
question whose answer names the tool.

## 1. Accessibility — three vendors

| Tool | Size | Take it when |
|---|---|---|
| `fixing-accessibility` (ibelick) | 140 lines | A specific thing is broken: focus ring, tab order, a missing label. Minutes, not hours. |
| `accessibility` (osmani) | 450 lines, WCAG 2.2 | The question is *compliance* — an audit, a conformance level, a client requirement, pre-launch. |
| `audit` (ui-craft) | in-context | You are mid-build and do not want to leave the build's context. |

**Discriminator:** is this a named defect, a compliance question, or a build-time check?

## 2. Performance — three vendors

| Tool | Take it when |
|---|---|
| `core-web-vitals` (osmani) | A metric is named — LCP, INP, CLS — or ranking is the motive. |
| `performance` (osmani) | The complaint is weight and load: payload, fonts, images, critical path, caching. |
| `fixing-motion-performance` (ibelick) | The slow thing is specifically an animation. |

**Discriminator:** a metric, a payload, or a moving thing?

## 3. Motion — five vendors

| Tool | Take it when |
|---|---|
| `motion-design` (emil) | Designing motion: timing, easing, choreography, from nothing. |
| `emil-design-eng` (emil) | One component should feel better — springs, the invisible details. |
| `apple-design` (emil) | Direct manipulation: drag, swipe, sheets, interruptibility, momentum. |
| `animate` / `delight` (ui-craft) | The project already has a motion token system and you are staying inside it. |
| `design-motion-principles` | A visible review is wanted — its audit emits an HTML report with looping demos. |

**Discriminator:** designing, polishing, gesturing, staying in-system, or reporting?

## 4. Polish — two vendors, one name

`polish` as installed is the **ui-craft** lens — it reads `.ui-craft/brief.md` and the project's
tokens. `impeccable` also has an internal `polish` mode, reachable only as `impeccable polish`.

**Rule:** default to `polish`. Reach for `impeccable polish` only when the user names impeccable, and
remember it is an orchestrator — it wants its own context.

## 5. Review — five tools

| Tool | Take it when |
|---|---|
| `critique` | An opinion is wanted. |
| `heuristic` | A number is wanted, or something a PM will read. |
| `audit` | A technical a11y pass inside a build session. |
| `web-quality-audit` | Metrics across performance, a11y, SEO, best practices at once. |
| `finalize` | A merge/ship decision is wanted. |

**Discriminator:** opinion, number, defect list, metrics, or verdict?

## 6. States — two ui-craft lenses

`unhappy` is state-*design*: it inventories non-happy states and refactors impossible booleans into
a state machine. `harden` is state-*production*: skeletons, i18n, offline, permissions, first-run.

**Rule:** `unhappy` before `harden`. Running `harden` on a surface with no state model gives you
decorated chaos.

## 7. Copy — two vendors

`clarify` (ui-craft) owns product microcopy: errors, empty states, CTAs, voice matrix, reading
level. The `ux:copy-writer` agent from the ux plugin owns longer-form and marketing voice.

**Rule:** if it lives inside a component, `clarify`.

## 8. Tokens — two entry points

`tokens` (ui-craft) establishes or audits the three-layer spine. The **brand contract** owns the
actual values. `tokens` may never propose different hues for YOURSAUNAS — if it does, the contract
wins and the proposal is discarded.

## 9. Typography — two vendors

`typeset` (ui-craft) works the scale, tracking and hierarchy of an existing pairing.
`high-end-visual-design` (taste-skill) changes the pairing's *character* toward expensive.

**Rule:** if the typefaces stay, `typeset`.

## 10. Responsive — two vendors

`adapt` (ui-craft) fixes breakpoints on a layout that basically works. A layout that is wrong at
every width is not a responsive problem — it is a composition problem, and that is `design-pipeline`.

## 11. SEO — one vendor, one boundary

`seo` (osmani) is the only SEO skill installed; ui-craft explicitly defers strategy to it. But
ui-craft's `metadata.md` owns the *correctness* of metadata already being emitted.

**Rule:** ranking, structured data, sitemaps → `seo`. "Is this title tag well-formed" mid-build →
ui-craft.

## 12. 3D — two sources

The ten `threejs-*` skills (repaired 2026-08-20) are technique references: fundamentals, loaders,
materials, lighting, shaders, geometry, textures, animation, interaction, postprocessing. The
`core-3d-animation` plugin covers the same ground at a framework level (react-three-fiber, babylon).

**Rule:** vanilla Three.js → `threejs-*`. React → `core-3d-animation:react-three-fiber`. And note
that neither is a design skill: they build a competent scene inside whatever page they are given.
