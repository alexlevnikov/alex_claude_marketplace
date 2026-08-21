# Wave 2: one HTTP gateway per machine

**Date:** 2026-08-19
**Status:** **DECLINED 2026-08-19. Not implemented, and not scheduled.** The
design below is sound and the measurements are real; the decision is that the
price is wrong for what it buys. Kept in full because the next person to feel
this pain should start from the analysis, not from zero. See "Why this was
declined" immediately below.
**Superseded by:** nothing. The problem it addresses is accepted, not solved.

## Why this was declined

The gateway removes a **cost**, not a defect. Only one thing was actually broken
— `chrome-devtools` failing in every session but the one that won the Chrome
profile race — and that is fixed far more cheaply by `--autoConnect`, shipped in
`browser-lab` 0.3.1. Everything else in the plugin worked throughout.

What the gateway would have cost, once the candidates were read rather than
trusted:

- A **Rust toolchain** (~1.4 GB) on a machine where nothing else needs one:
  Rai-onl publishes no binaries, its v0.3.0 release carries zero assets.
- Building a **thirteen-crate project** with OIDC auth, TLS and a credential
  store to do one small job — put three local servers behind a loopback HTTP
  port.
- A **third-party daemon in the path of all MCP traffic**, including the
  telegram token and n8n credentials carried over ssh.

Against roughly 300 MB on an 8 GB machine. Real money, but not at that price,
and not with that blast radius.

**Revisit when**, and only when, memory pressure again blocks work — the
symptom recorded in `CLAUDE.md` is scheduled-task spawns dying silently. Then
start here: the candidate is chosen, the two decisive properties are settled
from source, and the acceptance criteria are written.

---

**Original status (superseded):** Design — approved by Alex 2026-08-19. Not
implemented; phase 0 (the stand) gates everything else.
**Follows:** `2026-08-19-web-harvest-split-design.md`, which closed the retrieval
side and left this open.
**Prior art:** `2026-08-18-mcp-dynamic-loading-prior-art.md` — read it first. Its
conclusion ("we don't need a gateway yet") was correct for the requirement it
answered and is superseded by the measurements below, not by a change of mind.

## Problem

`stdio` MCP servers start with the session and live as long as it does. That cost
is multiplied by the number of open sessions, and this machine keeps many open.

Measured 2026-08-19 on 8 live sessions (all 8 parent processes confirmed alive;
this is not a leak of orphans, it is the steady state):

| Server | Processes | RSS | Owner |
| --- | --- | --- | --- |
| chrome-devtools | 46 | **207 MB** | browser-lab |
| playwright | 31 | **137 MB** | browser-lab |
| mitmproxy | 16 | 11 MB | browser-lab |
| firecrawl-mcp | 24 | **90 MB** | `firecrawl@claude-plugins-official` |
| mcp-remote (inkeep) | 8 | 62 MB | leftover; config is already `type: http` |
| @brightdata/mcp | 14 | 30 MB | leftover; pre-restart sessions on browser-lab 0.2.0 |
| episodic-memory | 16 | 58 MB | third-party plugin |
| superpowers-chrome | 8 | 27 MB | third-party plugin |
| telegram, n8n | 7 | 22 MB | plugin / user scope |
| **Total stdio** | **170** | **643 MB** | |

Whole session trees come to 1658 MB across the 8 sessions. The machine has 8 GB,
and `CLAUDE.md` already records the consequence: scheduled-task spawns die
silently under memory pressure, with `[CliGovernor] memory pressure` in the log.

**It is also a functional defect, not only a cost.** `chrome-devtools` fails
outright in every session but one:

```
The browser is already running for /Users/…/.cache/chrome-devtools-mcp/chrome-profile.
Use --isolated to run multiple browser instances.
```

Eight instances contend for one profile directory; the first to launch Chrome
wins and the other seven are dead for the whole session. Reproduced live in this
session, which is not the winner.

Two duplicates surfaced while measuring, and they are separate from the gateway:

- **`firecrawl-mcp` runs locally in every session** and duplicates the hosted
  Firecrawl that `web-harvest` already serves over HTTP for zero processes.
- **`mcp-remote` processes for inkeep persist** although the config moved to
  `type: http` on 2026-08-18. Old sessions still hold the shim.

Counts above include the four sessions opened before the wave-1 restart, which
still run `browser-lab` 0.2.0 and therefore carry a second `chrome-devtools@1.5.0`
and a second playwright. Sessions started after the restart carry one of each, so
that particular duplication is historical, not a live defect.

## Requirements (Alex, 2026-08-19)

1. **Scope: every `stdio` server on the machine**, third-party plugins included —
   not only the servers `browser-lab` owns.
2. **Concurrency: one Chrome, separate tabs.** One persistent profile shared by
   all sessions; each session addresses its own tab. Rejected explicitly:
   `--isolated`, because a temporary profile discards logins, and Alex wants
   logins preserved.
3. **Adopt, don't build** — take a ready transparent bridge, prove it on a stand
   first, and write our own only if both candidates fail the criteria.
4. Standing requirement from 2026-08-19: user-level install, servers start when
   used. Per-project scoping stays off the table.

## Why meta-routers are excluded

The field splits in two, and only one half is compatible with this setup.

**Meta-routers** collapse every backend tool into a search-and-invoke pair:
`mcpproxy-go` (`retrieve_tools` — 40 occurrences in its README, zero for
namespacing), `MikkoParkkola/mcp-gateway` (`gateway_search_tools` +
`gateway_invoke`, "~15 tools instead of ~150"), `MarimerLLC/mcp-aggregator`
(`list_services` / `get_service_details` / `invoke_tool`). They sell this as
context savings.

**We already have those savings for free.** MCP Tool Search defers tool schemas
natively and is on by default — visible in every session here. Adopting a
meta-router would buy a benefit we already hold, and pay for it with indirection
on every call and the loss of native tool schemas.

`mcp-aggregator` is otherwise the closest match to the lifecycle we want
(connect on first use, `ConnectionIdleTimeout` 30 min) and is worth re-reading if
the transparent bridges fail.

**Transparent bridges** keep each backend as its own HTTP endpoint with its own
native tools, which is the only shape compatible with the rule in `AUTHORING.md`
that skills detect a capability and never hard-code a tool name:

| Candidate | Evidence | Unknown |
| --- | --- | --- |
| [Rai-onl/mcp-gateway](https://github.com/rai-onl/mcp-gateway) | One binary, one config. Spawns the stdio child, performs the MCP handshake, restarts a crashed child on the next request. Per-server `request_timeout_seconds` (default 30 s). `SIGHUP` reloads config in place. | Lazy start on first call; idle reaping |
| [common-creation/mcp-gateway](https://github.com/common-creation/mcp-gateway) | "Auto-start MCP servers on first request". Streamable HTTP, per-server path `/v1/proxy/{server-name}`, `POST /api/servers/{name}/start\|stop`, web UI. | Idle reaping; maturity |

### Resolved from source, 2026-08-19

Both repositories were cloned and read rather than trusted. **Rai-onl wins on
every property that motivated this wave**, and `common-creation` is out.

| Property | Rai-onl (Rust) | common-creation (Go) |
| --- | --- | --- |
| Lazy start | **Yes** — `router/src/dispatch.rs` holds each bridge as an empty slot and a *request* spawns it; the slot lock is held "across the handshake" | **No** — `main.go:41` calls `manager.StartAll(ctx)` at startup. The lazy path exists (`ensureSession`, `streamable.go:113`) but is not the default |
| Crash / wedge recovery | **Yes** — background probe reaps a dead child and replaces one that fails the liveness probe repeatedly (`dispatch.rs:231`) | None |
| Idle reaping | No | No |
| Maintained | v0.3.0, 2026-07-27, recent commits | Last commit 2026-01-10 |
| Build | `cargo build` — **needs a Rust toolchain, absent on this machine** | Go / Docker, both present |

Two corrections to earlier reasoning, both recorded so they are not re-derived:

- **`common-creation`'s README overclaims.** "Auto-start MCP servers on first
  request" is contradicted by its own `main.go`. The README was the basis for
  putting it on the shortlist; the source removes it.
- **Criterion 3 was overweighted.** With one daemon the worst case is three
  browser-lab processes for the whole machine, against 21 today (7 sessions × 3).
  Idle reaping would buy "zero instead of three", not "three instead of 21". Its
  absence is therefore acceptable, and it drops from blocking to nice-to-have.

**Decision: Rai-onl/mcp-gateway.** Its cost is a Rust toolchain on this machine,
which no other work here needs.

## Architecture

```
launchd  (RunAtLoad + KeepAlive)
  └── mcp-gateway — one process per machine, bound to 127.0.0.1 (loopback only)
        ├── chrome-devtools   ← exactly one instance on the machine
        ├── playwright
        ├── mitmproxy
        ├── episodic-memory
        ├── superpowers-chrome
        ├── telegram
        └── n8n (ssh)          each spawned on first call, reaped when idle

Claude Code, any session:  {"type": "http", "url": "http://127.0.0.1:PORT/…"}  → 0 processes
```

**The chrome-devtools defect is fixed by the architecture, not by a flag.** The
profile conflict exists because eight instances contend for one directory. With
exactly one instance on the machine there is nothing to contend with: it launches
Chrome against the persistent profile `~/.cache/chrome-devtools-mcp/chrome-profile`
and logins survive. No `--browserUrl`, no externally managed Chrome. Add
`--experimentalPageIdRouting`, documented as "useful for concurrent agent
sessions", so each session addresses its own tab by id.

Note what this trades away: one backend instance means one blast radius. A wedged
playwright now affects every session, where today it affects one. The per-server
timeout in Rai-onl and the crashed-child restart are what make that acceptable.

### Configuration, by side

- **`browser-lab/.mcp.json`** — its three servers become `type: http` entries
  pointing at the gateway. We own this file and it ships through the marketplace.
- **Third-party plugins** — their `.mcp.json` lives in another marketplace's
  cache and any edit is erased on update. Their servers must be suppressed and
  re-added as user-scope HTTP entries in `~/.claude.json`.

`disabledMcpjsonServers` is documented as "List of specific MCP servers from
`.mcp.json` files to reject". Whether that covers a server arriving from a plugin
is **not documented** and must be tested, not assumed — see criterion 8.

## Phase 0: the stand

Criteria 2 and 3 were settled from source (see above) and no longer need the
stand. What remains needs a running gateway. The stand uses **Rai-onl**, one
backend, before any config on this machine changes.

1. Claude Code connects over `"type": "http"` and tools arrive with **native
   schemas**, not meta-tools.
2. **Lazy start** — *settled from source*. Confirm in passing: the backend
   process is absent from `ps` before the first tool call and present after it.
3. **Idle reaping** — *settled: neither candidate has it*, and it is not worth
   blocking on. Confirm instead that a started backend stays a single instance
   machine-wide no matter how many sessions call it.
4. **Two concurrent sessions** against one backend do not corrupt each other;
   chrome-devtools with page-id routing keeps their tabs separate.
5. **Logins survive** a session restart — a cookie set in one session is present
   in the next.
6. Killing and restarting the daemon **does not require restarting** any Claude
   Code session.
7. Tool names stay per-backend and do not collide.
8. A third-party plugin's MCP server can be suppressed **while its skills and
   agents stay available**.

Baseline for comparison, measured 2026-08-19: **643 MB across 170 stdio
processes** on 8 sessions. Target: one daemon plus only what is in use.

**Criterion 8 is the only one whose failure changes scope.** If a plugin's server
cannot be suppressed independently of its skills, third-party plugins stay as they
are and the gateway covers only what we control — `browser-lab`'s three servers,
355 MB of the 643 MB.

## Rollout

**Phase 1 — `browser-lab` only.** We own the plugin and the file; nothing
third-party can break. This alone fixes the chrome-devtools defect and moves the
largest single block of memory. `browser-lab` gets a minor version bump, and its
skill keeps describing capabilities rather than tool names, so the re-namespacing
that the gateway causes changes nothing for the skill.

**Phase 2 — third-party servers**, gated on criterion 8. One server at a time,
verifying after each that the plugin's skills and agents still resolve.

**Not in this wave:** the two duplicates found while measuring. They are cheaper
and independent, and are logged separately in `IMPROVEMENT-LOG.md`.

## Failure modes

| Failure | Effect | Mitigation |
| --- | --- | --- |
| Daemon down | Every backend dead in every session | `KeepAlive` in launchd; a `doctor.sh` check that reports the daemon plainly; `type: http` fails visibly, not silently |
| Daemon wedged, port held | Sessions hang on call | Per-server `request_timeout_seconds`; criterion 6 proves recovery without touching sessions |
| Backend crashes | One capability lost machine-wide | Rai-onl restarts the child on the next request |
| Gateway upgrade | All sessions affected at once | Upgrade with no session open, or accept one failed call |
| Port already taken | Silent connect failure | Fixed port recorded here and asserted by `doctor.sh` |

**Rollback is one commit.** Phase 1 reverts by restoring the three `stdio` entries
in `browser-lab/.mcp.json` and updating the plugin; phase 2 by restoring each
plugin to `enabledPlugins` and dropping its HTTP entry. Nothing in the gateway
holds state that a session needs, so a rollback costs a restart and no data.

## Open questions

- ~~Which candidate survives phase 0~~ — **resolved 2026-08-19 from source:
  Rai-onl.** The fallback if it fails the stand is still a purpose-built bridge
  (~400 lines: config, one endpoint per backend, spawn on first call, launchd).
- Whether a Rust toolchain on this machine is an acceptable price. It is needed
  only to build the gateway; nothing else here uses Rust. Alex decides before
  the stand runs.
- Whether the gateway should reap Chrome itself, or only the chrome-devtools
  server. Reaping the browser discards the tab state sessions may still want.
- Whether `n8n-hetzner` belongs behind the gateway at all: it is an `ssh`
  process, cheap at 4 MB, and moving it buys little.
