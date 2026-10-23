---
id: memory
kind: component
status: verified
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Memory layers

Separate current session context, curated `USER.md`/`MEMORY.md`, searchable session history and optional memory-provider backends. Choose a provider only for a measured retrieval or cross-session need, with explicit scope, deletion and evaluation. Never use retrieval as authorization or as the source of transactional truth.

The [memory architecture](../../docs/hermes-memory-architecture.md) explains prompt loading, limits and state. The [provider review](../../docs/hermes-memory-providers-review-2026-10-15.md) compares backends. The [book and podcast corpus architecture](../../docs/hermes-book-memory-architecture-2026-10-21.md) designs structure-aware retrieval for specialist bots with source-traceable books and episodes and an optional OpenViking projection. The [project context instructions](../../docs/project-context-routing.md) also covers session capture/dreaming and full-source versus retrieval experiments. The book study describes an earlier optional-projection design; read the [proposed consolidation decision](../decisions/2026-10-22-unified-memory-pilot.md) and current owner plan before treating it as the target architecture. Validate all settings and actual provider activation in the target image and profile.

Evidence: [persistent memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory), [memory providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers), [provider API](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin). Review if the provider interface or memory tool changes upstream.
