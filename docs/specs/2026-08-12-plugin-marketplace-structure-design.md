# Personal Plugin Marketplace — Structure Design

**Date:** 2026-08-12
**Status:** Approved (brainstorming) → next: implementation plan
**Location:** `~/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins/`

## Goal

Restructure the single bundled `browser-lab` plugin into **three focused, composable plugins**
served from **one personal marketplace**, so tools can be enabled per job:

1. **browser-lab** — live browser: interaction, frontend debugging, network disassembly.
2. **web-harvest** — web search, scraping, crawling, structured extraction.
3. **design-lab** — design orchestrator (the 5-layer taste/motion/3D router being built).

## Decisions (locked in brainstorming)

| # | Decision | Choice |
|---|---|---|
| D1 | Install model | **One personal marketplace** at `claude_plugins/` root; enable plugins per project. |
| D2 | design-lab package | **Skills + agents only** — no MCP servers of its own. |
| D3 | Naming | `browser-lab` · `web-harvest` · `design-lab`. |
| D4 | Connector model | **browser-lab bundles** its 3 keyless MCP (Model A). **web-harvest & design-lab reference** manually-added connectors (Model B) — no `.mcp.json`. |
| D5 | Missing connector behavior | **Detect + guide, then continue** — never blocks; tells user how to add a missing connector, proceeds with what's available. Applies to both web-harvest and design-lab. |
| D6 | Key storage | Model-B connector keys are entered **when adding the connector** (Customize UI / `claude mcp add`), stored in Claude's connector store. **No keys and no secrets ever inside the iCloud-synced plugin folder.** `~/.claude/settings.json` `env` is only used if the user chooses to define a connector via env-interpolation; still outside iCloud. |
| D7 | design-lab council | For complex jobs, spin a **multi-agent design council** (distinct lenses that debate + surface perspectives). **Auto-fires on complexity and ALWAYS confirms the chosen direction with the user before building.** Simple tasks skip it. |
| D8 | design-lab wiki | design-lab ships a `README.md` **living wiki** cataloging every skill/tool it carries or references (layer, purpose, router-trigger, vendored/referenced status, source). |

## Directory layout

```
claude_plugins/                          # personal marketplace root (git repo, iCloud-synced)
├── .claude-plugin/
│   └── marketplace.json                 # lists all 3 plugins
├── browser-lab/
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json                        # playwright, chrome-devtools, mitmproxy   (keyless)
│   └── skills/browser-lab/
├── web-harvest/
│   ├── .claude-plugin/plugin.json
│   ├── README.md                        # copy-paste connector configs (URLs + which key)
│   └── skills/web-harvest/              # NO .mcp.json — references user-added connectors (Model B)
├── design-lab/
│   ├── .claude-plugin/plugin.json
│   ├── README.md                        # WIKI: catalog of every skill/tool, its layer, when the router picks it
│   ├── skills/
│   │   ├── design-lab/                  # router skill (task type + 3 taste dials + council trigger)
│   │   └── <vendored design skills>     # curated subset — see "Plugin 3 — vendored set" below
│   └── agents/                          # review agents + council lens agents (read-only)  — NO .mcp.json
├── scripts/                             # shared build.sh / doctor.sh / validate-keys.sh
├── docs/specs/                          # this spec
└── browser-lab.plugin                   # legacy zip — kept, no longer relied on
```

Install: `/plugin marketplace add "<claude_plugins path>"` once, then enable per project.

## Connector models

**Model A — bundle (browser-lab only).** Plugin ships `.mcp.json`; servers auto-start when enabled.
browser-lab's three servers are keyless local processes, so bundling means it works instantly with
no manual connector step and no secrets.

**Model B — reference (web-harvest, design-lab).** No `.mcp.json`. The skill routes *by capability*:
it discovers what tools are available (Tool Search / presence check) and uses whatever connectors the
user has added. Per D5, if a needed connector is absent it **tells the user exactly how to add it,
then continues with whatever is available**. Skills must not hard-code exact tool names (a
manually-added connector may be namespaced differently); they detect by capability. Consequence:
a Model-B plugin does nothing until the relevant connectors are added — the plugin ships the routing
*intelligence*, the user supplies the connectors.

## Plugin 1 — browser-lab

- **Content:** existing `browser-lab` skill + `.mcp.json` reduced to `playwright`, `chrome-devtools`,
  `mitmproxy`. Removes the 5 search/scrape servers and the `web-harvest` skill (they move to plugin 2).
- **Keys:** none (all keyless, `npx`/`uvx`-run).
- **plugin.json:** description/keywords rewritten to browser-only scope.

## Plugin 2 — web-harvest (Model B — reference)

- **Content:** the existing `web-harvest` skill only. **No `.mcp.json`.**
- **Connectors (user-added):** `firecrawl` (keyless), `exa`, `tavily`, `brightdata`, `apify`. The
  user adds whichever they need via Customize / `claude mcp add`; keys are entered there and stored in
  Claude's connector store, not in the plugin.
- **README.md:** ships copy-paste connector configs so adding them is one step, e.g.
  Exa → HTTP `https://mcp.exa.ai/mcp` header `x-api-key`; Tavily → HTTP
  `https://mcp.tavily.com/mcp/?tavilyApiKey=<key>` (key starts `tvly-`); Firecrawl → HTTP
  `https://mcp.firecrawl.dev/v2/mcp` (keyless); Bright Data / Apify likewise.
- **Skill update:** add a detect-and-guide preamble — route by capability, and if no search/scrape
  connector is present, point the user at the README then proceed with whatever is available.
- **plugin.json:** description/keywords rewritten to search/scrape scope; note it requires connectors.
- This resolves the original Exa/Tavily 401s by construction — keys now live in the connector, not in
  empty `${VAR}` refs.

## Plugin 3 — design-lab

- **Model:** skills + agents; Model B connectors; detect-and-guide degradation.
- **Router skill:** reads task type + 3 taste dials (VARIANCE / MOTION / DENSITY), routes across the
  5 layers per the research doc's routing table, and enforces the build→see→critique loop with a
  **hard Core Web Vitals perf gate** as the exit condition (aesthetic score alone does not "pass").

### Plugin 3 — vendored set (curated subset, per research §9.5 + approved additions)

| Layer | Vendored / pinned |
|---|---|
| L1 Taste | `frontend-design` (official), `taste-skill` family (dials + variants), **impeccable** (+ its detect CLI / live overlay), **awwwards** (premium/award intent) |
| L1+L3 Polish/Motion authority | **emil-design-eng** + **apple-design** (Emil Kowalski: spring physics, "should this animate at all?") |
| L2 Tokens/System | `theme-factory` + Design-Tokens (`--brand-hue`/OKLCH); **DESIGN.md 9-section schema** as the system-definition format |
| L3 Motion & 3D | `greensock/gsap-skills` (code), **Motion.dev skill** (`199-biotechnologies/motion-dev-animations-skill`, 120fps/springs/gestures), `freshtechbro` `core-3d-animation` bundle (3D), **ux-motion-teardown** (reference-site → spec input) |
| L4 Eyes | (via **browser-lab** plugin) Playwright + Chrome DevTools MCP |
| L5 Review/Gate | `ui-craft` review agents (aesthetic), **web-quality (Osmani)** pinned as the **CWV perf-gate engine**, **baseline-ui** polish pipeline, **design-motion-principles** (motion audit), **plugin87 Nielsen 6-dim rubric** (scoring + DS crosswalk) |
| Cross-cutting | Context7 (docs, referenced), Figma (referenced), Firecrawl (via web-harvest) |

Prior art to study before authoring: `master5d/claude-design-skills` (3-layer harness) and
`Shawnchee/frontend-god-mode` (consolidated master skill).

### Plugin 3 — design council (multi-agent debate mode)

For **complex** jobs (new premium page, 3D hero, full redesign, reference-match), the router spins a
**design council** — several read-only agents, each loaded with a distinct **lens**:

- **Creative Director** (awwwards + impeccable) — bold art direction, "one-of-a-kind on first load."
- **Motion/Interaction** (emil-design-eng + Motion.dev) — restraint, spring feel, "should this move?"
- **Systems/Minimalist** (tokens + minimalist taste) — coherence, rhythm, on-system discipline.
- **A11y + Performance** (web-quality + baseline-ui) — the perf-gate + accessibility conscience.

Each agent independently proposes a direction and **surfaces its perspective + disagreements**;
design-lab synthesizes the tension into **2–3 concrete directions** and, per **D7**, **auto-fires on
complexity and always stops to confirm the chosen direction with the user before building**. Simple
tasks skip the council and run single-threaded. Council agents are read-only (no file writes); they
return structured positions the router reconciles.

### Plugin 3 — README wiki (D8)

design-lab ships a `README.md` that is a **living wiki** of everything it carries or references:
every skill/tool, its layer (L1–L5), what it does, **when the router picks it**, vendored-vs-referenced
status, and the source link. It is the single index for "what's in the box," kept in sync as the
vendored set evolves.

### Scope of THIS project

Scaffold the plugin: manifest, README-wiki skeleton, router skill stub (task-type + dials + council
trigger), council + review agent stubs, and the vendored-set folder structure. **Full router logic,
the actual vendored skill copies, and the council reconciliation prompts = a separate spec/plan**
after the structure lands.

## API keys + iCloud safety (D6)

The marketplace root is in **iCloud Drive** → everything in it syncs to the cloud. Therefore **no
secrets in the plugin folder**, ever. With web-harvest and design-lab on Model B, connector keys are
entered when the connector is added and stored in Claude's connector store — nothing to put in the
repo at all. browser-lab needs no keys. `~/.claude/settings.json` `env` remains available only if the
user prefers to define a connector via env-interpolation (still outside iCloud), but it is no longer
required by any plugin. `.gitignore` in the marketplace root excludes any stray `.env`/secret files
as defense-in-depth.

## Tooling & migration

- Move/rework `build.sh`, `doctor.sh`, `validate-keys.sh` into `scripts/`, operating over all three
  plugins.
- Author `marketplace.json` listing the three plugins by relative path.
- Reduce `browser-lab/.mcp.json` to the 3 browser servers; the 5 search/scrape servers are **not**
  bundled anywhere — their configs move into `web-harvest/README.md` as copy-paste connector snippets.
- Move the `web-harvest` skill folder into the new `web-harvest/` plugin (skill-only, no `.mcp.json`).
- Legacy `browser-lab.plugin` zip: leave in place, stop relying on it (folder-based marketplace
  references dirs directly). Optionally regenerate via build script later.
- Commit each step to the marketplace git repo.

## Out of scope (future specs)

- design-lab's full router logic, vendored-skill selection, and perf-gate implementation.
- Publishing the marketplace beyond local use.
- Any change to the live in-session bundled browser-lab (harness-managed copy).

## Success criteria

- `/plugin marketplace add <root>` lists three plugins.
- Enabling **browser-lab** exposes its 3 browser MCP tools immediately (no setup).
- Enabling **web-harvest** adds only the `web-harvest` skill (no MCP servers); with the relevant
  connectors added by the user it routes correctly, and with none it detect-and-guides via the README.
- Enabling **design-lab** adds skills+agents with **no** new MCP servers; its router detects and
  guides for missing optional connectors and continues.
- No secret material exists anywhere under the iCloud-synced marketplace folder.
