# Hermes Agent Architect: living component library

**Decision implemented:** 2026-10-15. The public `alex_claude_marketplace` checkout owns the architect skill and research; each bot and VPS deployment has its own source of truth for runtime state.

## Purpose and layout

The primary `hermes-agent-architect` skill remains a library of Hermes mechanics, reusable component cards, owner-approved architecture decisions, bot patterns and deeper studies. A separate Codex project may open this skill folder while Git remains rooted at the marketplace checkout. Supporting Hermes workflow skills live beside it and read this library. The pinned official upstream submodule lives at the plugin root, outside `skills/`, so its many own `SKILL.md` files do not appear as installed marketplace skills.

| Layer | Canonical content | Update rule |
| --- | --- | --- |
| `SKILL.md` | Short routing and evidence policy | Change when the workflow changes |
| `references/components/` | Mechanics, use conditions, limits, primary sources | Update after versioned verification |
| `references/decisions/` | Owner choices, status and review trigger | Accept only after owner choice; link superseded record |
| `references/patterns/` | Reusable bot designs and validation | Verify against pinned source and intended target |
| `docs/` | Full overview and deep research | Preserve evidence, date and uncertainty |
| `data/docs-catalog.json` | Current official URL index versus pinned files | Rebuild from a reviewed snapshot |
| `../../upstream/hermes-agent/` | Clean `v2026.9.14` source | Move pin only with explicit review |

## Use and learning loop

For a new bot, find the relevant components and prior decisions, compare current official docs with the pinned source, then inspect the target bot separately. After work, save only transferable evidence or a chosen decision. Leave secrets, live profiles, sessions, personal memory, tailnet identifiers and exact host topology in private operations sources. The public validator checks record shape and obvious leaks; human review still decides whether claims are supported.

A local installation pointing at the checkout reads edits on the next invocation. A published plugin cache or another VPS does not update automatically; Git pull or plugin update is still required. No knowledge edit deploys a bot.

## Extension boundaries

The architect library owns knowledge. `hermes-bot-blueprint` turns requirements into a bot architecture, `hermes-extension-author` chooses and designs extension points, and `hermes-runtime-audit` compares a real deployment to source and docs. A separate `vps-operator` plugin holds portable service and Tailscale audits; the machine-specific server map remains private. Avoid adding long-running MCP servers unless a concrete workflow needs them.
