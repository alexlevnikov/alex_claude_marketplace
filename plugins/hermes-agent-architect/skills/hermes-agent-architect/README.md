# Hermes Agent Architect library

This folder is the primary Codex skill and research workspace for reusable Hermes bot architecture. It belongs to the `alex_claude_marketplace` Git repository and can be opened as a separate Codex project. On a machine where the installed skill is a symlink to this checkout, local edits become visible on the next skill read; other machines need a Git update.

## Library

- [Component index](references/components/index.md): reusable Hermes mechanisms and evidence.
- [Decision guide](references/decision-guide.md): choose a profile, skill, plugin, MCP, provider, adapter or core patch.
- [Decisions](references/decisions/): owner-approved or proposed architecture choices.
- [Patterns](references/patterns/): repeatable bot designs with validation and rollback.
- [Platform overview](docs/hermes-platform-overview.md): full feature map and customization routes.
- [Memory research](docs/hermes-memory-architecture.md) and [provider review](docs/hermes-memory-providers-review-2026-10-15.md).
- `data/docs-catalog.json`: index of 239 official URLs captured 2026-10-13, including matches to the pinned tag.

Use `python3 scripts/find_knowledge.py memory` to search the authored library and `python3 scripts/find_docs.py memory` to find official pages and pinned files. Run `python3 scripts/validate_knowledge.py` after updating records. The pinned source is a clean submodule at `../../upstream/hermes-agent`, tag `v2026.9.14`, commit `345cd2b057a452236de401d3534b8502a7465e8d`. In another clone initialize it from the marketplace root with `git submodule update --init -- plugins/hermes-agent-architect/upstream/hermes-agent`.

Rebuild the catalog from a reviewed official index snapshot using `python3 scripts/build_catalog.py --index-file <path> --upstream ../../upstream/hermes-agent --captured-at <UTC> --tag v2026.9.14`. A current URL or a file in the tag does not establish that a target bot enables the feature.

Bot source, live service maps, profiles, credentials, sessions and personal memory stay outside this public library.
