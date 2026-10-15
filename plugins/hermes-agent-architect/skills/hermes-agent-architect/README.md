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

Resolve script paths relative to this installed SKILL.md, not the shell working directory. Use `python3 scripts/find_knowledge.py memory` to search the authored library and `python3 scripts/find_docs.py memory --require-upstream` to find current official URLs and verified pinned local files. `python3 scripts/resolve_upstream.py --json` reports the selected root and revision; `--file website/docs/user-guide/features/memory.md` verifies and returns a specific file. Run `python3 scripts/validate_knowledge.py --require-upstream` to check knowledge and local source together. Without the flag, validation checks library structure even on machines without the optional upstream checkout.

The pin is `v2026.9.14`, commit `345cd2b057a452236de401d3534b8502a7465e8d`. The resolver uses `--upstream` or `HERMES_ARCHITECT_UPSTREAM` (an upstream root) as an explicit, authoritative override. Otherwise it tries the adjacent `../../upstream/hermes-agent`, then `~/.local/share/alex-claude-marketplace/plugins/hermes-agent-architect/upstream/hermes-agent`. Each candidate must be the Git root, at exactly the catalog commit, clean, and contain `website/docs`. An invalid explicit override fails instead of silently falling back. Missing files and modified bytes cannot be used as pinned evidence.

See the [plugin setup](../../README.md) for creating the external checkout outside iCloud. No extra skill links, environment setting or per-request path is needed at the standard location. The resolver only reads: it never clones, fetches, resets or updates a source. Exit code 2 means unavailable; say so and keep current-documentation claims separate from unverified pinned-source claims.

Rebuild the catalog from a reviewed official index snapshot using `python3 scripts/build_catalog.py --index-file <path> --upstream ../../upstream/hermes-agent --captured-at <UTC> --tag v2026.9.14`. A current URL or a file in the tag does not establish that a target bot enables the feature.

Bot source, live service maps, profiles, credentials, sessions and personal memory stay outside this public library.
