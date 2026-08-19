---
name: web-harvest
description: >
  Use this skill for any task about getting information or data FROM the web — search,
  scraping, crawling, or structured extraction — when the goal is to retrieve content, not to
  drive or debug a live browser. Triggers on: search the web, research a topic, find sources,
  find the latest on X, scrape this page or site, get the content of a URL, turn a page into
  markdown, extract fields from a site, crawl a whole website, map a site's URLs, pull
  competitor / product / pricing data, monitor prices, get reviews or listings, or scrape
  Amazon / LinkedIn / Google Maps / Instagram. It routes across five bundled MCP servers — Exa
  and Tavily (web search), Firecrawl (clean scrape / crawl / extract), Bright Data (anti-bot
  unblocking + structured datasets), and Apify (site-specific scraper Actors) — picking the
  cheapest tool that works, escalating on failure, and handing off to the sibling browser-lab
  plugin for live clicking, logging in, or debugging.
metadata:
  version: "0.1.0"
---

# Web Harvest

The retrieval router for the open web. One job: given "get me something from the
web," classify it and run it on the right backend — search when you don't know
the URLs, scrape when you do, unblock when the site fights back, and use a
ready-made Actor when someone has already solved that exact site. Pick the
cheapest tool that works, escalate only on failure, and hand interaction/debug
work to the `browser-lab` plugin.

This skill is a **decision-maker, not a doer of everything at once.** Name the
route before you act, run it, verify you got real content, and stop.

## Scope: what this skill owns vs. what it hands off

| The task is really about… | Owner |
| --- | --- |
| **Finding / reading / extracting web content** (search, scrape, crawl, structured data) | **web-harvest** (this skill) |
| **Driving a live page** — click, type, fill forms, log in, multi-step flows | hand off to the **browser-lab** plugin → playwright |
| **Debugging a page** — console errors, slowness, performance, Lighthouse | hand off to the **browser-lab** plugin → chrome-devtools |
| **Reverse-engineering / intercepting a site's own API traffic**, replaying requests | hand off to the **browser-lab** plugin → mitmproxy |

**`browser-lab` is a separate plugin and may not be installed.** Check by
capability — is any tool available that drives a live browser or reads its
console/network? — **never by tool name**, because the namespace changes with the
plugin that ships the server. If nothing can drive a browser, say so in one line,
name `browser-lab` and how to get it (`/plugin` → `alex-claude-marketplace` →
install & enable `browser-lab`, then restart the session), and **carry on with
whatever this skill can still do**. Never stop the task on a missing sibling.

Rule of thumb: **web-harvest retrieves; browser-lab interacts.** If the data can
be reached by requesting URLs, it's web-harvest. If it requires *behaving like a
user in a browser* (or you need to see what the browser itself is doing), it's
browser-lab. The two are designed to chain: e.g. web-harvest finds the pages →
browser-lab logs in and drives the flow → web-harvest extracts the result.

## The five servers and what each owns

| Job | Server | Why it wins here |
| --- | --- | --- |
| **Find** — you don't have the URLs; discover pages/sources for a topic or question | **exa** (neural/semantic, find-similar, research agent) or **tavily** (fast factual answers tuned for agents) | LLM-ready results without scraping first; cheapest way to answer "what/where is…" |
| **Fetch & extract** — you have URL(s); want clean markdown, structured fields, a crawl, or a URL map | **firecrawl** (`scrape`, `crawl`, `map`, `search`, `extract`) | Fast JS-rendered rendering → clean markdown / schema'd JSON with no browser wiring |
| **Unblock & structured feeds** — the site blocks bots, needs geo/residential IPs, or is a big platform with a ready dataset (Amazon, LinkedIn, Instagram, Google Maps, SERPs) | **brightdata** (Web Unlocker + pre-built structured datasets) | Purpose-built anti-bot + maintained structured scrapers for the hard, high-value sites |
| **Ready-made site scrapers** — a specific site/platform already has a maintained scraper, or you need a big managed run | **apify** (thousands of Store Actors + `rag-web-browser`) | Skip building a scraper; someone already did, and it runs managed at scale |

All retrieval lives here. `browser-lab` ships no scraping backend of its own, so
a browser-lab task that grows into a real search/crawl/structured job routes to
this skill.

## Routing decision guide — classify first, then act

Work top-down; take the **first** match:

1. **"Search / research / find info / answer using the web"** (no specific URL) →
   **search first**. Use **exa** for exploratory, semantic, or "find pages like
   this / research this deeply" work; use **tavily** for fast, factual,
   question-answering lookups. Only scrape afterward if you need the *full*
   content of a specific result. See `references/search.md`.

2. **"Get / read / extract from this URL (or handful of URLs)"** → **firecrawl
   `scrape`** (add an `extract` schema if they want specific fields). See
   `references/scrape-extract.md`.

3. **"Crawl this whole site / get every page under X / map the site"** →
   **firecrawl `map`** to discover URLs, then `crawl` (or scrape the mapped
   URLs). See `references/scrape-extract.md`.

4. **Firecrawl returned a block / 403 / empty body / CAPTCHA, OR the target is a
   known anti-bot or geo-locked site** → escalate to **brightdata** Web
   Unlocker. See `references/structured-and-unblocking.md`.

5. **Target is a big platform with a maintained dataset or Actor** (Amazon,
   LinkedIn, Instagram, TikTok, Google Maps/Search, Zillow, marketplaces, social
   profiles) → skip generic scraping. Prefer **brightdata** structured datasets
   for the covered domains; use an **apify** Store Actor when there's a
   purpose-built scraper for that exact site or you need a large managed run. See
   `references/structured-and-unblocking.md`.

6. **Needs login, clicking, or multi-step interaction to even reach the data** →
   **hand off to the `browser-lab` plugin** (playwright drives it). Come back here
   to extract once the content is on screen. If browser-lab isn't installed, say
   so, name it, and fall back to what retrieval alone can reach — a Bright Data
   or Apify route often gets the page without driving a browser at all.

Many real jobs chain: **search (exa/tavily) → scrape/extract (firecrawl) →
unblock or structured-scrape the ones that failed (brightdata/apify)**. Sequence
the servers; don't fire all five at one target.

## Cost-aware escalation ladder

Always climb from cheap+simple to expensive+heavy, and **stop at the first rung
that returns real data**:

1. **Search API** (exa/tavily) — pennies per query, no scrape needed. If the
   answer or snippet is enough, stop here.
2. **Firecrawl scrape/extract** — cheap per page, clean output. Default for known
   URLs on normal sites.
3. **Bright Data Web Unlocker** — use only when firecrawl is blocked or the site
   is known-hostile. Costs more per request; worth it for the pages that matter.
4. **Bright Data structured dataset / Apify Actor** — for high-value platforms
   where a maintained scraper saves you from fighting anti-bot at all. Priced per
   record/result or compute; reserve for real volume or hard targets.

Do **not** jump straight to Bright Data / Apify for an ordinary page — that burns
money on a job firecrawl would do for a fraction of the cost. Do **not** loop
firecrawl against a site that clearly blocks it — escalate after one clean
failure.

## Standard operating procedure

1. **Classify & state the route.** Say which server(s) you'll use and why,
   in order. One line.
2. **Search before you scrape** when the URLs aren't given. It's cheaper and
   often sufficient.
3. **Run the cheapest viable tool first**, then escalate per the ladder only on
   failure.
4. **Verify you got real content.** Check the result isn't an empty body, a
   block page, a login wall, or a CAPTCHA before treating it as data. If it is,
   escalate — don't hand the user a block page as an answer.
5. **Extract to the shape asked for.** If the user wants fields (price, title,
   rating…), use a schema (`firecrawl extract`, or a structured dataset/Actor)
   rather than dumping raw markdown and hoping.
6. **Report source + method.** Cite the URLs used and note which tool got them,
   so results are reproducible and the user knows the provenance (and cost tier).

## Quick server cheat-sheet

**exa** — `web_search_exa` (semantic web search → clean content), `web_fetch_exa`
(URL → clean markdown), plus optional `web_search_advanced_exa` (filters, date
ranges, domain include/exclude, subpage crawl) and `agent_run` (multi-step
research with structured output). Best for discovery, "find similar," and deep
research.

**tavily** — `tavily-search` (real-time web search, agent-tuned, returns direct
answers + sources), `tavily-extract` (pull clean content from given URLs). Best
for fast factual Q&A and grounding.

**firecrawl** — `firecrawl_scrape` (page → markdown/HTML/screenshot),
`firecrawl_crawl` (multi-page), `firecrawl_map` (discover a site's URLs fast),
`firecrawl_search` (search + scrape in one), `firecrawl_extract` (schema/LLM
structured extraction across pages). The default workhorse for known URLs.

**brightdata** — Web Unlocker (fetch any URL as markdown/HTML through anti-bot +
residential/geo IPs), `search_engine` (SERP scraping), and `web_data_*`
structured collectors for covered platforms (Amazon, LinkedIn, Instagram,
Google Maps, and more). Enable `PRO_MODE` for the full structured-tool set. The
escalation tier for blocked/hard/high-value sites.

**apify** — `search-actors` (find a scraper for a site in the Store),
`fetch-actor-details` (read its input schema), `call-actor` (run it),
`apify/rag-web-browser` (general scrape+read). Use when a purpose-built Actor
already exists for the target or you need a large managed run.

## Environment prerequisites (API keys)

All five backends are hosted HTTP services and need keys. They are read from
`env` in `~/.claude/settings.json` — **not** from the shell environment, which
Claude Code never sees when it is launched from the GUI. Each key is
optional-but-recommended; set the ones for the tiers you'll use:

- **exa** → `EXA_API_KEY` (https://exa.ai) — search + research.
- **tavily** → `TAVILY_API_KEY` (https://tavily.com) — search + extract.
- **firecrawl** → keyless works for basic `scrape`; **`FIRECRAWL_API_KEY`**
  (https://firecrawl.dev) unlocks `crawl`, `extract`, and higher limits. Set it
  before relying on crawl/extract.
- **brightdata** → `BRIGHTDATA_API_TOKEN` (https://brightdata.com) — unblocking +
  structured datasets. Optional `PRO_MODE=true` for the full tool set.
- **apify** → `APIFY_TOKEN` (https://apify.com) — Store Actors.

If a server's key is missing, say so plainly and route to the next viable tool
(e.g. no Bright Data key → try firecrawl, or ask the user to add the key for the
hard target). Free tiers exist on all five for evaluation. A 401 from a backend
means its key is missing or wrong in `~/.claude/settings.json` — say which key,
don't retry the same call. `bash validate-keys.sh` at the marketplace root proves
every key with a real API call.

## Responsible use

Search and retrieval at scale can cross legal and ethical lines. Operate within
these bounds (the same guardrails `browser-lab` applies to interaction):

- Scrape only what the user is authorized to collect. Respect Terms of Service,
  `robots.txt`, rate limits, and authentication/paywall boundaries. Don't use
  unblocking or proxies to defeat access controls the user isn't entitled to
  bypass.
- Don't harvest personal data without a lawful basis; be especially careful with
  profile/social scraping (LinkedIn, Instagram, etc.).
- Treat any returned credentials, tokens, or personal data as sensitive; never
  echo secrets into logs or the final answer.
- If a request looks aimed at fraud, spam, mass personal-data harvesting, or
  circumventing security, decline and explain why.

## References

Load the relevant playbook when you start that kind of work:

- `references/search.md` — Exa vs Tavily: when to use which, key parameters,
  research patterns, and how to chain search → scrape.
- `references/scrape-extract.md` — Firecrawl `scrape`/`crawl`/`map`/`extract`
  patterns, structured-schema extraction, and crawl-scoping to avoid runaway
  cost.
- `references/structured-and-unblocking.md` — Escalating to Bright Data (Web
  Unlocker + structured datasets) and Apify (Store Actors): when to skip generic
  scraping, choosing between them, and cost control.
