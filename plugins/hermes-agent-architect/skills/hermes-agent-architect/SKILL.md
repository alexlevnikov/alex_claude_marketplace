---
name: hermes-agent-architect
description: Research Hermes Agent capabilities and maintain a versioned library of bot components, architecture decisions, patterns, and deep studies. Use for Hermes platform design and reusable knowledge; use focused sibling skills for bot blueprints, extensions, and runtime audits.
---

# Hermes Agent Architect

This is the durable, public component and research library for designing Hermes bots. Keep it as the primary place for reusable platform mechanics, evidence, decisions and deep studies. The owning Git repository is `alex_claude_marketplace`; the skill directory can also be opened as its own Codex project.

1. Search [the component index](references/components/index.md), [decision guide](references/decision-guide.md), prior [decisions](references/decisions/) and [patterns](references/patterns/) before proposing an architecture. Use `python3 scripts/find_knowledge.py <topic>` for the authored library and `python3 scripts/find_docs.py <topic>` for the official catalog.
2. Before any pinned-source claim, run `python3 <skill-dir>/scripts/resolve_upstream.py --json`, where `<skill-dir>` is the directory of this installed `SKILL.md`, independent of the shell working directory. The resolver checks the catalog commit, a clean Git tree and `website/docs`; it finds either the adjacent submodule or the standard external marketplace checkout described in the [README](README.md). Use `--file website/docs/user-guide/features/memory.md` (or another source-relative file) to verify its bytes and get a readable absolute path. On exit code 2, explicitly report that pinned source is unavailable and that implementation claims remain unverified; do not substitute the current website or initialize/repair a checkout without authorization. The [catalog](data/docs-catalog.json) separates current URLs from pinned `v2026.9.14` paths. Verify current claims against official sources. Tagged code does not prove enablement in a target bot.
3. For a deployed bot, inspect its private service inventory, source repository, Compose/systemd definition, image and runtime profile. Use a host-specific architecture skill when one is installed. Never infer deployment from this public library.
4. Explain the selected component or extension point, prerequisites, data and permission boundaries, version compatibility, validation and rollback. A core patch needs a reason that supported extension points cannot satisfy the need.
5. After substantive Hermes work, follow the [knowledge policy](references/knowledge-policy.md): save verified reusable findings and owner-approved decisions here. Keep live profiles, secrets, sessions and personal memory outside this public plugin.

For a broad feature map read the [platform overview](docs/hermes-platform-overview.md). For memory design read the [memory architecture](docs/hermes-memory-architecture.md) and [provider review](docs/hermes-memory-providers-review-2026-10-15.md). The [README](README.md) explains layout and commands.
