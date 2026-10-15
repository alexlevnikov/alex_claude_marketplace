# Hermes capability and architecture guide

This is an index of design choices, not a claim that every documented feature
is enabled in a target bot. This library pins upstream `v2026.9.14` at commit
`345cd2b057a452236de401d3534b8502a7465e8d`. Start with the tagged file
named in `../data/docs-catalog.json`; check the current official page for
changes and inspect each target image and any local patch separately.

## Choose the right mechanism

| Need | Prefer | Avoid confusing it with | Primary docs |
| --- | --- | --- | --- |
| A new agent identity, config, memory and Telegram token | A separate **profile** and gateway; Bot Mode is a UI over profiles | A session, which shares profile state; a profile is not an OS sandbox | [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), [many gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways), [Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode) |
| A separate conversation or model context within one bot | A **session**; use per-session model selection where supported | Another bot/profile when identity and state should remain shared | [Sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions), [configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Stable persona vs project rules vs remembered facts | `SOUL.md` for identity, context files for project rules, `USER.md`/`MEMORY.md` for curated memory | Storing executable policy only in an LLM prompt | [Which file does what](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what), [context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files), [memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Reusable procedural knowledge | A **skill**, optionally distributed through a tap | A plugin when no new runtime tool or hook is needed | [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [creating skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills) |
| Custom tool, hook, slash command, or bot-specific integration | A **general plugin** with `plugin.yaml` and explicit enablement | Editing Hermes core or treating untrusted input as authorization | [Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins), [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins), [hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) |
| Existing external service exposing tools | **MCP** server with per-server tool filtering | Reimplementing the same service as a core tool | [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp), [MCP config](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference) |
| Shared or specialist cross-session memory backend | A **memory provider plugin** | Copying `auth.json` or writable profile files between bots | [Memory providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers), [provider API](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin) |
| Alternative context compression | A **context engine plugin** after measuring a real limitation | Enlarging prompts or patching the agent loop reflexively | [Context engine](https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin), [compression](https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching) |
| New model, browser, search, media or secret backend | Its corresponding **provider plugin** or documented config-driven adapter | A general plugin or fork when a provider contract already exists | [Pluggable interfaces](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins), [model providers](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin) |
| New transport/channel | A supported **platform adapter** or relay connector | A second polling consumer on the same bot token | [Adding adapters](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters), [relay](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/relay) |
| Drive Hermes from an application or editor | OpenAI-compatible **API server**, **ACP**, or programmatic library, according to the caller | Scraping CLI output or opening a new Telegram poller | [Programmatic integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration), [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server), [ACP](https://hermes-agent.nousresearch.com/docs/user-guide/features/acp) |

For the full built-in tool inventory and platform presets, consult
[Tools Reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)
and [Toolsets Reference](https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference).
Tool availability depends on enabled toolsets, platform, provider and credentials;
the catalog is not a list of tools active in a given profile.

For bot memory design, use the local [memory architecture and configuration guide](../docs/hermes-memory-architecture.md), then the [provider comparison](../docs/hermes-memory-providers-review-2026-10-15.md) when a specialist backend is justified.

## Choose the automation primitive

| Work shape | Hermes primitive | Boundary |
| --- | --- | --- |
| Durable scheduled or event-triggered job, including no-LLM script | [Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) and optionally [webhook](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks) | Check delivery target, retry, permissions and duplicate effects. |
| Repeated timer-driven work inside a live session | [Loop](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops) | Not a substitute for unattended cron. |
| Periodic prompt returning to the same idle session | [Heartbeat](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat) | Session lifecycle and owning process matter. |
| One objective with a completion contract and self-continuation | [Persistent goal](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals) | Judge output is not external proof of correctness. |
| Parallel, bounded child tasks of one parent turn | [Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) | Child context and tool access are explicit; not durable multi-agent coordination. |
| Durable work assigned across specialist profiles | [Kanban](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban) | Keep one dispatcher and clear ownership of side effects. |
| Many tool calls within one inference turn | [Code execution](https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution) | RPC/tool permission and resource limits still apply. |

## Media, interfaces and operations

- [Voice/STT/TTS](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode),
  [document extraction](https://hermes-agent.nousresearch.com/docs/user-guide/features/document-extraction),
  [vision](https://hermes-agent.nousresearch.com/docs/user-guide/features/vision),
  [image generation](https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation),
  [browser automation](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser):
  verify provider credentials, media-size limits and transport behavior per bot.
- [Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard),
  [Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/desktop),
  [CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli),
  [TUI](https://hermes-agent.nousresearch.com/docs/user-guide/tui):
  interfaces to the same core but not identical deployment surfaces.
- [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security),
  [secrets](https://hermes-agent.nousresearch.com/docs/user-guide/secrets),
  [managed scope](https://hermes-agent.nousresearch.com/docs/user-guide/managed-scope),
  [Docker network isolation](https://hermes-agent.nousresearch.com/docs/user-guide/egress/network-isolation):
  profile separation is not filesystem or credential isolation. Approval policy,
  toolsets, writable mounts, messaging authorization and egress require separate checks.
- [Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks)
  and [observer hooks](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks)
  differ: use read-only observers for telemetry, behavior-changing plugin hooks
  only when the trust path and failure behavior are understood.

## Version and deployment gates

The current official index has 239 unique pages. Twelve URL paths are not
present in the pinned tag's docs, including Session Storage Recovery, Bot
Screen, Language Packs, Application Declarations and Package Management.
They may be new, renamed, or relocated; do **not** infer the runtime lacks or
has them from a path match alone. Inspect current upstream source/release notes
and the running image before depending on one.

A target bot may use a different image, build chain or local patch. Before a
production change, inspect its private service inventory, source repository,
Compose/systemd definition, deployed image and runtime profile. Never copy
OAuth, memory, sessions or secrets into this public knowledge library.

## Finding the rest of Hermes

The catalog records every indexed page, grouped under Getting Started (7),
Using Hermes (31), Core Features (36), Automation (8), Media & Web (5),
Messaging Platforms (35), Integrations (11), Guides & Tutorials (35),
Developer Guide (56), Reference (14), and More (1). The total is 239 unique
URLs. Run
`python3 scripts/find_docs.py <topic>` from the skill directory to get the
current URL and absolute tagged source path; the catalog also indexes all 457
Markdown files in the pinned tag, including files absent from the current
public index. If the tag has no matching file,
investigate whether the page is newer, renamed or moved before designing
around it.

Important areas beyond the mechanism tables:

- **Execution and recovery:** Git worktrees, Docker backend, checkpoints and
  rollback, managed scope, batch processing, code execution and LSP diagnostics.
- **Context and quality:** curator, context references, prompt assembly,
  compression/caching, memory providers, Mixture of Agents and tool search.
- **Delivery and UI:** Desktop, TUI, dashboard, deliverable artifacts,
  themes, Bot Mode, voice/wake word and computer use.
- **Connectivity:** 35 messaging-platform pages plus webhooks, A2A, relay,
  Google Workspace, MCP, ACP and the API server. Platform pages describe
  different capabilities and authentication models, not interchangeable transports.
- **Models and credentials:** provider routing, fallback providers, credential
  pools, local models, subscription proxy and secret backends. Inspect policy,
  quota and credential ownership before combining them.
- **Extensibility:** plugin catalog, built-in plugins, skills/taps, provider
  plugin contracts, tools, hooks and platform adapters. Prefer a documented
  extension interface before carrying a core patch.

For each proposal, record the exact page and tagged source path, runtime image
and profile, config/toolset prerequisites, data boundary, rollout test and
rollback. An upstream feature page is only discovery evidence until its
specific version and local enablement are verified.
