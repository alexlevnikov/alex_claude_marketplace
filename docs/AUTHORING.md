# Authoring Guide

How to add a plugin, a skill, or an MCP server to this marketplace.
Read `ARCHITECTURE.md` first — especially the cost model in §2. This guide is
the procedure; that one is the reasoning.

**Always edit the working copy:**
`~/Library/Mobile Documents/.../alex.levnikov.root/claude_plugins/`
Never edit `~/.claude/plugins/marketplaces/alex-claude-marketplace/` — Claude Code
overwrites it on update.

---

## Decide first: is this a plugin, or a skill in an existing plugin?

**A new skill in an existing plugin** when it shares that plugin's backends and
its trigger vocabulary sits next to the existing ones. `web-harvest` living
inside `browser-lab` is this case — both route web work, and they hand off to
each other.

**A new plugin** when *any* of:
- it needs MCP servers the existing plugins don't ship;
- you want to enable it in some projects and not others;
- its domain has nothing to do with the existing ones.

Scope is the deciding factor more often than subject matter. **If two skills
would always be enabled together, they belong in one plugin.** If you would ever
want one without the other, split them — that is the only way to pay for one
without the other.

---

## Add a new plugin

### 1. Scaffold

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins
mkdir -p <plugin>/.claude-plugin <plugin>/skills/<skill>/references
```

### 2. `<plugin>/.claude-plugin/plugin.json`

```json
{
  "name": "<plugin>",
  "version": "0.1.0",
  "description": "What it does and which backends it routes across.",
  "author": { "name": "Alex Levnikov" },
  "keywords": ["...", "..."],
  "license": "MIT"
}
```

`name` must match the directory name.

### 3. Register it in `.claude-plugin/marketplace.json`

Append to `plugins[]`:

```json
{
  "name": "<plugin>",
  "source": "./<plugin>",
  "description": "One sentence — this is what shows in the plugin list.",
  "version": "0.1.0",
  "author": { "name": "Alex Levnikov" },
  "keywords": ["...", "..."]
}
```

Keep `version` here in sync with `plugin.json`. Bump both together.

### 4. Write the router skill (below), then install and verify (§Install).

---

## Write a skill

`<plugin>/skills/<skill>/SKILL.md`:

```markdown
---
name: <skill>
description: >
  Use this skill when ... Triggers on: "<phrase>", "<phrase>", "<phrase>".
  It routes across <backends> and <what it decides>. For <adjacent job>, use
  the sibling `<other-skill>` skill instead.
metadata:
  version: "0.1.0"
---

# <Title>

<One paragraph: the single job this skill owns.>

## What each backend owns

| Job | Backend | Why |
| --- | --- | --- |

## Routing decision guide

- **"<user phrasing>"** → <backend>. See `references/<file>.md`.

## Scope: what this skill hands off

| The task is really about… | Owner |
| --- | --- |
```

### The description is the whole trigger mechanism

It is the only part of the skill always in context. Everything else loads after
it fires. So:

- **Write the phrases the user would actually type**, in their words, in quotes.
  `"why is this page slow"` beats "performance analysis".
- **State the boundary explicitly** — name the sibling skill that owns the
  adjacent job, in both skills. A router that doesn't say what it *isn't* fires
  on everything and becomes noise.
- **Be specific enough to fire and bounded enough not to over-fire.** Both
  failure modes are real; over-firing is the one you notice later.

### Keep `SKILL.md` a map

Put procedures, examples, and API detail in `references/*.md` and link them from
the routing guide. `SKILL.md` should be readable end-to-end in under a minute —
it exists to pick a route, not to execute one.

---

## Add an MCP server

**Before anything else, check the vendor's transport.** This one decision
dominates the plugin's runtime cost (`ARCHITECTURE.md` §2).

### If the vendor has an HTTP endpoint → it is free. Use it.

In a bundled `.mcp.json`:

```json
{ "mcpServers": {
  "<name>": { "type": "http", "url": "https://..." }
} }
```

Or, for a user-added connector (Model B), document this in the plugin README:

```bash
claude mcp add --transport http <name> https://... --header "Authorization: Bearer <key>"
```

Verify an endpoint really speaks HTTP before wiring it up:

```bash
curl -s -o /dev/null -w "%{http_code}\n" --max-time 20 -X POST "<url>" -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
```

`200` with a JSON-RPC `result` means native HTTP works — **do not use `mcp-remote`.**

### If it is genuinely stdio-only → bundle it only if the plugin needs it to exist

```json
{ "mcpServers": {
  "<name>": { "command": "npx", "args": ["-y", "<package>"] }
} }
```

Then treat the plugin as project-scoped by default (`ARCHITECTURE.md` §4).
`${CLAUDE_PLUGIN_ROOT}` resolves to the plugin directory if the server ships
inside the plugin.

### Never put secrets in this repo

It is iCloud-synced and pushed to GitHub. Keys belong in Claude's connector store
(entered at `claude mcp add` time) or in `~/.claude/settings.json` `env`.
`${VAR}` interpolation in a bundled `.mcp.json` only works if the variable is
actually defined outside the repo — an unset `${VAR}` yields silent 401s, which
is exactly the failure Model B was introduced to avoid.

---

## Install and verify

```bash
claude plugin marketplace add ~/Library/Mobile\ Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins
```

Once only. Afterwards, pull in your own changes with:

```bash
claude plugin marketplace update alex-claude-marketplace
```

### Enable at the right scope — this is the memory decision

```bash
claude plugin enable <plugin>@alex-claude-marketplace -s project
```

`-s` takes `user` (everywhere), `project` (this repo, committed), or `local`
(this repo, private). **Default to `project` for anything bundling `stdio`
servers**; reserve `user` for skills-only plugins. `claude plugin disable` takes
the same flag.

### Check what it costs before you commit to it

```bash
claude plugin details <plugin>
```

This prints the component inventory and the **projected token cost** —
`always-on` (paid in every session) versus `on-invoke` (paid when a skill fires).
`browser-lab`, for reference, is ~451 always-on tokens for two routers.

**Read the MCP line carefully.** It lists the servers and notes that tool schemas
are *resolved at runtime and not counted*. That is a statement about **tokens**,
not about memory — the `stdio` servers among them still start with the session
and still hold RAM. `plugin details` has no view of that. Measure it yourself:

```bash
ps -Ao rss=,command= | grep -Ei "mcp|npm exec" | grep -v grep | awk '{s+=$1} END {printf "%.0f MB across %d processes\n", s/1024, NR}'
```

Run it before and after enabling, in a fresh session. If a plugin you believed
was skills-only adds processes, something bundled an `.mcp.json` you didn't
intend.

### Confirm the router actually fires

In a fresh session, try the phrases from the `description` verbatim — not a
paraphrase you invented, which is the most common way a broken trigger looks
fine in testing. For repeatable checks, `claude plugin eval` runs scored cases
from `evals/**/case.yaml` against the plugin, including a no-plugin baseline arm.

## Pre-commit checklist

- [ ] `plugin.json` `name` matches the directory name
- [ ] Registered in `marketplace.json`, versions in sync
- [ ] Every `SKILL.md` has `name` + `description` frontmatter
- [ ] Sibling skills name each other in both directions
- [ ] Every new MCP server: HTTP if the vendor offers it; no `mcp-remote` shims
- [ ] No API keys, tokens, or `.env` anywhere in the repo
- [ ] `references/` carries the detail; `SKILL.md` stays a map
- [ ] JSON parses:
      `for f in $(find . -name "*.json" -not -path "./.git/*"); do python3 -c "import json;json.load(open('$f'))" || echo "BAD $f"; done`

---

## Periodic hygiene

Roughly monthly, or whenever the machine feels slow:

**Find duplicate MCP declarations** — the same server shipped by two plugins is
the most common regression (e.g. `chrome-devtools` from both `browser-lab` and
the official `chrome-devtools-mcp` plugin, running `@latest` and `@1.5.0` side
by side):

```bash
cd ~/.claude/plugins/cache && find . -maxdepth 4 -name ".mcp.json" -exec python3 -c "import json,sys;d=json.load(open(sys.argv[1]));[print(k,'←',sys.argv[1]) for k in d.get('mcpServers',{})]" {} \; | sort
```

**Find stdio servers that could be HTTP** — check each `command`-based entry
against its vendor's current docs; several have shipped HTTP endpoints since.

**Audit what is enabled at user level** — anything bundling `stdio` that you
don't use in *most* projects should be demoted to project scope:

```bash
python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.claude/settings.json')));[print(('ON ' if v else 'off'),k) for k,v in sorted(d.get('enabledPlugins',{}).items())]"
```
