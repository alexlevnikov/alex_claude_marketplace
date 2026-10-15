# Hermes Agent Architect

This folder is a Codex skill and its research workspace. The source of truth is
the `alex_claude_marketplace` Git repository. On the VPS, open this folder as
the separate `VPS · Hermes Architect` Codex project; the installed skill points
to the same files. Local edits are visible at the next skill read. Changes from
another machine require an ordinary Git pull in the marketplace checkout.

## Contents

- `SKILL.md`: short routing instructions for designing Hermes bots.
- `references/decision-guide.md`: extension-point and capability selection.
- `references/knowledge-policy.md`: how to preserve verified findings and
  architecture decisions after work.
- `docs/hermes-platform-overview.md`: one complete feature, memory and
  customization map with all 239 official index pages.
- `docs/`: deep research, including memory architecture and provider review.
- `data/docs-catalog.json`: version-aware index of the official Hermes docs.
- `scripts/find_docs.py`: search the catalog and locate pinned documents.
- `scripts/build_catalog.py`: rebuild the catalog from an official index file.
- `upstream/hermes-agent/`: official Hermes source as a Git submodule, pinned to
  `v2026.9.14` at `345cd2b057a452236de401d3534b8502a7465e8d`.

The catalog captured on 2026-10-13 has 239 unique official URLs. It maps 227
to files in the pinned tag and indexes 457 Markdown files from that tag. A URL
may describe a newer feature; a tagged file does not prove a feature is enabled
in any running bot.

Search from this directory with `python3 scripts/find_docs.py memory`. To
initialize the pinned source in another clone, run `git submodule update --init
-- plugins/hermes-agent-architect/skills/hermes-agent-architect/upstream/hermes-agent`
from the marketplace root. For current behavior, also check the [official docs
index](https://hermes-agent.nousresearch.com/docs/llms.txt). A new index can be
captured to a temporary file and compared with the catalog by running
`python3 scripts/build_catalog.py --index-file <path> --upstream
upstream/hermes-agent --captured-at <UTC> --tag v2026.9.14`.

This is architecture knowledge. Bot source and deployment state stay with each
bot. Credentials, OAuth, profiles, sessions, personal memory and raw API
responses with credentials do not belong in the marketplace.
