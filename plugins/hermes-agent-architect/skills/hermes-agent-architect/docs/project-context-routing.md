# Project context: where to look before working

Use these instructions to recover the current project context. Start from the project being changed; load research when a concrete design question requires it. These routing instructions were checked on 2026-10-22. Project plans and actual deployment can advance independently of this plugin.

## Resolve the project and read its current instructions

1. Identify the affected project from the request. Use the installed host architecture skill and its private project registry (`CODEX_PROJECTS.md`, and `HERMES-SERVICES.md` for Hermes) to resolve the actual source checkout and running service. Keep physical paths and runtime state in that private registry.
2. Read that checkout's `AGENTS.md`, `README.md`, `resources/README.md` when present, and the relevant documents below. In Linear, find the project by name, list its **Resources**, and read the full current plan and relevant active issues. An issue summary or a historical research recommendation is not the current implementation contract.
3. Follow the matching project route. For work spanning multiple projects, read the shared plan and the instructions for each affected producer/consumer. If Linear is unavailable, use the project-local plan and state which source was available; do not invent current status or ask the owner to repeat information that the checkout contains.
4. State the applicable decision, observed implementation and next unfinished step before changing code. Owner corrections take precedence over older plans. Use runtime/source evidence to describe what exists, the current plan for what should be built, and research for the rationale. Resolve contradictions explicitly rather than treating a proposed feature as deployed.

## Reflection: diary, notes, graph, podcasts

Find **«Reflection Agent — дневник и голосовые ответы»** in Linear. Read the Resources document for the feature, related issues, and the shared memory plan if storage/search is involved. In the resolved Reflection checkout, read `docs/REFLECTION-NOTES.md` for the editor/feed, `docs/HERMES-REFLECTION-HANDOFF-RU.md` for implementation history and `docs/PARALLEL-PROCESSING.md` for processing/graph writes.

Before touching data flow, inspect the relevant current code: `runtime/reflection_pipeline.py` for processing/commit, `runtime/reflection_links.py` for evidence-backed relations, `upload/notes_catalog.py` for reading graph data, and `runtime/reflection_relay.py` for note actions. Podcast revisions use `runtime/reflection_youtube_revision.py`. Locate current originals, graph and deployed configuration through the private registry; do not infer them from research. Preserve author text, analysis attribution, source versions and verified citations.

## Life Manager: book knowledge, coaching and personal planning

Find **«Hermes Life Manager — дисциплина и личное планирование»** in Linear. Read its architecture/plan document, the **«OpenViking для Life Manager — единый план и интеграция»** pointer in Resources, and the linked canonical shared-memory plan. Follow the links to full documents; the pointer is not a duplicate implementation spec.

In its checkout, start with `README.md`, then `docs/tool-skill-map.md` for tools, `docs/neurosprint-rollout.md` and `docs/pilot-protocol.md` for the book workflow, `docs/acceptance.md` and `docs/runbook.md` for delivery. For a nightly task also read `references/nightly-procedure.md` and verify the actual scheduler. If the change affects book retrieval, continue with the Corpus route; do not rebuild a parallel book index just because an older research document suggested one.

## Hermes Corpus: book/podcast processing and retrieval evaluation

Resolve the Corpus source project through the private registry. In Linear, its canonical document **«Hermes Corpus — план, реализация и результаты испытаний»** is in Reflection Resources, with a link from Life Manager; do not assume there is a separate Linear project named Hermes Corpus.

Read `README.md`, `docs/IMPLEMENTATION-AND-TESTS.md`, `docs/VALIDATION.md`, `docs/BOT-INSTRUCTIONS.md`, and `docs/RUNBOOK.md`. Inspect `src/hermes_corpus/model.py`, `bundle.py`, `publish.py` and the relevant retrieval code before changing schemas or publication. Resolve the active manifest and source versions from runtime; a test recorded in the report may concern an older release. Existing Corpus results describe that implementation, not OpenViking. Preserve complete methods, provenance and citation anchors when evaluating a replacement.

## Shared VPS memory / OpenViking: consolidation, sessions and dreaming

First read **«Единый контекст VPS — архитектура памяти, сессий и ресурсов V2»** from Reflection Resources; Life Manager Resources points to it. The project-local file `resources/vps-unified-context-memory-architecture-v2-2026-10-22.md` is a VPS copy; the Linear Resources document is canonical while the knowledge directory is not Git-versioned. It defines one access path, explicit owners of Git/Linear/app data, session capture, evidence-based memory and project context. Scope and rollout order remain open. The older **«Единая память VPS — OpenViking, миграция и сравнительный пилот»** document retains the OV-F/OV-R test protocol, but its claim that OV should own all working content has been revised.

Check the existing OpenViking pilot checkout and `docs/pilot-status-2026-10-22.md` before proposing deployment. The isolated server and Studio exist; source import, bot cutover and benchmark had not completed at the V2 checkpoint. Use `resources/openviking-vps-implementation-plan-2026-10-22.md` only for capture details compatible with V2. For API/configuration, use the sibling [OpenViking skill](../../openviking-memory/SKILL.md) and verify the running release. For migration, follow the Reflection and Corpus routes too; confirm each class's writer, published version, replay and rollback. Do not create a second server or treat a research recommendation as deployed state.

## When research is needed

After reading the current project plan, open only the study relevant to the unresolved question:

- Hermes lifecycle and configuration: [memory architecture](hermes-memory-architecture.md).
- Provider choice, self-hosting and trade-offs: [provider study](hermes-memory-providers-review-2026-10-15.md).
- Book/podcast structure and whole exercises: [corpus architecture](hermes-book-memory-architecture-2026-10-21.md).
- Full source versus RAG and evaluation: [context study](full-context-vs-retrieval-research-2026-10-22.md).
- Cross-agent sessions, capture and nightly dreaming: [session study](agent-session-memory-research-2026-10-22.md).

Full research copies are also in Reflection Resources under «Исследование — …» titles, with links from Life Manager. Use the local copies for reusable technical background. Earlier backend/access recommendations are historical; read the current project plan before applying them. Reopen research for a changed version, missing evidence, a failed test or an explicit request, rather than restarting the entire survey.
