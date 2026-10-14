---
name: browser-lab
description: >
  This skill should be used for any browser automation, web debugging, or
  network reverse-engineering task — when the user wants to "automate a
  browser", "fill out a form on a site", "scrape a page", "debug why a page
  is slow/broken", "check console errors", "inspect network requests", "see
  what API a website calls", "reverse-engineer a site's API", "capture the
  requests a page makes", "replicate/replay an HTTP request", "turn a request
  into curl or code", or "intercept and modify traffic". It routes the task
  across bundled Playwright, Chrome DevTools, and mitmproxy MCP servers and
  explains which tool to use for what. For pure retrieval — searching the web,
  scraping/crawling sites, or extracting structured data at scale with no live
  browser needed — use the sibling `web-harvest` plugin instead.
metadata:
  version: "0.3.0"
---

# Browser Lab

Orchestrate three bundled MCP servers to cover the full spectrum of live-browser
work: driving pages, debugging the frontend, disassembling a site's network
traffic, and replicating its requests. This skill is the router — pick the
right server for each job, chain them, and fall back gracefully.

## The three servers and what each owns

| Job | Server | Why |
| --- | --- | --- |
| Drive the page (navigate, click, type, forms, screenshots, multi-step flows) | **playwright** | Deterministic accessibility-tree driving, multi-browser, token-cheap, no vision needed |
| Debug the frontend (console errors, network waterfall, performance traces, storage, Lighthouse) | **chrome-devtools** | Full Chrome DevTools Protocol — the only server with deep perf/console/network inspection |
| Disassemble & intercept raw traffic (TLS MITM, modify/replay requests, extract tokens, generate curl) | **mitmproxy** | Sees all HTTP(S) below the browser; built for interception, replay, and API pattern detection |

Rule of thumb: **playwright acts, chrome-devtools inspects, mitmproxy disassembles.** When two servers can do a thing (e.g. both playwright and chrome-devtools can click), let the table above decide ownership so you don't load two competing toolsets for the same step.

**Retrieval is not in this plugin.** Search, scraping, crawling, and structured
extraction belong to the sibling **`web-harvest`** plugin, which routes them
across Firecrawl, Exa, Tavily, Bright Data, and Apify with cost-aware escalation.

## Routing decision guide

Classify the request first, then act:

- **"Automate / do X on this site"** → playwright. See `references/automation.md`.
- **"Why is this page broken / slow / erroring?"** → chrome-devtools. See `references/debugging.md`.
- **"What does this site call under the hood / what's its API?"** → start with chrome-devtools `list_network_requests` for a quick read; escalate to mitmproxy when you need to intercept, modify, or capture traffic the DevTools panel can't (native apps, service workers, non-browser clients). See `references/network-disassembly.md`.
- **"Replicate / replay / turn into curl or code this request"** → mitmproxy for capture+replay+token chaining; shell out to `curlconverter` for HAR/curl → code. See `references/request-replication.md`.
- **"Get the content/data from this page/site"** → **hand off to the `web-harvest` plugin**; that is its whole job. Keep it here only when the data is behind interaction or login — then playwright drives to the content and web-harvest extracts it.

`web-harvest` is a separate plugin and may not be installed. Detect it **by capability** — is any tool available that searches or scrapes the web? — and **never by tool name**, since the namespace moves with the plugin that ships the server. If nothing can retrieve, say so in one line, name `web-harvest` and how to get it (`/plugin` → `alex-claude-marketplace` → install & enable `web-harvest`, then restart the session), and continue with what playwright can reach directly. Never stop the task on a missing sibling.

Many real tasks chain these: drive a flow with playwright → watch it in chrome-devtools → capture the key call with mitmproxy → replicate it with curl. Sequence the servers; don't try to do everything in one.

## Standard operating procedure

1. **Confirm scope and authorization.** Read the "Responsible use" section below before any interception, replay, or scraping work.
2. **State the plan.** Name which server(s) you'll use and in what order.
3. **Start the browser/proxy once.** Reuse the session across steps rather than re-launching per action.
4. **Prefer structured reads over screenshots.** Use playwright `browser_snapshot` and chrome-devtools `take_snapshot` (accessibility tree) before falling back to screenshots + coordinate clicks.
5. **Capture evidence.** For debugging, pull the actual console messages, network entries, and perf insights — don't infer. For network work, save the raw request/response (headers + body).
6. **Verify the result.** After automating, assert the expected end state (element visible, URL, response code). After replicating a request, diff the replayed response against the original captured one.

## Quick server cheat-sheet

**playwright** — `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_take_screenshot`, `browser_file_upload`, `browser_evaluate` (run JS in page), `browser_console_messages`, `browser_network_requests`, `browser_wait_for`, tab tools, coordinate `*_xy` fallbacks, `browser_pdf_save`.

**chrome-devtools** — `navigate_page`, `list_network_requests`, `get_network_request` (full headers/body/timing), `list_console_messages`, `get_console_message`, `evaluate_script`, `performance_start_trace`/`performance_stop_trace`/`performance_analyze_insight`, `lighthouse_audit`, `emulate` (CPU/network throttle, device), heap-snapshot suite, `take_screenshot`.

**mitmproxy** — `start_proxy`/`stop_proxy`/`set_scope`, `get_traffic_summary`, `search_traffic`, `inspect_flow` (returns curl equivalent), `add_interception_rule` (inject_header / replace_body / block), `set_global_header`, `replay_flow` (resend with modified method/headers/body), `extract_from_flow`, `set_session_variable`/`extract_session_variable` (token chaining), `detect_auth_pattern`, `get_api_patterns`, `export_openapi_spec`, `generate_scraper_code`.

## Environment prerequisites

- **playwright / chrome-devtools**: need Node.js and a local Chrome/Chromium. They run via `npx`; first launch downloads the package.
- **chrome-devtools attaches, it does not launch.** It runs with `--autoConnect` and drives the user's already-open Chrome, which is why several sessions can use it at once and why the user's logins are already present. This needs remote debugging enabled once at `chrome://inspect/#remote-debugging`. **If a call fails because no browser can be attached to, say so and name that toggle — do not switch the server to `--isolated` or a private profile to work around it, and never enable it on the user's behalf.** Anything that only needs a browser to act in, rather than the user's own session, belongs to playwright: it brings its own browser and never touches the personal profile.
- **mitmproxy**: needs `uv` (for `uvx`) and, for HTTPS interception, its CA certificate trusted by the client under test (visit `mitm.it` through the proxy, or install the cert). Without the trusted CA it can only see plaintext HTTP and TLS metadata.
- **request replication codegen**: `curlconverter` is invoked via `npx curlconverter` — no install needed beyond Node.

All three servers are keyless and local — this plugin needs no API key. (Retrieval keys live in `web-harvest`.)

If a server is missing its prerequisite, say so plainly and offer the fallback (e.g. use chrome-devtools network reads if the mitmproxy CA isn't trusted yet).

## Responsible use

Network disassembly, interception, and request replication are powerful and can enable abuse. Operate within these bounds:

- Only intercept, replay, or automate against sites the user **owns or is explicitly authorized to test**. For anything else, confirm authorization before proceeding.
- Respect Terms of Service, `robots.txt`, rate limits, and authentication boundaries. Do not defeat access controls the user is not entitled to bypass, and do not harvest personal data without a lawful basis.
- Treat captured tokens, cookies, and credentials as secrets: never echo them into logs or the final response, and scrub them from any saved artifacts.
- If a request looks aimed at fraud, credential theft, scraping protected personal data, or circumventing security, decline and explain why.

## References

Load the relevant playbook when you start that kind of work:

- `references/automation.md` — Playwright driving patterns, forms, auth, waiting, multi-tab.
- `references/debugging.md` — Console, network waterfall, performance traces, storage/cookies, Lighthouse.
- `references/network-disassembly.md` — Capturing and mapping a site's real API with chrome-devtools + mitmproxy.
- `references/request-replication.md` — Turning captured requests into curl/code, auth/token chaining, replay & verification.
