# Operations, verification and recovery

## Completion and observability

Track `task_id` for each import and session commit. `pending` and `processing` both need to reach zero before a queue is empty, but an empty queue alone does not establish success. Check the task terminal status, error, archive URI, `.done`, and `memory_diff.json`. Measure `source sessions/messages discovered`, `captured`, `committed`, `extraction completed/failed`, lag, and exact-source recall separately. [Task API](upstream/docs/en/api/17-tasks.md), [queue lifecycle](upstream/docs/en/concepts/16-queue-lifecycle.md), [metrics](upstream/docs/en/api/09-metrics.md), [observability](upstream/docs/en/guides/05-observability.md).

## Backup and restore

Back up the complete persistent workspace, vector index, configuration without publishing keys, and the secret keys needed to decrypt data. Use a consistent stopped-service or backend-supported snapshot; test restoration on an isolated instance and compare sample session messages, memory files, search results, and ACLs. Built-in file-tree snapshots do not version ACLs or vector indexes and cannot replace a full disaster-recovery backup. Backend multi-write copies are asynchronous; verify lag before treating one as a recoverable copy. [Storage](upstream/docs/en/concepts/05-storage.md), [snapshots](upstream/docs/en/guides/15-snapshot.md), [multi-write storage](upstream/docs/en/concepts/14-multi-write-storage.md).

## Upgrade and rollback

Record server revision, image digest, SDK, CLI, plugin versions, embedding dimension/model, and schema migration notes before updating. Back up before first write by the new version. Some local index record-format changes are one-way for older executables; executable rollback alone may fail. Restore the pre-upgrade data copy if downgrade is required. Change one agent integration at a time, inspect real health and a complete commit/extraction/search cycle, and keep native source logs until import parity is proven. [Storage compatibility](upstream/docs/en/concepts/05-storage.md), [deployment](upstream/docs/en/guides/03-deployment.md), [Hermes integration](upstream/docs/en/agent-integrations/05-hermes.md).

## Nightly consolidation

OpenViking does not provide a universal switch meaning “capture all agents now, extract only at night.” Live plugins can commit during the day. If night-only inference is mandatory, arrange capture without immediate commit and schedule explicit commits, or customize the integration; test crashes and restart recovery. A simpler first release lets OpenViking extract on its normal commits and runs a nightly reconciliation/review job over completed `memory_diff` records. That job can flag unsupported or contradictory claims, stale memories, sensitive data and missing sessions without falsely promising that the model itself only runs at night. [Session lifecycle](upstream/docs/en/concepts/08-session.md), [log ingestion](upstream/docs/en/agent-integrations/09-log-ingestion.md).
