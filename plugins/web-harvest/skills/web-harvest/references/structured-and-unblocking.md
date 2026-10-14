# Unblocking & structured feeds — Bright Data + Apify

This is the **escalation tier**: reach for it only when a search API + Firecrawl
can't get the data — either the site actively blocks bots, or it's a big platform
where a maintained scraper beats fighting anti-bot yourself. Both cost more per
result, so route here deliberately, not by default.

## Bright Data — the unblocker + structured datasets

Two distinct capabilities:

**1. Web Unlocker** — fetch *any* URL as clean markdown/HTML through Bright
Data's anti-bot + residential/geo IP network. This is the answer to "Firecrawl
got blocked / 403 / CAPTCHA" and to geo-restricted content. Also `search_engine`
for scraping SERPs (Google/Bing) reliably.

**2. Structured datasets (`web_data_*`)** — maintained, schema'd collectors for
high-value platforms: Amazon (products, reviews, search), LinkedIn (people,
companies, jobs), Instagram, TikTok, Google Maps, and more. These return
clean records without you writing selectors or fighting layout changes. Enable
`PRO_MODE=true` to expose the full structured-tool set.

Use Bright Data when:
- Firecrawl failed on a page that matters (escalate for *that* page).
- The target is one of the covered platforms and you want reliable structured
  records (e.g. Amazon competitor pricing, LinkedIn company data).
- You need geo-specific results (pricing/availability that varies by country).

## Apify — thousands of ready-made site scrapers

Apify Store has purpose-built, maintained **Actors** for thousands of specific
sites. Instead of building a scraper, find one and run it.

Flow:
1. `search-actors` — find an Actor for the target site/platform.
2. `fetch-actor-details` — read its input schema (what params it needs).
3. `call-actor` — run it with your inputs; get structured results.
4. `apify/rag-web-browser` — a general-purpose scrape+read Actor when no
   site-specific one fits.

Use Apify when:
- A purpose-built Actor already exists for that exact site (often true for niche
  platforms Bright Data's datasets don't cover).
- You need a **large managed run** (thousands of pages) with retries/queue
  handled for you.
- The job is recurring and you want a repeatable, parameterized scraper.

## Bright Data vs Apify — choosing

| Situation | Prefer |
| --- | --- |
| Page is blocked but you just need its content | **Bright Data** Web Unlocker |
| Covered major platform (Amazon/LinkedIn/Maps/Instagram) | **Bright Data** structured dataset |
| Niche site with an existing community Actor | **Apify** Store Actor |
| Large managed crawl with queueing/retries | **Apify** |
| Reliable SERP scraping | **Bright Data** `search_engine` |
| Geo-specific residential IPs required | **Bright Data** |

When both could work, Bright Data is usually the faster path for the platforms it
covers; Apify wins on breadth of long-tail sites and big managed runs.

## Cost control

- These tiers bill per record/result (Bright Data ≈ $1–1.5 / 1,000 results;
  browser navigation per GB) or per compute (Apify Compute Units + per-result
  Actor fees). Reserve them for the pages that justify the cost.
- Don't route an ordinary page here — that's Firecrawl's job at a fraction of the
  price. Escalate the *specific* hard/high-value targets, not the whole batch.
- Both charge mainly for successes; still, estimate volume (how many records)
  and tell the user before a large run.
- Missing key → say so and fall back: no Bright Data key → try Firecrawl or ask
  the user to add it for the hard target; no Apify key → check if Bright Data
  covers the platform instead.
