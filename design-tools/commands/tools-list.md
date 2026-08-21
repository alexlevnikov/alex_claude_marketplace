---
description: Show the design tool catalog and the set's health without running anything
argument-hint: "[look|feel|fix|judge|lookup|all|set|vendors]"
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh":*), Read
---

Show the `design-tools` catalog for: **$ARGUMENTS** (default: all routable groups).

- A group name or `all` → read `references/catalog.md` and print the matching groups as a table:
  tool · vendor · writes or reports · what it is for · when not to reach for it. Add the relevant
  entries from `references/collisions.md` for any group that contains a contested tool.
- `set` → the whole set, including the tools the router never lands on (orchestrators, phases,
  techniques): print `wiki/README.md` § *Tools by group*, then run
  `bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh" --all` and report what is resolvable right now
  and from where — project scope, user scope, or the design-studio root.
- `vendors` → `wiki/README.md` § *Vendors*, one line each, with the link to `wiki/vendors/<vendor>.md`.

Every tool listed has a direct command, `/design-tools:<vendor>-<tool>`, and a page, `wiki/tools/<tool>.md`;
every vendor has an entry command, `/design-tools:<vendor>` (master skill as designed, or the hub).

Change nothing. This command answers "what have I got", not "do something".
