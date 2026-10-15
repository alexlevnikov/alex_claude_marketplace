# Hermes Agent Architect

The [architect skill](skills/hermes-agent-architect/SKILL.md) remains the primary component and research library: [component cards](skills/hermes-agent-architect/references/components/index.md), [architecture decisions](skills/hermes-agent-architect/references/decisions/), [bot patterns](skills/hermes-agent-architect/references/patterns/), [full platform overview](skills/hermes-agent-architect/docs/hermes-platform-overview.md), memory research and an official documentation catalog. Focused sibling skills turn that library into bot blueprints, extension designs and runtime audits.

The clean Hermes `v2026.9.14` submodule is pinned at `upstream/hermes-agent`, outside `skills/`, to avoid discovering upstream skills as this plugin's skills. Initialize it after cloning with `git submodule update --init -- plugins/hermes-agent-architect/upstream/hermes-agent` from the marketplace root.

This plugin starts no MCP server and deploys no bot. A local Codex symlink to the marketplace checkout sees knowledge edits on the next read; published plugin caches need their own update. Host maps, credentials, profiles, sessions and personal memory stay in private sources.

## Deferred: pinned upstream in Codex plugin cache

Mac verification on 2026-10-15 found that Codex loads all four Hermes skills from plugin version `0.2.0`, but the installed plugin cache does not contain the `upstream/hermes-agent` submodule. The authored library and documentation catalog remain available there; a claim about the pinned `v2026.9.14` implementation still needs the exact tagged source from a checkout with that submodule initialized.

Revisit how the Mac should provide the pinned source for research: initialize it in a separate marketplace checkout or establish a supported plugin installation path that includes submodules. Check how the skill locates that source and avoid duplicate installed skills. Until then, report the missing local source instead of treating the catalog entry or current website as proof of tagged behavior.
