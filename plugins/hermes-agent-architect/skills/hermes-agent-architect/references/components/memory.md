---
id: memory
kind: component
status: verified
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Memory layers

Separate current session context, curated `USER.md`/`MEMORY.md`, searchable session history and optional memory-provider backends. Choose a provider only for a measured retrieval or cross-session need, with explicit scope, deletion and evaluation. Never use retrieval as authorization or as the source of transactional truth.

The [memory architecture](../../docs/hermes-memory-architecture.md) explains prompt loading, limits and state. The [provider review](../../docs/hermes-memory-providers-review-2026-10-15.md) compares backends. Validate all settings and actual provider activation in the target image and profile.

Evidence: [persistent memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory), [memory providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers), [provider API](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin). Review if the provider interface or memory tool changes upstream.
