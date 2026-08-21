---
description: Route a design request to exactly one specialist skill, load it, and run it
argument-hint: "<what you want, in your own words> [file or path]"
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh":*), Bash(find:*), Read
---

Use the `design-tools` skill to route: **$ARGUMENTS**

1. Resolve `BRAND-CONTRACT.md` (working directory, then parents) before any write pass.
2. Find the route in `references/routing.md`. If it lands on accessibility, performance, motion,
   polish or review, check `references/collisions.md` before calling.
3. **Say the route out loud** — the tool, the vendor, and the one-sentence reason — before loading it.
4. **Load it** (`references/loading.md`): run
   `bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh" <tool>` and read the manifest.
   `load: skill` → invoke by name with the Skill tool. `load: read` → Read the `skill:` file (and
   `base:` first for a ui-craft lens) and follow it as if invoked. `status: MISSING` → stop, say where
   it looked, do not improvise. If `${CLAUDE_PLUGIN_ROOT}` did not substitute, locate the resolver:
   `find ~/.claude/plugins "$HOME/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins" -path '*design-tools/scripts/resolve.sh'`.
5. Run it. Read-only tools first on code you have not seen this session.
6. Report what changed, one line per file.

If the request needs more than two write-tools, or asks for a new look rather than a fix, stop and
offer `design-pipeline` instead. If the request is "make it better" with no aspect named, ask which
aspect is wrong — do not guess. If the user named a tool outright, there is nothing to route:
`/design-tools:<tool>` does the same resolve-and-load for that one tool.
