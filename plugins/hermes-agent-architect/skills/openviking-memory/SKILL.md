---
name: openviking-memory
description: Use when designing, configuring, integrating, or operating OpenViking as agent memory or a shared context server, including sessions, extraction, retrieval, authentication, and VPS deployment.
---

# OpenViking memory

Use the local documentation copy for concrete settings and API behavior. It contains all 304 Markdown files in upstream `docs` at commit `824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24` (22 October 2026), including the complete English and Chinese trees. Non-Markdown images and site assets stay upstream. This is a source snapshot, not proof that a deployed server or plugin runs that revision. The [documentation index](references/docs-index.md) routes to the right page; [manifest](references/upstream/manifest.json) records the upstream blob for each file. The copied documentation is licensed under the included [AGPL-3.0 license](references/upstream/LICENSE).

## Existing project work

Follow the architect skill's [project context instructions](../hermes-agent-architect/docs/project-context-routing.md), especially the shared-memory route and the affected Reflection/Corpus/Life Manager route. Read the latest canonical plan from Linear project Resources or its project-local copy before configuring OV. Check the integration checkout and actual service to identify unfinished work. Use the research linked there for the specific unresolved question; this documentation snapshot does not establish deployment or benchmark success.

## Choose what to read

| Task | Start with | Then open |
| --- | --- | --- |
| Explain memory and data model | [Architecture notes](references/architecture.md) | `references/upstream/docs/en/concepts/01-architecture.md`, `05-storage.md`, `08-session.md`, `11-multi-tenant.md` |
| Deploy or change server settings | [Server configuration](references/server-configuration.md) | `guides/03-deployment.md`, `configuration/01-server.md`, `guides/04-authentication.md` |
| Attach Hermes, Codex, Claude Code, OpenCode or import history | [Integration notes](references/integrations.md) | `agent-integrations/16-capability-reference.md` and the matching integration page |
| Search, ingest resources, tune recall | [Architecture notes](references/architecture.md) | `concepts/06-extraction.md`, `07-retrieval.md`, `api/02-resources.md`, `06-retrieval.md` |
| Diagnose, back up, upgrade, or recover | [Operations notes](references/operations.md) | `api/17-tasks.md`, `concepts/16-queue-lifecycle.md`, `guides/05-observability.md`, `15-snapshot.md` |

Paths in the last column are relative to `references/upstream/docs/en/`. Search the local tree with `rg` when a setting or operation is not in the index. Read the actual page before stating a default or command. For features added after this snapshot, verify against current official docs and code; label any unverified version difference.

## Invariants that change design decisions

- A server is shared, but memories and sessions are scoped to an authenticated `user_id`; account-shared Resources and Skills have different visibility. ACL rules cover shared Resources, not user memories. Choose identity and keys before calling a deployment “shared memory.”
- `session.commit()` archives messages in the request and schedules summaries and memory extraction. A returned `task_id` is accepted work, not completed work. Check terminal task state and `memory_diff.json` before claiming a new memory exists.
- OpenViking's directory summaries, vector index, and session memories are not a substitute for reconciling every source transcript. Hooks can miss crashes, stopped services, non-primary Hermes contexts, and history that predates installation. Keep native logs until import counts and restore tests pass.
- `memory.extraction_enabled` does not start automatic commits. A nightly review or scheduled commit needs an explicit design; the stock Hermes/Codex integrations may commit during the day.
- The bundled local embedding default is `bge-small-zh-v1.5-f16`. For Russian content, measure a multilingual model before using this default as the production retrieval baseline. Model calls can be local or external; self-hosting the database does not keep text local when an external VLM is configured.
- Separate source material (books, podcasts, transcripts) from extracted claims. Retrieval text and `memory_diff.json` do not by themselves prove a claim is supported by an exact source span.

Before changing a running VPS bot, inspect its source repository, Compose/systemd unit, image revision, and runtime profile. Do not infer deployment from this skill or start a second Telegram poller. Keep private paths, tokens, and session contents out of this reusable skill.

## Updating this skill

Pin one new upstream commit, refresh the copied `docs/**/*.md` files and manifest together, run `python3 scripts/verify_docs.py`, then review changed defaults and integration contracts in the five notes. Keep the prior commit in the change record of the owning repository; do not silently switch to `main` URLs for implementation claims.
