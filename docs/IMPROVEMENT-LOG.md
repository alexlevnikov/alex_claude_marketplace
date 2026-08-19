# Improvement Log

Running log of how to make this marketplace better: what to change, what to
borrow from other projects, and which questions are still open. Newest entries
on top. Companion docs: `ARCHITECTURE.md` (how it works), `AUTHORING.md` (how to
build), `specs/` (dated design decisions).

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
