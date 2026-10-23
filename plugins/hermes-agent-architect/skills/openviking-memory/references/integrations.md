# Agent integration and capture

## Select one capture owner per source

OpenViking has live agent plugins and an independent `openviking-server ingest` log adapter. Mixing both against the same native session can create duplicate or divergent OpenViking sessions. Decide whether the plugin or the ingester owns a source, record its deterministic session-ID mapping, and reconcile imported message counts. Backfill older logs in bounded batches with `--dry-run` and `--since`. The ingester is disabled both globally and per harness by default. It supports Hermes, Codex, Claude Code and OpenClaw JSONL; OpenCode SQLite is marked experimental. Default log import drops tool input/output. [Log ingestion](upstream/docs/en/agent-integrations/09-log-ingestion.md).

## Hermes

The current catalog plugin supports a **Custom** self-hosted connection, common OpenViking user memory, and optional peer-aware recall. It is different from the bundled provider in older Hermes releases. The current plugin's `recall_scope=shared` searches common and all peer memories under the same user; `peer` adds only the current sender's peer memory. These settings affect automatic recall, not API authorization or shared chat history. Client configuration is profile-specific and should be tested in the pinned Hermes image. [Hermes integration](upstream/docs/en/agent-integrations/05-hermes.md), [external plugin README](https://github.com/volcengine/OpenViking/blob/824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24/examples/hermes-plugin/README.md), [advanced configuration](https://github.com/volcengine/OpenViking/blob/824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24/examples/hermes-plugin/CONFIGURATION.md).

The external plugin requests a commit at 20,000 pending tokens by default, on normal session end, and on session switch. Its non-primary `cron`, `subagent`, and `flush` contexts skip automatic turn upload and commit. It mirrors successful native Hermes memory writes separately and asynchronously. Do not claim complete capture based on `hermes memory status: available`; verify live message and task counts. The bundled provider has different commit behavior. [Capability reference](upstream/docs/en/agent-integrations/16-capability-reference.md), [advanced configuration](https://github.com/volcengine/OpenViking/blob/824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24/examples/hermes-plugin/CONFIGURATION.md).

## Codex, Claude Code, OpenCode

Their integrations provide prompt-time recall, session capture and commits via hooks; MCP supplies explicit search/read tools. A normal exit can still miss a commit on crash or interrupted network. Codex normal-exit capture depends on host version; its documentation identifies 0.145+ for SessionEnd and an idle sweep/fallback for earlier hosts. Verify installed host versions and hook behavior before enabling. [Codex](upstream/docs/en/agent-integrations/04-codex.md), [Claude Code](upstream/docs/en/agent-integrations/02-claude-code.md), [OpenCode](upstream/docs/en/agent-integrations/10-opencode.md), [capability reference](upstream/docs/en/agent-integrations/16-capability-reference.md).

## Practical checks

For each agent, test create/reuse session ID, a user turn, assistant turn, normal end, abrupt exit, restart, network outage, retry, and recall of a verified memory. Capture counts must match the native transcript after deliberate exclusions and deduplication. Test one bot at a time; an agent integration does not authorize starting another Telegram poller. Use an explicit search first, then enable automatic recall after latency and relevance checks.
