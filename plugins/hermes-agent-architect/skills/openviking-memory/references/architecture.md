# Architecture and memory semantics

Source snapshot: OpenViking commit `824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24`. Read the linked source page for implementation details and version-sensitive defaults.

## What is stored

OpenViking has three context types: Resource (documents and external material), Memory (extracted interaction knowledge), and Skill (reusable procedures). Each is addressable by `viking://` URI and can expose L0 abstract, L1 overview, and L2 detail. AGFS/RAGFS persists content; a separate vector index stores URI, metadata, vectors, and retrieval text. Back up both. See [architecture](upstream/docs/en/concepts/01-architecture.md), [context types](upstream/docs/en/concepts/02-context-types.md), [layers](upstream/docs/en/concepts/03-context-layers.md), [storage](upstream/docs/en/concepts/05-storage.md).

```text
Agent or ingester -> HTTP/SDK -> Session messages -> commit archive
                                                  -> durable task -> optional summary + memory diff
Resource import -> parser -> content tree -> semantic queue -> L0/L1 + vector index
Query -> optional intent analysis -> global vector search -> optional rerank -> URI -> read L2
```

The current retriever performs global vector search over eligible L0/L1/L2 records. It does **not** recursively walk from directory summaries to leaves. `find()` is a simple single-query path; `search()` can use session-aware intent analysis and issue several typed queries. A reranker only reorders recalled candidates. Scope and identity filters act before results are returned. See [retrieval mechanism](upstream/docs/en/concepts/07-retrieval.md) and [retrieval API](upstream/docs/en/api/06-retrieval.md).

## Session to memory

Create a session, append user/assistant messages, then call `commit`. In the request, OpenViking archives messages and queues background work; later it updates memory files and, when working-memory summaries are enabled, creates summaries. The session result can be `skipped` when there is nothing to archive. For an accepted commit, persist `task_id`, poll [Task API](upstream/docs/en/api/17-tasks.md) until terminal, then inspect the archive's `memory_diff.json` and `.done` marker. A successful commit may legitimately create no memory. See [session concept](upstream/docs/en/concepts/08-session.md) and [session API](upstream/docs/en/api/05-sessions.md).

`memory_diff.json` records adds, updates, deletes, and skipped operations against an archive URI. It does not automatically establish exact claim-to-message citations. If answers need precise evidence, retain message IDs and attach a separately verified source span to promoted claims. `working_memory.enabled` controls archive summaries and defaults off in current session policy; confirm the intended policy in the running version.

## Identity and sharing

`account_id` is the outer boundary. Within an account, `viking://resources/` is shared; memories and sessions under `viking://user/{user_id}/` are private to that authenticated user. A `peer_id` labels or filters a peer collection within one user; it is not another user or tenant. Shared Resources can use ACLs, but ACLs do not turn private memories into shared memories. A shared-memory design therefore needs one common user identity or an explicit publishing bridge from per-agent users. The common identity is simple but grants those clients broad write capability to its user space; separate user keys provide isolation but do not share native memory. See [multi-tenancy](upstream/docs/en/concepts/11-multi-tenant.md), [ACL](upstream/docs/en/concepts/15-acl.md), [data organization](upstream/docs/en/guides/23-data-organize.md).

## Books and podcasts

Import books and episode transcripts as Resources with stable source IDs, hierarchy, and citation metadata. OpenViking's Markdown parser splits sections near its size targets, so it may separate an exercise from its rationale. Preserve an existing structure-aware primary corpus and project its vetted nodes into Resources until whole-unit retrieval and citation parity are measured. Extracted Memory is a derivative of conversations; it must not be presented as a quotation from a book. See [extraction](upstream/docs/en/concepts/06-extraction.md), [resource API](upstream/docs/en/api/02-resources.md), [data organization](upstream/docs/en/guides/23-data-organize.md).
