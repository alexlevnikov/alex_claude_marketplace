# Browser Lab

A power toolkit for the **whole web** — bundled behind two orchestration skills
so Claude always picks the right tool for the job:

- **`browser-lab`** — *act on & debug a live browser and its traffic*: browser
  automation, deep frontend debugging, network disassembly, and HTTP request
  replication.
- **`web-harvest`** — *find, fetch & extract web content/data at scale*: web
  search, scraping, crawling, and structured data extraction, with cost-aware
  escalation and clean handoff back to `browser-lab` for live interaction.

Rule of thumb across the plugin: **web-harvest retrieves; browser-lab
interacts.** If the data can be reached by requesting URLs, it's web-harvest. If
it needs behaving like a user in a browser (or seeing what the browser itself is
doing), it's browser-lab.

## Skills

### `browser-lab` — interact & debug
Routes any live-browser/network task across the local core servers and loads
deeper playbooks on demand (automation, debugging, network disassembly, request
replication).

### `web-harvest` — search, scrape & extract
The retrieval router. Classifies the request and picks the cheapest backend that
works — search when you don't have URLs, scrape when you do, unblock when the
site fights back, use a ready-made Actor when someone already solved that site —
and escalates only on failure. Loads playbooks for search, scrape/extract, and
unblocking/structured feeds.

## MCP servers

**Local core (browser-lab — no account required):**

| Server | Package | Covers | Needs |
| --- | --- | --- | --- |
| `playwright` | `@playwright/mcp` (Microsoft) | Driving pages: navigate, click, forms, uploads, multi-step flows, screenshots | Node.js + Chromium |
| `chrome-devtools` | `chrome-devtools-mcp` (Google) | Deep debugging: console, network waterfall, performance traces, memory, Lighthouse | Node.js + Chrome |
| `mitmproxy` | `mitmproxy-mcp` | Network disassembly: TLS interception, modify/replay requests, extract tokens, curl/codegen, API mapping | `uv` + trusted mitmproxy CA for HTTPS |

**Cloud retrieval (web-harvest — need API keys; free tiers available on all):**

| Server | Package / endpoint | Covers | Key |
| --- | --- | --- | --- |
| `firecrawl` | hosted `mcp.firecrawl.dev` | Clean scrape → markdown, crawl, map, structured extract | Keyless for basic scrape; `FIRECRAWL_API_KEY` for crawl/extract + limits |
| `exa` | hosted `mcp.exa.ai` | Neural/semantic web search, find-similar, deep research, URL → markdown | `EXA_API_KEY` |
| `tavily` | hosted `mcp.tavily.com` | Fast agent-tuned factual search + content extraction | `TAVILY_API_KEY` |
| `brightdata` | `@brightdata/mcp` | Anti-bot Web Unlocker, SERP scraping, structured datasets (Amazon, LinkedIn, Maps, Instagram…) | `BRIGHTDATA_API_TOKEN` |
| `apify` | hosted `mcp.apify.com` | Thousands of site-specific Store Actors + `rag-web-browser`, managed large runs | `APIFY_TOKEN` |

Firecrawl is shared by both skills (browser-lab's quick "harvest" + web-harvest's
main workhorse).

## Setup

**Local core** self-installs on first use via `npx`/`uvx`. Prerequisites:
- **Node.js** (playwright, chrome-devtools) and a local **Chrome/Chromium**.
- **`uv`** for mitmproxy (`uvx mitmproxy-mcp`). For HTTPS interception, trust the
  mitmproxy CA (route a browser through the proxy and visit `mitm.it`).

**Cloud retrieval** — set the keys for the tiers you'll use as environment
variables (the `.mcp.json` reads them via `${VAR}`):

```bash
export FIRECRAWL_API_KEY=fc-...        # crawl/extract + higher limits
export EXA_API_KEY=...                  # exa search/research
export TAVILY_API_KEY=tvly-...          # tavily search/extract
export BRIGHTDATA_API_TOKEN=...         # unblocking + structured datasets
export APIFY_TOKEN=apify_api_...        # store actors
```

Get keys at firecrawl.dev, exa.ai, tavily.com, brightdata.com, apify.com. Each
has a free tier for evaluation. A server whose key is unset simply won't connect;
the others still work, and `web-harvest` routes around it.

**Optional Firecrawl key in the endpoint:** to enable `crawl`/`extract`, swap the
firecrawl entry's URL to the keyed form:
`"url": "https://mcp.firecrawl.dev/${FIRECRAWL_API_KEY}/v2/mcp"`.

**Optional Bright Data structured tools:** add `"PRO_MODE": "true"` to the
brightdata server's `env` to expose the full `web_data_*` structured-dataset tool
set (Amazon, LinkedIn, etc.) beyond the default Web Unlocker + SERP tools.

## Usage

Just describe the task — the right skill triggers and routes it.

**web-harvest (retrieval):**
- "Research the latest sauna heater regulations and give me sources." → exa/tavily
- "Scrape our competitor's product pages into clean markdown." → firecrawl scrape
- "Pull name, price, and stock for every product under /saunas on competitor.com." → firecrawl map + extract
- "Get current Amazon pricing for these 20 competitor SKUs." → Bright Data structured dataset
- "This site blocks me — get the page anyway." → Bright Data Web Unlocker
- "Scrape all Google Maps reviews for these locations." → Apify Actor / Bright Data

**browser-lab (interaction & debugging):**
- "Automate filling out the signup form on example.com and screenshot it." → playwright
- "Figure out why this page takes 6 seconds to load." → chrome-devtools
- "Show me what API this dashboard calls and its auth." → chrome-devtools → mitmproxy
- "Capture the search request and turn it into a Python script." → mitmproxy → curlconverter

**Chained across skills:** "Find our top 5 competitors, log into each pricing
page, and extract their tiers." → web-harvest (exa search) → browser-lab
(playwright login) → web-harvest (firecrawl extract).

## Optional add-ons

Paste into `.mcp.json` under `mcpServers` to extend coverage:

**Browserbase + Stagehand (cloud stealth browsers, natural-language actions):**
```json
"browserbase": {
  "type": "http",
  "url": "https://mcp.browserbase.com/mcp",
  "headers": { "Authorization": "Bearer ${BROWSERBASE_API_KEY}" }
}
```

**browser-use (local autonomous "just do this task" agent):**
```json
"browser-use": {
  "command": "uvx",
  "args": ["--from", "browser-use[cli]", "browser-use", "--mcp"],
  "env": { "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}" }
}
```

**Observability connectors (OAuth, add via Cowork connector settings):** Sentry,
Jam.dev, PostHog — for when the bug lives in production telemetry, not a live page.

## Responsible use

Automation, interception, replay, search, and scraping can enable abuse. Use this
plugin only against sites you own or are authorized to test; respect Terms of
Service, `robots.txt`, rate limits, paywalls, and auth boundaries; don't use
unblocking/proxies to defeat access controls you aren't entitled to bypass; don't
harvest personal data without a lawful basis (be especially careful with
LinkedIn/Instagram-style profile data); treat captured tokens/cookies/PII as
secrets and never expose them. Both skills enforce these guardrails and will
decline requests aimed at fraud, spam, mass personal-data harvesting, or
circumventing security.

## Components

| Component | Count | Purpose |
| --- | --- | --- |
| Skills | 2 | `browser-lab` (interact/debug) + `web-harvest` (search/scrape/extract) |
| MCP servers | 8 | playwright, chrome-devtools, mitmproxy, firecrawl, exa, tavily, brightdata, apify |
| Agents | 0 | Not needed |
| Hooks | 0 | Not needed |
