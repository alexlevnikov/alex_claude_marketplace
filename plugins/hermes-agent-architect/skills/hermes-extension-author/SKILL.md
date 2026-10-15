---
name: hermes-extension-author
description: Design or implement a Hermes Agent skill, plugin, MCP integration, provider, hook, adapter, or justified core patch with version and permission checks. Use for custom bot capabilities and extension contracts.
---

# Hermes extension author

Read the sibling [extension component](../hermes-agent-architect/references/components/extensions.md) and [decision guide](../hermes-agent-architect/references/decision-guide.md). Search the [official catalog](../hermes-agent-architect/data/docs-catalog.json) with `python3 ../hermes-agent-architect/scripts/find_docs.py <mechanism>`, then inspect the matching pinned source in `../../upstream/hermes-agent` and current official docs when the API may have changed.

Select the smallest supported extension contract for the requested behavior. Specify loading and enablement, trust boundary, tool permissions, secrets source, error path and upgrade compatibility. Build bot-specific code in that bot's repository; keep the pinned upstream submodule clean. Validate with a focused local test and, for deployment, the actual image/profile. Document rollback. Preserve a reusable component finding or pattern in the architect library when supported by evidence.
