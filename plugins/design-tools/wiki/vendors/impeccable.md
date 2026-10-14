# Impeccable — pbakaus

**Upstream:** https://github.com/pbakaus/impeccable
**Bundled:** one `impeccable` skill at v4.5.2, its references, and its skill scripts. See [pinned revision](../../vendors/LOCK.json) and [Apache-2.0 attribution](../../third-party/README.md).

Impeccable has internal design, audit, polish, live, and generation modes. They are modes of one skill, rather than separate entries in this library. Give it its own context for large art-direction work.

Its current entrypoint asks the agent to run `<dir>/scripts/impeccable context`, where `<dir>` is the bundled skill directory returned by the resolver. The launcher can download a binary on first use; this runtime dependency is not packaged as part of `design-tools`. Follow the skill's own current instructions for subsequent modes and checks.

The earlier design-studio cost and quality comparison used v4.0.4. It does not establish v4.5.2's behavior.

## Invoke

- Claude Code: `/design-tools:impeccable <mode> <target>` or `/design-tools:impeccable:impeccable <mode> <target>`.
- Codex: `$design-tools:design-tools impeccable <mode> <target>`.
