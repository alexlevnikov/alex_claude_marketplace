# Prior art: dynamic MCP loading and skill-orchestrator marketplaces

**Date:** 2026-08-18
**Status:** Research — no decision taken
**Question:** we build plugins as skill+tool orchestrators, hand a task to a skill,
and let it decide which tools it needs. How do others solve this, and is there
something better than what we have?

## TL;DR

The problem splits in two, and almost every project found solves only the first.

| Problem | Status |
| --- | --- |
| **Context** — tool schemas eat the window | **Already solved natively.** MCP Tool Search ships on by default (announced 2026-01-14), ~85% reduction. Most gateways in this list predate or duplicate it. |
| **Memory** — `stdio` servers start with every session | **Not solved by any of it.** Only scope, HTTP transport, or a gateway that owns the process lifecycle touches this. |

**Conclusion: we don't need a gateway yet.** Scope + HTTP transport is free and
addresses the actual pain. Revisit `mcpproxy-go` only if that proves insufficient.

## What is already native (and therefore not worth rebuilding)

- **MCP Tool Search** — deferred tool schemas, resolved on demand. On by default;
  `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` turns it off. Verified live: this
  setup's own MCP tools arrive deferred with no configuration.
- **`env.ENABLE_TOOL_SEARCH: "auto:0"`** in `~/.claude/settings.json` forces
  full on-demand loading. The older `ENABLE_EXPERIMENTAL_MCP_CLI` env var is dead.
  ([paddo.dev](https://paddo.dev/blog/claude-code-hidden-mcp-flag/))
- **Skills' three-level progressive disclosure** — ~100 tokens per skill for
  name+description; body loads only on fire. This is what our router pattern
  already rides on.
- Anthropic's [code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
  is the published form of the same idea.

## The landscape

Catalog: [e2b-dev/awesome-mcp-gateways](https://github.com/e2b-dev/awesome-mcp-gateways)
— 23 open-source + ~30 commercial gateways.

### Lazy-loading proxies — closest to our problem

| Project | What it does | Fit |
| --- | --- | --- |
| [smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go) | Local Go binary. One endpoint over many upstreams, BM25 `retrieve_tools` search, quarantine, Docker isolation for stdio children, macOS tray, Homebrew. Very active, spec-driven. | **Best candidate if we ever need one.** Single local process, no Docker required for the proxy itself. |
| [MarimerLLC/mcp-aggregator](https://github.com/MarimerLLC/mcp-aggregator) | Upstreams connect **on first use**, idle connections reaped, servers registered at runtime without restart. MCP + REST. .NET. | The clearest statement of the lifecycle we sketched. |
| [RaiAnsar/mcp-gateway](https://github.com/RaiAnsar/mcp-gateway) | Exposes 4 lightweight tools instead of every schema; claims ~95% context reduction. | Context-only — solves the problem we no longer have. |
| [mcp-shark/lazy-tool](https://github.com/mcp-shark/lazy-tool) | Local-first, 5 meta-tools, search-before-invoke. Aimed at 50+ tool catalogs. | Same. |
| [Toolport](https://toolport.app/) | Local-first, ~90% fewer tool tokens, secrets in the OS keychain, tool-integrity checks. | Commercial. Keychain handling is the interesting part. |

### Aggregators / orchestrators

[metatool-ai/metamcp](https://github.com/metatool-ai/metamcp) (aggregator +
middleware, Docker) · [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge)
(federation, virtual servers) · [agentic-community/mcp-gateway-registry](https://github.com/agentic-community/mcp-gateway-registry)
(semantic-search discovery) · [VeriTeknik/pluggedin-mcp](https://github.com/VeriTeknik/pluggedin-mcp)
(proxy + cached discovery) · [adamwattis/mcp-proxy-server](https://github.com/adamwattis/mcp-proxy-server).

### Enterprise/governance — not our shape

[microsoft/mcp-gateway](https://github.com/microsoft/mcp-gateway) (K8s lifecycle),
Kuadrant, Pomerium, Open Edison, Gate22. These solve multi-tenant policy, not a
laptop's RAM.

### Lightweight alternative to a gateway

[McPick](https://scottspence.com/posts/mcpick-manage-mcp-servers-and-plugins-in-claude-code)
— `npx mcpick enable/disable <server>`, runnable by Claude itself. Toggling
config beats building a proxy when the goal is just "not all of them at once".

## The most useful signal: AIRIS walked it back

[agiletec-inc/airis-mcp-gateway](https://github.com/agiletec-inc/airis-mcp-gateway)
is listed in awesome-mcp-gateways as a Docker multiplexer aggregating *60+ tools
behind 7 meta-tools, 97% context reduction, HOT/COLD server lifecycle, circuit
breaker* — i.e. exactly the ambitious version of what we were considering.

Its **current README says the opposite**: don't register the gateway as a
permanent global MCP. The agent opens a **short-lived session from a skill**, and
only when it genuinely needs that backend; everything else goes to native tools
or purpose-built skills.

They built the big multiplexer and retreated to *skill decides → open briefly →
close*. That is the design we already have. Worth knowing before rebuilding
their first version.

## Sharp edge for our plugins: namespacing

[ruflo#2685](https://github.com/ruvnet/ruflo/issues/2685) — a plugin's bundled
MCP server gets namespaced on the marketplace install path: tools that are
`mcp__<server>__*` standalone become **`mcp__plugin_<plugin>_<server>__*`**.
Skills that hard-code the bare names break when installed as a plugin.

Confirmed live here: our Exa tool resolves as
`mcp__plugin_browser-lab_exa__web_search_exa`. This is precisely why
`AUTHORING.md` says to detect by capability and never hard-code tool names — it
is a real failure mode, not a stylistic preference.

## Known-broken in our own setup

`browser-lab/.mcp.json` interpolates `${EXA_API_KEY}`, `${TAVILY_API_KEY}`,
`${BRIGHTDATA_API_TOKEN}`. These are unset, so **exa and tavily return 401 on
every call** (verified 2026-08-18 while running this very research — both failed,
and the work fell back to keyless Firecrawl and WebSearch). This is the exact
failure the 2026-08-12 spec's Model B was introduced to eliminate: move them to
user-added connectors so the key lives in the connector store, or drop them.

## If we ever do build one

The insight that makes it worth it isn't lazy start — it's **transport**. A
gateway exposed over **HTTP is one process for the whole machine**, not one per
session. Eight sessions × ten `stdio` servers collapses to one gateway plus
whatever it starts on demand. A gateway that is itself `stdio` re-creates the
problem once per session and is not worth building.
