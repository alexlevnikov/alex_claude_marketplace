# Hermes library and portable VPS skills: implementation plan

Status: implemented in the marketplace working tree on 2026-10-15; publication remains a separate Git operation.

## Goals and boundaries

Keep `hermes-agent-architect` as the main living library of Hermes mechanics, component cards, deep research, architecture decisions and reusable bot patterns. Support specific design and audit tasks with short sibling skills. Keep the marketplace public: no server map, real tailnet policy, credentials, runtime profiles, session data or personal memory. The existing private host-architecture skill remains the owner of machine topology.

## Work sequence

1. Move the pinned Hermes submodule from the architect skill directory to the Hermes plugin root; update paths and verify that Codex no longer discovers its nested skills.
2. Preserve overview and research; add component cards, a searchable knowledge corpus, an accepted library-boundary decision and a new-bot pattern. Require versioned evidence and a public-content check for future additions.
3. Add `hermes-bot-blueprint`, `hermes-extension-author` and `hermes-runtime-audit` as focused workflows that read the architect library rather than duplicate it.
4. Add a separate, skills-only `vps-operator` plugin for portable service and Tailscale access reviews. Keep the machine-specific inventory in private sources.
5. Validate skill frontmatter, links, catalog paths, manifest registration, public hygiene and the local Codex installation. Do not alter running services.

## Acceptance criteria

- The architect skill still links to its overview, memory studies, official catalog, decisions and patterns.
- The pinned source remains at commit `345cd2b057a452236de401d3534b8502a7465e8d`, with no nested upstream skill in the installed architect directory.
- New skills appear as top-level plugin skills and can resolve shared library references.
- Public authored files contain no concrete VPS or tailnet inventory.
- Read-only checks pass, and any unrelated working-tree changes remain untouched.
