---
name: hermes-agent-architect
description: Research Hermes Agent and design or extend Hermes bots using version-checked official capabilities and reusable architecture decisions. Use for profiles, skills, plugins, MCP, memory, cron, hooks, delegation, gateways, APIs, or source patches.
---

# Hermes Agent Architect

This skill is the entry point to the Hermes architecture knowledge in the
directory containing this file. Its Git source is
`alex_claude_marketplace/plugins/hermes-agent-architect/skills/hermes-agent-architect`.
Read only the references needed for the current task. For a broad map of
features, memory and customization, open the [complete platform overview](docs/hermes-platform-overview.md).

1. Use [the decision guide](references/decision-guide.md) to choose a Hermes
   mechanism. Search `data/docs-catalog.json` with `python3 scripts/find_docs.py
   <topic>` from this directory, or run the script by its absolute path. Read
   the exact tagged file under `upstream/hermes-agent/website/docs` when present.
   If the submodule is absent, initialize it from the marketplace Git root or
   check the pinned official source at commit
   `345cd2b057a452236de401d3534b8502a7465e8d`.
2. Distinguish three claims: the current official documentation, what is in
   pinned Hermes `v2026.9.14`, and what is enabled in the target bot. Verify
   current claims against official sources. A document in the tag does not prove
   runtime enablement.
3. For a bot on this VPS, read
   `/srv/repos/agent-lab-mvp/docs/HERMES-SERVICES.md`, then inspect its source
   repository, Compose or systemd unit, image and profile before changing it.
   Keep knowledge, deployed code, secrets and runtime data separate.
4. Explain the smallest supported extension point, prerequisites, trust
   boundary, version compatibility, validation and rollback. A core patch needs
   a reason that the documented extension points cannot satisfy.
5. After substantive Hermes work, follow
   [the knowledge policy](references/knowledge-policy.md): preserve verified
   reusable findings and decisions in this skill. Never copy secrets, profiles,
   sessions, private user memory or raw credential-bearing API responses here.

For memory design, read [the memory architecture](docs/hermes-memory-architecture.md)
and, when comparing backends,
[the provider review](docs/hermes-memory-providers-review-2026-10-15.md).
The [README](README.md) explains the catalog and the local project layout.
