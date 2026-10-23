---
id: 2026-10-22-unified-memory-pilot
kind: decision
status: proposed
pinned_tag: v2026.9.14
verified_utc: 2026-10-22
---

# Consolidate memory through a bounded pilot

Scope: proposed design informed by an owner-requested OpenViking consolidation project; not a global default or a completed deployment. The owner selected OpenViking as the direction. Backend acceptance, migration and retrieval-policy selection require the experiment recorded in the current private project plan.

## Proposed target

One shared context access path and object/revision/evidence contract. OpenViking is the candidate context catalog and memory backend. Git owns code and technical documents; Linear owns project status and issues; each operational app owns its records; native journals own original session events. Mirror those into OV with source versions, freshness and deep links. For books, notes and memories, decide writer ownership by class after the relevant edit/replay/restore gates. Preserve complete corpus bundles, note provenance and citation checks. Avoid two independent writers or a permanent two-way sync.

Compare the existing system as control against OV-F (selected full source) and OV-R (structural retrieval plus complete bundle/evidence expansion), both on one OV instance. A small corpus can favor full-source reading. Test project-plan freshness, session capture, memory evidence, storage, editing and recovery separately from answer quality. If OV fails a backend gate, retain the current owner for that content class behind the shared adapter and investigate the concrete failure.

The isolated OV server and Studio are running at this checkpoint, while import, benchmark and bot cutover remain unproven. External embedding quota currently blocks semantic retrieval. Existing note editors need a supported writer adapter or replacement editing path; direct writes into OV backend files are not a verified integration. Treat Wiki or additional graph generation as later measured improvements.

## Evidence and review trigger

See [project context instructions](../../docs/project-context-routing.md), [full-context research](../../docs/full-context-vs-retrieval-research-2026-10-22.md), [session research](../../docs/agent-session-memory-research-2026-10-22.md), and [OpenViking storage contracts](https://github.com/volcengine/OpenViking/blob/824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24/docs/en/concepts/05-storage.md). The date records the proposal/research checkpoint, not a runtime validation. Revisit after benchmark/restore results, API changes or a changed ownership/access requirement. Project-specific all-bots access is not inferred for other deployments.
