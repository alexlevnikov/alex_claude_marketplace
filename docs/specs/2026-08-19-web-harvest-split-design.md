# Wave 1: split web-harvest out, fix the keys

**Date:** 2026-08-19
**Status:** Design — awaiting review
**Supersedes:** the plugin split in `2026-08-12-plugin-marketplace-structure-design.md`
(D1 per-project scoping, and Model B for the cloud backends — both replaced below)

## Problem

`browser-lab` bundles two unrelated areas behind one plugin: driving a live
browser, and retrieving data from the web. That forces one enable/disable
decision on both, and the plugin ships eight MCP servers where a given task
needs at most a few.

Two concrete defects fall out of it:

1. **Exa and Tavily 401 on every call.** Their keys interpolate from
   `${EXA_API_KEY}` / `${TAVILY_API_KEY}`, which are exported in `~/.zshrc:22-26`.
   Claude Code's desktop app launches from the GUI and never reads `.zshrc`, so
   the variables are empty. Verified live on 2026-08-18: both failed mid-research
   and the work fell back to keyless Firecrawl. `setup-keys.sh` targets the same
   dead end (writes `~/.browser-lab-keys.env`, sources it from the shell profile)
   and therefore cannot fix it — neither that file nor the source line exists today.
2. **`brightdata` runs as a local `npx` process** although Bright Data offers a
   hosted endpoint, so it costs memory in every session for no reason.

## Requirement (Alex, 2026-08-19)

Plugins install at **user level**, and servers start **when used**. Per-project
scoping is explicitly rejected.

## Design

### Two plugins, each owning a whole area

| | `browser-lab` 0.3.0 | `web-harvest` 0.1.0 |
| --- | --- | --- |
| Area | live browser: drive, debug, disassemble traffic | retrieval: search, scrape, crawl, extract |
| Skill | `browser-lab` + its 4 references | `web-harvest` + its 3 references |
| Servers | playwright, chrome-devtools, mitmproxy | firecrawl, exa, tavily, apify, brightdata |
| Transport | stdio (keyless, local) | **http — all five** |
| Model | A (bundle) | A (bundle) |
| Cost per session | 3 processes | **0 processes** |
| Scope | user | user |

The area boundary and the cost boundary are the same line here, so splitting by
area costs nothing architecturally. The `web-harvest` skill and its `references/`
move wholesale into the new plugin; no content is rewritten.

`web-harvest` satisfies the requirement by construction: HTTP connectors hold no
process and connect on first call.

`browser-lab` cannot — all three servers are stdio-only, with no hosted variant
(verified 2026-08-19; Chrome DevTools' `--browser-url` / `--cdp-endpoint` select
which *browser* to attach to, not the MCP transport). It therefore still costs 3
processes per session, down from 8. Closing that gap needs a gateway and is
**wave 2** — tracked in `../IMPROVEMENT-LOG.md`.

### Keys

Move all five into `env` in `~/.claude/settings.json`, which Claude Code reads
regardless of how it was launched. Values already exist in `~/.zshrc:22-26`;
copy them, leave the shell exports alone (harmless, useful for CLI work).

```json
{ "env": {
  "FIRECRAWL_API_KEY": "…", "EXA_API_KEY": "…", "TAVILY_API_KEY": "…",
  "BRIGHTDATA_API_TOKEN": "…", "APIFY_TOKEN": "…"
} }
```

`setup-keys.sh` is deleted — it institutionalises the broken path, and a script
that looks like it works is worse than no script. `validate-keys.sh` is rewritten
to check the settings.json source and to prove each backend with a real call, not
merely a non-empty variable.

### Transports in the new `web-harvest/.mcp.json`

| Server | Config |
| --- | --- |
| firecrawl | `https://mcp.firecrawl.dev/v2/mcp`, header `Authorization: Bearer ${FIRECRAWL_API_KEY}` — keyless works but limits to Search/Scrape/Parse; the key unlocks crawl/extract and the developer index |
| exa | `https://mcp.exa.ai/mcp`, header `x-api-key: ${EXA_API_KEY}` — unchanged |
| tavily | `https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}` — unchanged |
| apify | `https://mcp.apify.com`, header `Authorization: Bearer ${APIFY_TOKEN}` — unchanged |
| brightdata | **changed** from `npx @brightdata/mcp` to `https://mcp.brightdata.com/mcp?token=${BRIGHTDATA_API_TOKEN}` |

All entries use `"type": "http"`. Claude Code does **not** accept
`"streamable-http"`; the wrong value fails silently as a permanent "connecting"
state rather than an error.

### Degradation across the split

The two plugins can now be enabled independently, so neither may assume the
other is present:

- `web-harvest`, on a task needing clicks or login, names `browser-lab`, says how
  to enable it, and continues with whatever is available. It never blocks (D5).
- `browser-lab` hands real retrieval jobs to `web-harvest` the same way.
- **Detection is by capability, never by tool name.** Tools are namespaced
  `mcp__plugin_<plugin>_<server>__*`, so exa is
  `mcp__plugin_browser-lab_exa__web_search_exa` today and
  `mcp__plugin_web-harvest_exa__*` after the move. Any hard-coded name breaks on
  this very migration.

### Marketplace

`marketplace.json` gains `web-harvest` 0.1.0 and bumps `browser-lab` to 0.3.0 —
a breaking change, since it loses five servers and a skill. `build.sh`,
`doctor.sh` and `validate-keys.sh` are shared tooling; keep one copy at the repo
root rather than duplicating per plugin.

## Not in this wave

- **The gateway** giving `browser-lab` lazy start (wave 2).
- **`design-lab`** from the 2026-08-12 spec.
- **Task-oriented router plugins** — considered and rejected 2026-08-19: Alex
  wants plugins that each cover a whole area, not per-task entry points.

## Acceptance

1. A fresh session with both plugins enabled at user scope shows all five
   `web-harvest` backends connected and **zero** new processes attributable to them:
   `ps -Ao rss=,command= | grep -Ei "mcp|npm exec"` is unchanged from before enabling.
2. Exa, Tavily, Bright Data, Apify and Firecrawl each answer a real query — no 401.
3. `browser-lab` accounts for exactly three MCP processes per session.
4. Disabling `browser-lab` leaves `web-harvest` fully working, and a click-requiring
   task produces a named suggestion to enable it rather than a failure.
5. No API key appears anywhere in the git repository.
