---
name: hermes-bot-blueprint
description: Turn requirements for a new Hermes Agent bot into a version-checked architecture blueprint. Use when choosing bot identity, channels, memory, tools, automation, deployment ownership, and validation before building.
---

# Hermes bot blueprint

Use the sibling `hermes-agent-architect` library at `../hermes-agent-architect/` for [components](../hermes-agent-architect/references/components/index.md), [prior decisions](../hermes-agent-architect/references/decisions/), [patterns](../hermes-agent-architect/references/patterns/) and [official docs search](../hermes-agent-architect/scripts/find_docs.py). Keep this skill a workflow, not a second knowledge base. Before pinned-source claims run the sibling `hermes-agent-architect/scripts/resolve_upstream.py --json` using the installed skill paths; it locates and verifies the source even when the plugin cache lacks a submodule. Exit code 2 means pinned source is unavailable and must be reported explicitly.

Gather purpose, users, channel, data classification, allowed actions and operating constraints. Choose profile/session boundary, memory layers, extension points and triggers with reasons. Distinguish current docs, the pinned Hermes source and the target image. Write a blueprint covering component choices, data and permission flows, source repository, runtime owner, validation and rollback. Mark assumptions explicitly. If implementing, put bot code in its own repository and leave profiles and secrets outside public Git. Do not treat a project folder or source edit as deployment.

For an existing bot, inspect the private service inventory, source, Compose/systemd, image and profile before changing behavior. Do not start a second poller for an existing Telegram token. Add transferable findings to the architect library after validation.
