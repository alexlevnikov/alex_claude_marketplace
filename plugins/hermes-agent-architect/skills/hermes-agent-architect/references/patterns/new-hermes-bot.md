---
id: new-hermes-bot
kind: pattern
status: draft
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# New Hermes bot from a reusable blueprint

Start with the bot's purpose, users, channel, data classification and actions. Choose profile/session isolation from [profiles and sessions](../components/profiles-and-sessions.md), memory from [memory](../components/memory.md), and tools from [extensions](../components/extensions.md). Add [automation](../components/automation.md) only for a defined trigger.

Keep bot source in its own repository. Keep credentials and writable profile outside public Git. Document the source, image/tag, Compose/systemd owner, mounts, channel token owner and service inventory in private operations records. For validation, inspect the deployed image and profile, run one safe interaction for each enabled capability, and confirm that no second poller uses the token. Rollback restores the previous source/image and profile state according to the bot's deployment procedure.

This pattern is a starting structure, not a claim that all components are required. Review when Hermes changes its profile, gateway or extension contracts.
