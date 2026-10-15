# Hermes Agent Architect

The [architect skill](skills/hermes-agent-architect/SKILL.md) remains the primary component and research library: [component cards](skills/hermes-agent-architect/references/components/index.md), [architecture decisions](skills/hermes-agent-architect/references/decisions/), [bot patterns](skills/hermes-agent-architect/references/patterns/), [full platform overview](skills/hermes-agent-architect/docs/hermes-platform-overview.md), memory research and an official documentation catalog. Focused sibling skills turn that library into bot blueprints, extension designs and runtime audits.

The clean Hermes `v2026.9.14` submodule is pinned at `upstream/hermes-agent`, outside `skills/`, to avoid discovering upstream skills as this plugin's skills. Initialize it after cloning with `git submodule update --init -- plugins/hermes-agent-architect/upstream/hermes-agent` from the marketplace root.

This plugin starts no MCP server and deploys no bot. A local Codex symlink to the marketplace checkout sees knowledge edits on the next read; published plugin caches need their own update. Host maps, credentials, profiles, sessions and personal memory stay in private sources.
