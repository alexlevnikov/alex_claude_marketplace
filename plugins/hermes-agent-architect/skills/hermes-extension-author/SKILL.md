---
name: hermes-extension-author
description: Design or implement a Hermes Agent skill, plugin, MCP integration, provider, hook, adapter, or justified core patch with version and permission checks. Use for custom bot capabilities and extension contracts.
---

# Hermes extension author

For an existing Reflection, Life Manager, Corpus or shared-memory project, first follow the [project context instructions](../hermes-agent-architect/docs/project-context-routing.md) to read the current plan, project Resources and relevant checkout documents. Use that context to resume the actual unfinished work.

Read the sibling [extension component](../hermes-agent-architect/references/components/extensions.md) and [decision guide](../hermes-agent-architect/references/decision-guide.md). Search the [official catalog](../hermes-agent-architect/data/docs-catalog.json) with `python3 ../hermes-agent-architect/scripts/find_docs.py <mechanism>`, then locate the pinned source with `python3 ../hermes-agent-architect/scripts/resolve_upstream.py --json` and inspect the verified root plus current official docs when the API may have changed. Resolve scripts relative to this installed SKILL.md. Exit code 2 means pinned source is unavailable; report it and leave pinned API claims unverified.

Select the smallest supported extension contract for the requested behavior. Specify loading and enablement, trust boundary, tool permissions, secrets source, error path and upgrade compatibility. Build bot-specific code in that bot's repository; keep the pinned upstream submodule clean. Validate with a focused local test and, for deployment, the actual image/profile. Document rollback. Preserve a reusable component finding or pattern in the architect library when supported by evidence.
