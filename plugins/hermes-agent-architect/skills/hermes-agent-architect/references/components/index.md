# Hermes component library

Read the card for the mechanism you plan to use, then inspect its official and pinned evidence. These cards describe reusable components; they do not assert that a deployed bot enables them.

| Component | Design question | Deep research |
| --- | --- | --- |
| [Profiles and sessions](profiles-and-sessions.md) | Separate bot identity or only conversation state? | [Platform overview](../../docs/hermes-platform-overview.md) |
| [Skills, plugins and MCP](extensions.md) | Reusable instruction, Hermes hook/tool, or external tool server? | [Decision guide](../decision-guide.md) |
| [Memory layers](memory.md) | Prompt memory, searchable history, or provider backend? | [Memory architecture](../../docs/hermes-memory-architecture.md), [provider review](../../docs/hermes-memory-providers-review-2026-10-15.md) |
| [Automation](automation.md) | Scheduled task or event-driven hook? | [Platform overview](../../docs/hermes-platform-overview.md) |

Find owner-approved choices in [decisions](../decisions/) and reusable bot recipes in [patterns](../patterns/). Search all authored material with `python3 scripts/find_knowledge.py <topic>` from the skill root.
