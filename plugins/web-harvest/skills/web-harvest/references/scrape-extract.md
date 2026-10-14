# Scrape & extract playbook — Firecrawl

Firecrawl is the default workhorse once you **have the URL(s)** and the site
isn't actively hostile. It renders JS, returns clean markdown, and can extract
structured fields against a schema.

## Pick the right Firecrawl tool

| You want… | Tool | Notes |
| --- | --- | --- |
| One page as clean markdown/HTML | `firecrawl_scrape` | Add `formats` for screenshot/HTML; the default markdown is LLM-ready |
| Specific fields from a page/pages (price, title, rating, specs) | `firecrawl_extract` | Pass a JSON schema; returns structured JSON, not prose |
| Every page under a section / a whole site | `firecrawl_crawl` | **Scope it** (see below) or cost explodes |
| Just the list of URLs a site exposes | `firecrawl_map` | Fast, cheap; run this before a crawl to see the shape |
| Search the web and scrape the hits in one call | `firecrawl_search` | Handy, but for pure discovery a dedicated search API (exa/tavily) is cheaper |

## Structured extraction (the high-value pattern)

When the user wants *data*, not *text*, always extract to a schema instead of
dumping markdown:

```
firecrawl_extract(
  urls = ["https://competitor.com/products/sauna-x"],
  schema = {
    "type": "object",
    "properties": {
      "name":  {"type": "string"},
      "price": {"type": "number"},
      "currency": {"type": "string"},
      "in_stock": {"type": "boolean"},
      "features": {"type": "array", "items": {"type": "string"}}
    }
  }
)
```

Returns JSON you can put straight into a table/spreadsheet. This is the right
tool for competitor-pricing and product-catalog jobs on normal sites.

## Crawl scoping — avoid runaway cost

`firecrawl_crawl` bills per page. A naive crawl of a big site can burn thousands
of credits. Before crawling:

1. `firecrawl_map` first to see how many URLs exist and their pattern.
2. Constrain: set `includePaths` / `excludePaths` (or an equivalent URL filter)
   to only the section you need, and cap `limit` / depth.
3. If you only need a handful of known pages, **don't crawl** — scrape that list
   directly.
4. State the expected page count to the user before a large crawl.

## When Firecrawl isn't enough → escalate

Treat these as signals to stop retrying Firecrawl and move up the ladder
(`structured-and-unblocking.md`):

- Response is a block page, CAPTCHA, 403/429, or an empty/near-empty body.
- The site is a known anti-bot target (large marketplaces, social platforms) or
  is geo-restricted.
- You need residential/geo-specific IPs.

One clean failure is enough — escalate to Bright Data Web Unlocker rather than
looping. If the site is a big platform with a maintained dataset/Actor, skip
straight to the structured tools.

## Keys / limits

- Basic `scrape` works on the keyless hosted endpoint but is rate-limited.
- `crawl` and `extract` and higher limits need `FIRECRAWL_API_KEY`, read from
  `env` in `~/.claude/settings.json`. If it's missing and the user needs
  crawl/extract, ask them to add it there (or fall back to a search API for
  discovery).
