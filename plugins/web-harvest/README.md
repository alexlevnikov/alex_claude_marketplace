# Web Harvest

The **retrieval router for the open web**. One skill, five hosted backends, one
job: given "get me something from the web," classify it and run it on the right
backend — search when you don't know the URLs, scrape when you do, unblock when
the site fights back, use a ready-made Actor when someone already solved that
site. Cheapest tool first, escalate only on failure.

**Costs nothing to leave enabled.** All five servers are HTTP connectors: no
local process is started, and the connection happens on the first call. Enable it
at user scope and forget about it.

For the other half of the web — driving a live browser, debugging a page, and
disassembling its traffic — install the sibling **`browser-lab`** plugin. Rule of
thumb: **web-harvest retrieves; browser-lab interacts.** If the data can be
reached by requesting URLs, it's web-harvest. If it needs behaving like a user in
a browser (or seeing what the browser itself is doing), it's browser-lab. The two
chain cleanly, and each works fine without the other.

## The skill

**`web-harvest`** classifies the request, names the route, runs it, and verifies
it got real content rather than a block page. It loads a playbook on demand:
`references/search.md` (Exa vs Tavily), `references/scrape-extract.md`
(Firecrawl scrape/crawl/map/extract), `references/structured-and-unblocking.md`
(Bright Data and Apify, and when the extra cost is justified).

## MCP servers

All five are hosted HTTP endpoints — **zero local processes**.

| Server | Endpoint | Covers | Key |
| --- | --- | --- | --- |
| `firecrawl` | `mcp.firecrawl.dev/v2/mcp` | Clean scrape → markdown, crawl, map, structured extract | Keyless works for Search/Scrape/Parse; `FIRECRAWL_API_KEY` unlocks crawl/extract + the developer index |
| `exa` | `mcp.exa.ai/mcp` | Neural/semantic web search, find-similar, deep research, URL → markdown | `EXA_API_KEY` |
| `tavily` | `mcp.tavily.com/mcp/` | Fast agent-tuned factual search + content extraction | `TAVILY_API_KEY` |
| `brightdata` | `mcp.brightdata.com/mcp` | Anti-bot Web Unlocker, SERP scraping, structured datasets (Amazon, LinkedIn, Maps, Instagram…) | `BRIGHTDATA_API_TOKEN` |
| `apify` | `mcp.apify.com` | Thousands of site-specific Store Actors + `rag-web-browser`, managed large runs | `APIFY_TOKEN` |

## Setup — keys

Keys go in **`env` in `~/.claude/settings.json`**, which Claude Code reads however
it was launched:

```json
{
  "env": {
    "FIRECRAWL_API_KEY": "fc-...",
    "EXA_API_KEY": "...",
    "TAVILY_API_KEY": "tvly-...",
    "BRIGHTDATA_API_TOKEN": "...",
    "APIFY_TOKEN": "apify_api_..."
  }
}
```

Restart Claude Code after editing, then prove every key with a real API call:

```bash
bash validate-keys.sh
```

(`validate-keys.sh` lives at the marketplace root and is shared by all plugins.)

**Do not** rely on `export` lines in `~/.zshrc`. The desktop app launches from
the GUI and never reads your shell profile, so `${EXA_API_KEY}` interpolates to
empty and the server answers 401. This was the actual bug that motivated the
plugin — see `docs/specs/2026-08-19-web-harvest-split-design.md`.

Get keys at firecrawl.dev, exa.ai, tavily.com, brightdata.com, apify.com — all
have a free tier. A server whose key is unset simply won't authenticate; the
others still work and the skill routes around it.

## Usage

Just describe the task — the skill triggers and routes it.

- "Research the latest sauna heater regulations and give me sources." → exa/tavily
- "Scrape our competitor's product pages into clean markdown." → firecrawl scrape
- "Pull name, price, and stock for every product under /saunas on competitor.com." → firecrawl map + extract
- "Get current Amazon pricing for these 20 competitor SKUs." → Bright Data structured dataset
- "This site blocks me — get the page anyway." → Bright Data Web Unlocker
- "Scrape all Google Maps reviews for these locations." → Apify Actor / Bright Data

**Chained with `browser-lab`:** "Find our top 5 competitors, log into each
pricing page, and extract their tiers." → web-harvest (exa search) → browser-lab
(playwright login) → web-harvest (firecrawl extract).

## Responsible use

Search and retrieval at scale can cross legal and ethical lines. Use this plugin
only to collect what you're authorized to collect; respect Terms of Service,
`robots.txt`, rate limits, paywalls, and auth boundaries; don't use unblocking or
proxies to defeat access controls you aren't entitled to bypass; don't harvest
personal data without a lawful basis (be especially careful with
LinkedIn/Instagram-style profile data); treat any returned tokens or PII as
secrets. The skill enforces these guardrails and declines requests aimed at
fraud, spam, mass personal-data harvesting, or circumventing security.

## Components

| Component | Count | Purpose |
| --- | --- | --- |
| Skills | 1 | `web-harvest` — search/scrape/crawl/extract router |
| MCP servers | 5 | firecrawl, exa, tavily, brightdata, apify — all `http`, 0 processes |
| Agents | 0 | Not needed |
| Hooks | 0 | Not needed |
