# Search playbook — Exa vs Tavily

Use a **search API before scraping** whenever you don't already have the URLs, or
when a good snippet/answer would satisfy the request. It's an order of magnitude
cheaper than scraping and returns LLM-ready text.

## Which search server?

| Use case | Pick | Why |
| --- | --- | --- |
| "Answer this question using the web", fast factual grounding, current events | **tavily** (`tavily-search`) | Agent-tuned; returns a direct answer + ranked sources with clean snippets |
| Exploratory / semantic "find pages *like* this", topic research, discovery | **exa** (`web_search_exa`) | Neural search finds conceptually similar content keyword search misses |
| Deep, multi-step research with a structured result | **exa** (`agent_run`) | Runs an autonomous research loop and returns organized output |
| Filtered search — date range, include/exclude domains, subpage crawl | **exa** (`web_search_advanced_exa`) | Fine-grained control over the result set |
| Just need clean markdown of a URL a search already returned | **exa** (`web_fetch_exa`) or **tavily** (`tavily-extract`) | One-hop fetch without spinning up firecrawl |

Rule of thumb: **tavily answers, exa discovers.** For "what is / who is / latest
on" → tavily. For "find me sources / similar companies / research this" → exa.
When unsure, tavily is the cheaper first probe; escalate to exa for depth.

## Patterns

**Ground a factual claim (cheapest path):**
`tavily-search` with a focused query → read the returned answer + top sources. If
that settles it, stop. No scraping needed.

**Research a topic broadly:**
`web_search_exa` (or `agent_run` for depth) → collect the most relevant URLs →
only then deep-scrape the few that matter with firecrawl. Don't scrape every
result; search snippets often suffice.

**Search → scrape handoff:**
1. Search (exa/tavily) to get candidate URLs.
2. Triage: which URLs actually need full content vs. which the snippet covers.
3. For the ones that need full text/fields → `firecrawl_scrape` / `extract`
   (see `scrape-extract.md`). Escalate blocked ones to Bright Data.

**Domain-scoped search:**
Use `web_search_advanced_exa` with include/exclude domains and a date range to
cut noise (e.g. only official docs, only the last 12 months).

## Cost notes

- Both bill per search (~$5–8 / 1,000). Free tiers ≈ 1,000 searches/month each —
  plenty for evaluation.
- A search + one targeted scrape almost always beats scraping a whole site to
  find one fact. Search is the cheap filter that decides what's worth scraping.
- Don't re-run near-identical queries; refine one query rather than firing many.
