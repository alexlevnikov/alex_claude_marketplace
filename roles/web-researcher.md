# Web researcher

Install **`web-harvest`** for search, scraping, crawling, and structured
extraction. Add **`browser-lab`** when the site requires clicking, forms, login,
or browser-level debugging. The provider credentials for `web-harvest` stay in
the local runtime settings; this repository contains no keys.

## Start

| Task | Claude Code | Codex |
| --- | --- | --- |
| Find or extract web content | `/web-harvest:web-harvest <task>` | `$web-harvest:web-harvest <task>` |
| Interact with a live page | `/browser-lab:browser-lab <task>` | `$browser-lab:browser-lab <task>` |

Use the retrieval pack to find and extract sources. When a site requires a
browser session, hand the URL and the precise interaction goal to `browser-lab`.
Return source links, distinguish what was observed from what was inferred, and
keep authentication state outside the repository.
