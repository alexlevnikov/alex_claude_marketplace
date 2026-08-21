# Improvement Log

Running log of how to make this marketplace better: what to change, what to
borrow from other projects, and which questions are still open. Newest entries
on top. Companion docs: `ARCHITECTURE.md` (how it works), `AUTHORING.md` (how to
build), `specs/` (dated design decisions).

---

## 2026-08-19 — Wave 2 declined. `browser-lab` 0.3.1 fixes the defect instead

**Decision (Alex, 2026-08-19): the gateway is not built.** The design stays in
`specs/2026-08-19-mcp-gateway-design.md` marked DECLINED, with the reasoning, so
that reopening it starts from the analysis rather than from zero.

**What separated the two things.** The gateway removes a *cost*; only one thing
was *broken*. `chrome-devtools` failed in every session but the one that won the
race for the Chrome profile — and that is fixed by a single flag, not by a
daemon. Everything else worked the whole time.

**`browser-lab` 0.3.1** adds `--autoConnect` to `chrome-devtools`. It attaches to
the Chrome you already have open instead of launching its own, so there is no
profile to contend over, every session can use it at once, and existing logins
are simply there. **It requires enabling remote debugging once** at
`chrome://inspect/#remote-debugging`, and the README states plainly what that
means: any local process can then drive the logged-in browser. `playwright`
remains the answer for anyone who would rather not — it brings its own browser
and never touches the personal profile.

**Why the gateway lost, on evidence gathered after it was approved:**

- Rai-onl publishes **no binaries** — v0.3.0 ships zero release assets — so it
  means installing a **Rust toolchain** (~1.4 GB) that nothing else here needs.
- It is a **thirteen-crate project** with OIDC, TLS and a credential store, for
  the job of putting three local servers behind a loopback port.
- The daemon would sit **in the path of all MCP traffic**, including the telegram
  token and n8n credentials over ssh.
- Against ~300 MB on an 8 GB machine.

**Two things worth keeping from the work, even though it shipped nothing:**

- **Read the source, not the README.** `common-creation/mcp-gateway` advertises
  "auto-start MCP servers on first request"; its own `main.go:41` calls
  `StartAll` at startup. Rai-onl documents neither lazy start nor reaping, yet
  its `router/src/dispatch.rs` shows both a request-filled bridge slot and
  liveness-driven replacement. Both READMEs were wrong in opposite directions.
- **Check whether the criterion is worth its weight.** "Idle reaping" was written
  as a blocking requirement. With one daemon the worst case is 3 processes
  machine-wide against 21 today, so reaping buys zero-instead-of-three, not
  three-instead-of-21. It should never have been blocking.

**Accepted permanently:** 3 stdio processes per open session for `browser-lab`.
`ARCHITECTURE.md` §6 now says so instead of pointing at a pending wave.

---

## 2026-08-19 — Wave 1 verified live, and what the measurement found

First session after the restart. Everything wave 1 claimed was re-checked against
running software rather than against the config.

**Wave 1 holds.** `validate-keys.sh` passes 11/11 and `doctor.sh` passes all seven
sections. All five `web-harvest` backends answered with real data through their
plugin-namespaced tools — exa, tavily, firecrawl, brightdata, apify. The 401s are
gone. `@brightdata/mcp` no longer spawns in new sessions: retrieval costs **zero
local processes**, as designed.

**`browser-lab` is 2 of 3.** playwright and mitmproxy answer. `chrome-devtools`
fails with *"The browser is already running for …/chrome-profile"* — eight
sessions contend for one profile directory and only the first to launch Chrome
works. This is a real defect, not a cosmetic one, and it is what wave 2 fixes.

**The measurement, on 8 live sessions:** 170 `stdio` processes, **643 MB** (1658 MB
counting whole session trees, on an 8 GB machine). `browser-lab` is 355 MB of it.
All eight parent processes were confirmed alive — there is nothing to reap, so
only the gateway moves this number. Full table in
`specs/2026-08-19-mcp-gateway-design.md`.

**Two duplicates worth removing independently of wave 2:**

- **`firecrawl-mcp` runs locally in every session** (24 processes, 90 MB) from
  `firecrawl@claude-plugins-official`, duplicating the hosted Firecrawl that
  `web-harvest` already serves over HTTP for free. Not a free removal: that plugin
  also carries eleven `firecrawl-*` skills, which go with it.
- **`mcp-remote` shims for inkeep persist** (8 processes, 62 MB) although the
  config moved to `type: http` on 2026-08-18. Sessions opened before that change
  still hold them; they die with those sessions.

**Wave 2 decided (Alex, 2026-08-19):** scope is every `stdio` server on the
machine; one shared Chrome with per-session tabs, because logins must survive
(`--isolated` is therefore rejected); and we adopt a ready **transparent bridge**
rather than build one, proving it on a stand first.

Meta-routers are out, and the reasoning generalises: `mcpproxy-go`,
`MikkoParkkola/mcp-gateway` and `mcp-aggregator` all collapse backend tools behind
a search-and-invoke pair and sell it as context savings — **which MCP Tool Search
already gives us natively, for free**. Paying indirection on every call for a
benefit we already hold is a bad trade. Candidates that survived:
[Rai-onl/mcp-gateway](https://github.com/rai-onl/mcp-gateway) and
[common-creation/mcp-gateway](https://github.com/common-creation/mcp-gateway).

**Method note worth keeping:** `doctor.sh` and `validate-keys.sh` both passed
while `chrome-devtools` was broken. They check reachability and credentials, not
whether a tool answers. A config that validates is not a plugin that works —
verify by calling the tool.

---

## 2026-08-19 — Wave 1 shipped: web-harvest split out, keys fixed

Implemented `specs/2026-08-19-web-harvest-split-design.md` on branch
`wave-1-web-harvest-split`.

**What changed**

- **`web-harvest` 0.1.0** is its own plugin: the skill and its three references
  moved wholesale, and all five backends are now `"type": "http"` — including
  `brightdata`, which was the last local `npx` process among them
  (`mcp.brightdata.com/mcp?token=…`). **0 processes per session.**
- **`browser-lab` 0.3.0** keeps only playwright, chrome-devtools and mitmproxy.
  It lost firecrawl with the split, so its skill no longer claims a retrieval
  route: it hands the whole area to `web-harvest`, by capability and never by
  tool name. **3 processes per session**, unchanged and still the open problem.
- **Keys moved to `env` in `~/.claude/settings.json`** and all five verified with
  a real API call — exa, tavily, firecrawl, brightdata, apify each answered 2xx.
  The 401s are gone at the source.
- **`setup-keys.sh` deleted.** It wrote `~/.browser-lab-keys.env` and sourced it
  from the shell profile — the exact dead end that caused the bug. A script that
  looks like it works is worse than no script.
- **`validate-keys.sh` rewritten** to check *two* things: that the key sits in
  settings.json (the only place Claude Code reads) **and** that it authenticates.
  A key found only in `~/.zshrc` now FAILS the source check even when the call
  succeeds — the call proves the key, not the wiring.
- **Shared tooling moved to the repo root.** `build.sh` takes a plugin directory
  (or `--all`) and refuses to package a directory containing key-shaped strings.
- **`*.plugin` archives are no longer committed.** Installation happens over git
  from the marketplace, so a checked-in archive is a stale copy — `browser-lab.plugin`
  had gone stale the moment the split landed. Build one with `build.sh` when you
  need to hand a plugin over out-of-band.

**Operational note worth remembering:** this marketplace is installed from
`github.com/alexlevnikov/alex_claude_marketplace`, **not** from the iCloud working
copy. Editing here changes nothing until the branch is merged and pushed; then
`/plugin` → update the marketplace → enable `web-harvest` → restart the session.

**Still open:** the wave-2 gateway. `browser-lab` is now the only thing costing
memory, which is exactly the shape the gateway decision needs — one plugin, three
stdio servers, no hosted variant. See the next entry.

---

## 2026-08-19 — Requirement change: user-level install, servers start on use

**Alex:** the plugins should install at **user level**, and servers should start
**when they are used**, not per project. Per-project scoping is off the table.

This is a harder requirement than the one `ARCHITECTURE.md` §4 answers, and it
changes what has to be built.

### What that requirement costs, by backend

| Backend | Transport | Can it start on use? |
| --- | --- | --- |
| firecrawl, exa, tavily, apify, brightdata | **http** | **Yes, already** — HTTP connectors hold no process; the connection happens on the first call. Nothing to build. |
| playwright, chrome-devtools, mitmproxy | **stdio only** | **No** — verified 2026-08-19: all three ship as `npx`/`uvx` stdio servers with no hosted endpoint. Chrome DevTools' `--browser-url` / `--cdp-endpoint` flags govern which *browser* it attaches to, not its MCP transport. |

So `web-harvest` satisfies the requirement by construction once brightdata moves
to its hosted URL. `browser-lab` cannot — not without a gateway.

### Open decision: how browser-lab gets lazy start

A gateway is the only mechanism. The decisive property is that **the gateway
itself must be HTTP** — an `stdio` gateway is re-spawned per session and
reproduces the exact problem it was meant to solve.

Target shape:

```
Claude Code (any session, user scope)
├── web-harvest   → 5 HTTP connectors            → 0 processes
└── browser-lab   → 1 HTTP url to the gateway    → 0 processes per session
                       ↓  one daemon per machine
                       ├── playwright       ← started on first call
                       ├── chrome-devtools  ← started on first call
                       └── mitmproxy        ← started on first call
```

Today's cost is 3 stdio servers × every open session (8 sessions ⇒ 24 processes).
The target is one daemon plus whatever is actually in use.

Candidates in `specs/2026-08-18-mcp-dynamic-loading-prior-art.md`:
[mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go) (Go binary, Homebrew,
http-streamable, BM25 tool search, documented Claude setup) versus a small
purpose-built gateway. **Not yet decided.**

### Verify during implementation

- Claude Code wants `"type": "http"` — **not** `"streamable-http"`. The wrong
  value fails silently as a permanent "connecting" state.
- Whether the chosen gateway shuts idle upstreams down, or only starts them
  lazily. Starting lazily without reaping means a long-lived daemon eventually
  holds all three anyway.
- A gateway re-namespaces tools again (`mcp__plugin_browser-lab_playwright__*` →
  whatever the gateway exposes). One more reason skills must detect by
  capability, never by tool name.

---

## 2026-08-19 — Root cause found: API keys never reach Claude Code

`EXA_API_KEY`, `TAVILY_API_KEY`, `BRIGHTDATA_API_TOKEN`, `APIFY_TOKEN` and
`FIRECRAWL_API_KEY` are all exported in `~/.zshrc:22-26` and are visible to an
interactive shell — but **Claude Code never sees them**. The desktop app launches
from the GUI, which does not read `.zshrc`, so `${EXA_API_KEY}` in `.mcp.json`
interpolates to empty and the server 401s.

Confirmed live: exa and tavily both returned 401 during the 2026-08-18 research,
which fell back to keyless Firecrawl and WebSearch.

**Decision (Alex, 2026-08-19):** keys move to `env` in `~/.claude/settings.json`,
which Claude Code reads regardless of how it was started.

**Consequence:** `setup-keys.sh` is fixing the wrong layer — it writes
`~/.browser-lab-keys.env` and sources it from the shell profile, the same dead
end. (Neither the file nor the source line currently exists.) Delete it and
rewrite `validate-keys.sh` against the new source.

**Rule for new backends:** never rely on the ambient shell environment. Either
`env` in settings.json, or a connector added with `claude mcp add` where the key
lives in Claude's connector store.

---

## 2026-08-18 — Transport is the lever, not granularity

From the gateway survey (`specs/2026-08-18-mcp-dynamic-loading-prior-art.md`):

- **Context is already solved natively.** MCP Tool Search defers tool schemas by
  default (~85% reduction). Most gateways on GitHub predate it and rebuild it.
  Don't build for this problem.
- **Memory is nobody's solved problem.** `stdio` servers start with the session
  regardless of use. Only transport, scope, or a lifecycle-owning gateway helps.
- **`mcp-remote` is an anti-pattern.** It is a stdio shim over an HTTP endpoint —
  two processes per session for zero benefit. This setup's `inkeepMcp` used it
  until 2026-08-18; now `{"type":"http"}` direct.
- **Prior art worth reading before building:**
  [MarimerLLC/mcp-aggregator](https://github.com/MarimerLLC/mcp-aggregator) —
  upstreams connect on first use, idle connections reaped, runtime registration.
  The clearest statement of the lifecycle we want.
- **The cautionary tale:** [AIRIS MCP Gateway](https://github.com/agiletec-inc/airis-mcp-gateway)
  is catalogued as a 60+-tool Docker multiplexer with HOT/COLD lifecycle. Its
  current README argues the opposite — don't register the gateway globally; have
  a skill open a short-lived session only when a backend is genuinely needed.
  They built the ambitious version and retreated. Read it before building ours.

**Namespacing, borrowed the hard way** ([ruflo#2685](https://github.com/ruvnet/ruflo/issues/2685)):
a plugin's bundled MCP server is namespaced on the marketplace path —
`mcp__<server>__*` becomes `mcp__plugin_<plugin>_<server>__*`. Skills hard-coding
bare names break on install. Confirmed here: exa resolves as
`mcp__plugin_browser-lab_exa__web_search_exa`, and it will change again when the
server moves to the `web-harvest` plugin. **Detect by capability, always.**

**Worth evaluating, not yet used:**
[McPick](https://scottspence.com/posts/mcpick-manage-mcp-servers-and-plugins-in-claude-code)
(`npx mcpick enable/disable`, runnable by Claude itself) — toggling config is a
cheaper answer than a gateway when the goal is merely "not all of them at once".
`claude plugin details <name>` already reports projected token cost per plugin;
there is no equivalent for memory, so measure that with `ps`.
