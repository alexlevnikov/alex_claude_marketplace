# Hermes Agent Architect

The [skill](skills/hermes-agent-architect/SKILL.md) contains the complete
architecture workspace: routing guidance, documentation catalog, deep research,
scripts and the pinned Hermes source submodule. The skill folder is also the
separate Codex project folder on the VPS.

This pack starts no MCP server and deploys no bot. It is installed locally on
the VPS through a symlink to the marketplace checkout, so knowledge edits in
that checkout are visible at the next read. A published plugin cache may lag
until its own update and may need the Git submodule initialized in a checkout;
the official linked source is the fallback.
