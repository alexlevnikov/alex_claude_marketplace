# Marketplace Architecture

How this marketplace is put together, and — more importantly — **what each part
costs at runtime**. Read this before adding a plugin; the cost model is the part
that is easy to get wrong and expensive to undo.

**Repo:** `alex_claude_marketplace` · working copy at
`~/Library/Mobile Documents/.../alex.levnikov.root/claude_plugins/`
(the copy under `~/.claude/plugins/marketplaces/` is a read-only clone Claude
Code manages — never edit it; edit here and push).

---

## 1. The shape

```
claude_plugins/                       ← marketplace root (git repo)
├── .claude-plugin/
│   └── marketplace.json              ← the index: every plugin listed here
├── <plugin>/
│   ├── .claude-plugin/
│   │   └── plugin.json               ← this plugin's manifest
│   ├── .mcp.json                     ← OPTIONAL — MCP servers this plugin ships
│   ├── skills/
│   │   └── <skill>/
│   │       ├── SKILL.md              ← router: frontmatter + decision guide
│   │       └── references/*.md       ← detail, loaded only on demand
│   ├── agents/                       ← OPTIONAL — subagent definitions
│   └── README.md
├── build.sh                          ← shared: package a plugin → .plugin
├── doctor.sh                         ← shared: environment check
├── validate-keys.sh                  ← shared: key source + live key check
└── docs/
    ├── ARCHITECTURE.md               ← this file
    ├── AUTHORING.md                  ← how to build one
    └── specs/                        ← design decisions, dated
```

Tooling is shared, one copy at the root — three plugins do not need three copies
of the same script.

A plugin listed in `marketplace.json` becomes installable; a plugin **enabled**
in settings has its skills registered and its MCP servers started.

---

## 2. The three layers, and what each one costs

A plugin is up to three independent things. They have completely different
runtime costs, and conflating them is the root of most bloat.

| Layer | What it is | Cost when enabled but unused |
| --- | --- | --- |
| **Skills** | `SKILL.md` routers + `references/` | ~1 line of context (name + description) |
| **Agents** | subagent definitions | nothing until dispatched |
| **MCP servers** | `.mcp.json` entries | **depends entirely on transport — see below** |

### The MCP cost model — the thing that actually matters

MCP servers start **when the session starts**, not when a tool is first called.
There is no lazy start for `stdio`. So:

| Transport | Local process | Cost per session |
| --- | --- | --- |
| `http` / `sse` | none | **0** |
| `stdio` | one (often two: `npm exec` wrapper + the server) | **~45–80 MB** |

Multiply `stdio` by the number of concurrent sessions. On an 8 GB machine with
8 sessions open, four bundled `stdio` servers cost ~1.5–2.5 GB of resident
memory whether or not a single tool is ever called.

**Three rules follow directly:**

1. **Prefer `http` whenever the vendor offers an endpoint.** It is free.
2. **Never wrap an HTTP endpoint in `mcp-remote`.** `mcp-remote` is a `stdio`
   shim around an HTTP server — it converts a free connector into two processes
   per session for zero benefit. Claude Code speaks HTTP natively:
   `claude mcp add --transport http <name> <url>`.
   *(This repo's own `inkeepMcp` was configured this way until 2026-08-18.)*
3. **Bundle `stdio` servers only when they are the plugin's reason to exist**,
   and keep that plugin narrowly scoped so it is enabled only where needed.

### Two budgets, and only one of them is instrumented

Tokens and memory are separate budgets, and it is easy to mistake a report on one
for a report on the other.

`claude plugin details <plugin>` measures **tokens**: `always-on` (in every
session) versus `on-invoke` (when a skill fires). It lists MCP servers but marks
their schemas "resolved at runtime; not counted" — because ToolSearch fetches
them on demand. That is genuinely cheap, and it is the problem the router-skill
pattern solves.

It says nothing about **memory**. A plugin can read as ~200 always-on tokens and
still hold half a gigabyte across your open sessions, because its `stdio` servers
started when those sessions did. Nothing in the tooling surfaces that number —
measure it directly:

```bash
ps -Ao rss=,command= | grep -Ei "mcp|npm exec" | grep -v grep | awk '{s+=$1} END {printf "%.0f MB across %d processes\n", s/1024, NR}'
```

Skills are cheap; MCP servers are not. The general answer would be "enable a
skills-only plugin globally, and a `stdio`-bundling one per project" — but this
marketplace has rejected per-project scoping, which changes the answer. See §4.

---

## 3. Connector models — A (bundle) vs B (reference)

Decided in `specs/2026-08-12-plugin-marketplace-structure-design.md` (D4/D5).

**Model A — bundle.** The plugin ships `.mcp.json`; servers start automatically
when the plugin is enabled. Use for **keyless local** servers that the plugin
cannot function without (`playwright`, `chrome-devtools`, `mitmproxy`).

- Pro: works immediately, no setup step, no secrets in the repo.
- Con: pays the `stdio` cost in every session where the plugin is enabled.

**Model B — reference.** The plugin ships **no `.mcp.json`**. The skill routes
*by capability*: it detects which connectors are present and uses those. The
user adds connectors themselves (`claude mcp add`, or the Customize UI), and the
keys live in Claude's connector store.

- Pro: zero runtime cost; no secrets in an iCloud-synced folder; the user
  controls which backends exist.
- Con: the plugin does nothing until connectors are added — it ships the routing
  *intelligence*, the user supplies the muscle.
- **Requirement (D5):** never block. If a needed connector is missing, say
  exactly how to add it and continue with whatever is available.
- **Requirement:** never hard-code exact tool names — a user-added connector may
  be namespaced differently. Detect by capability.

**Choosing:** the axis that matters is **transport**, not keys.

- `http` backends → **A**, always. They hold no process, so bundling them is
  free, and bundling means they work the moment the plugin is enabled instead of
  waiting on a manual `claude mcp add`. Keys are not a reason to choose B; they
  live in `~/.claude/settings.json` → `env` and interpolate into the bundled
  `.mcp.json`. This is why `web-harvest` ships Model A with five keyed backends.
- `stdio` backends → **A** when the plugin cannot function without them
  (`browser-lab`), and then keep that plugin narrow, because every session pays.
- **B** stays right for genuinely optional or user-supplied backends, where the
  plugin ships routing intelligence and the user supplies the muscle.

---

## 4. Scope — where "dynamic loading" actually lives

There is no runtime mechanism to start an MCP server on demand. The real control
is **where a plugin is enabled**, and it has three levels:

| Level | File | Applies to |
| --- | --- | --- |
| user | `~/.claude/settings.json` → `enabledPlugins` | every project |
| project | `<repo>/.claude/settings.json` → `enabledPlugins` | that repo, shared via git |
| local | `<repo>/.claude/settings.local.json` | that repo, not committed |

MCP servers have the same three scopes via `claude mcp add -s user|project|local`;
`-s project` writes a `.mcp.json` into the repo.

**The design consequence:** splitting one fat plugin into several thin ones buys
nothing on its own — if all the pieces stay enabled at user level, the same
servers still start. Granularity is a *multiplier* on scope, not a substitute for
it. Split **and** demote to project scope, or don't bother splitting.

### Where this marketplace deliberately departs from that

The rule above is the general one. **This setup rejects it** (Alex, 2026-08-19):
plugins install at **user** scope, and servers must start when used. Per-project
enabling is not an acceptable answer here — it makes availability depend on which
directory a session happens to sit in.

That is a strictly harder requirement, and it splits by transport:

- **HTTP backends satisfy it for free.** No process is held; the connection
  happens on the first call. This is why `web-harvest` can sit at user scope
  costing nothing.
- **stdio backends cannot satisfy it at all** without a gateway, because Claude
  Code starts them with the session. `browser-lab`'s three servers are stdio-only
  with no hosted variant, so it currently pays 3 processes per session at user
  scope — accepted deliberately, pending the wave-2 gateway.

So: **prefer HTTP; where a backend is stdio-only, a gateway is the only way to
keep user scope honest.** See `IMPROVEMENT-LOG.md` for that decision's status.

---

## 5. The router-skill pattern

Every plugin here is an **orchestrator**, not a tool dump. The pattern:

1. **One router skill per domain.** Its `description` frontmatter carries the
   full trigger vocabulary — the phrases a user would actually type. This is the
   only part always in context, so it must be specific enough to fire reliably
   and bounded enough not to fire on everything.
2. **An ownership table.** For each job, exactly one backend owns it, with the
   reason. When two backends could do a thing, the table decides — this is what
   stops the model from loading two competing toolsets for one step.
3. **A routing decision guide.** Classify first, then act. Name the route before
   running it.
4. **Explicit hand-offs to sibling skills.** `browser-lab` ⇄ `web-harvest` name
   each other in both directions, so the wrong entry point self-corrects instead
   of muddling through.
5. **`references/*.md` for the detail.** Progressive disclosure: `SKILL.md` stays
   a map, references carry the procedures and are read only when that route is
   taken.

This is what makes "give the task to the skill and let it pick the tools" work —
the routing lives in the skill, not in the user's head.

**What the pattern does and does not solve.** It solves *context*: one router
description instead of N tool-schema dumps, with ToolSearch fetching schemas on
demand. It does **not** solve *memory* — see §2. Those are separate problems with
separate fixes, and a good router does nothing for the second one.

---

## 6. Current inventory

| Plugin | Skills | MCP shipped | Model | Cost per session | Notes |
| --- | --- | --- | --- | --- | --- |
| `browser-lab` 0.3.1 | `browser-lab` | 3 `stdio`: playwright, chrome-devtools, mitmproxy | A | **3 processes** | Keyless and local. All three are stdio-only with no hosted variant, so user scope costs 3 processes per open session — **accepted permanently**: the gateway that would have removed it was designed and declined (`specs/2026-08-19-mcp-gateway-design.md`). `chrome-devtools` runs with `--autoConnect` and needs remote debugging enabled once in Chrome. |
| `web-harvest` 0.1.0 | `web-harvest` | 5 `http`: firecrawl, exa, tavily, brightdata, apify | A | **0 processes** | Keys in `~/.claude/settings.json` → `env`. Connects on first call; free to leave enabled at user scope. |
| `agents-os` 0.1.0 | `hetzner-server` | none | — | 0 | Pure knowledge. Free to enable anywhere. |

Split on 2026-08-19 per `specs/2026-08-19-web-harvest-split-design.md` (wave 1).
Shared tooling lives at the repo root: `build.sh` (package a plugin),
`doctor.sh` (environment check), `validate-keys.sh` (prove key source + key).

### Where the keys live

`env` in `~/.claude/settings.json`, which Claude Code reads however it was
launched. **Not** a shell profile: the desktop app starts from the GUI and never
sources `.zshrc`, so `${EXA_API_KEY}` in a `.mcp.json` interpolates to empty and
the backend answers 401 — the bug that motivated wave 1. Any new keyed backend
follows the same rule, or uses a connector added with `claude mcp add` where the
key lives in Claude's connector store.

