# Browser Lab

The **live-browser toolkit**: drive a page, debug what it's doing, disassemble
its network traffic, and replicate its requests. One orchestration skill routes
every task to the right server, so you describe the job and not the tooling.

For the other half of the web — search, scraping, crawling, structured
extraction — install the sibling **`web-harvest`** plugin. Rule of thumb:
**browser-lab interacts; web-harvest retrieves.** If it needs behaving like a
user in a browser (or seeing what the browser itself is doing), it's browser-lab.
If the data can be reached by requesting URLs, it's web-harvest. The two chain
cleanly, and each works fine without the other.

## The skill

**`browser-lab`** classifies the request, names the plan, and runs it, loading a
playbook on demand: `references/automation.md` (Playwright driving, forms, auth,
waiting, multi-tab), `references/debugging.md` (console, network waterfall,
performance traces, storage, Lighthouse), `references/network-disassembly.md`
(mapping a site's real API), `references/request-replication.md` (captured
request → curl/code, token chaining, replay & verification).

## MCP servers

All three are **local, keyless, and stdio** — no account, no API key.

| Server | Package | Covers | Needs |
| --- | --- | --- | --- |
| `playwright` | `@playwright/mcp` (Microsoft) | Driving pages: navigate, click, forms, uploads, multi-step flows, screenshots | Node.js + Chromium |
| `chrome-devtools` | `chrome-devtools-mcp` (Google) | Deep debugging: console, network waterfall, performance traces, memory, Lighthouse | Node.js + Chrome |
| `mitmproxy` | `mitmproxy-mcp` | Network disassembly: TLS interception, modify/replay requests, extract tokens, curl/codegen, API mapping | `uv` + trusted mitmproxy CA for HTTPS |

**Runtime cost, stated plainly:** stdio servers start with the session, not on
first use, so this plugin holds **three processes in every open session** whether
or not you touch a browser. Idle they are small (a few MB each); the weight
arrives when a browser actually launches. All three ship stdio-only with no
hosted variant, so the only way to close the gap is a gateway — **considered in
depth and declined**, see `docs/specs/2026-08-19-mcp-gateway-design.md`. If you
rarely do browser work, disable this plugin and enable it when you need it —
`web-harvest` is unaffected and costs nothing either way.

## Setup

Everything self-installs on first use via `npx`/`uvx`. Prerequisites:

- **Node.js** (playwright, chrome-devtools) and a local **Chrome/Chromium**.
- **Remote debugging enabled in Chrome**, one time, at
  `chrome://inspect/#remote-debugging`. `chrome-devtools` runs with
  `--autoConnect` and attaches to the Chrome you already have open instead of
  launching its own. Without this toggle it has no browser to attach to.

  This is what makes the server usable in more than one session at a time.
  Without it, each session tries to launch its own Chrome against the same
  profile directory and every session but the first fails with *"The browser is
  already running for …/chrome-profile"*. Attaching to one shared browser also
  means your existing logins are simply there.

  **Know what you are turning on.** With the remote debugging server running,
  any local process can drive your logged-in browser — mail, bank, anything you
  are signed into. Turn it on if you want deep debugging across sessions;
  leave it off and use `playwright`, which brings its own browser and never
  touches your profile, if you do not.
- **`uv`** for mitmproxy (`uvx mitmproxy-mcp`). For HTTPS interception, trust the
  mitmproxy CA: route a browser through the proxy and visit `mitm.it`. Without
  the trusted CA it sees only plaintext HTTP and TLS metadata.
- **`curlconverter`** for request codegen — invoked via `npx`, nothing to install.

Verify the environment from your Mac Terminal:

```bash
bash doctor.sh
```

(`doctor.sh` lives at the marketplace root and is shared by all plugins.)

## Usage

Just describe the task — the skill triggers and routes it.

- "Automate filling out the signup form on example.com and screenshot it." → playwright
- "Figure out why this page takes 6 seconds to load." → chrome-devtools
- "Show me what API this dashboard calls and its auth." → chrome-devtools → mitmproxy
- "Capture the search request and turn it into a Python script." → mitmproxy → curlconverter

**Chained with `web-harvest`:** "Find our top 5 competitors, log into each
pricing page, and extract their tiers." → web-harvest (exa search) → browser-lab
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

Keys for add-ons go in `env` in `~/.claude/settings.json`, never in a shell
profile — Claude Code launched from the GUI never reads `.zshrc`.

**Observability connectors (OAuth, add via connector settings):** Sentry,
Jam.dev, PostHog — for when the bug lives in production telemetry, not a live
page.

## Responsible use

Automation, interception, and replay are powerful and can enable abuse. Use this
plugin only against sites you own or are authorized to test; respect Terms of
Service, `robots.txt`, rate limits, and auth boundaries; don't defeat access
controls you aren't entitled to bypass; treat captured tokens, cookies, and PII
as secrets and never echo them into logs or answers. The skill enforces these
guardrails and declines requests aimed at fraud, credential theft, or
circumventing security.

## Components

| Component | Count | Purpose |
| --- | --- | --- |
| Skills | 1 | `browser-lab` — drive / debug / disassemble |
| MCP servers | 3 | playwright, chrome-devtools, mitmproxy — all `stdio`, 3 processes per session |
| Agents | 0 | Not needed |
| Hooks | 0 | Not needed |
