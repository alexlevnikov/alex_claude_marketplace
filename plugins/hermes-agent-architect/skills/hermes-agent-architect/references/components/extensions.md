---
id: extensions
kind: component
status: verified
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Skills, plugins and MCP

Use a Hermes skill for reusable procedure or knowledge. Use a general plugin when the bot needs a Hermes tool, hook or command. Use a provider plugin for a documented provider contract. Use MCP for an external tool service. A core patch is the last extension point when documented contracts cannot satisfy the requirement.

For each choice, identify loading and enablement, tool permissions, untrusted inputs, secret source, failure behavior and version compatibility. Keep bot-specific code in the bot's source repository. Avoid a second Telegram poller for one token.

For owner-directed changes to a bot's procedures, the pinned `skill_manage` tool writes the active profile's skills. With `skills.write_approval: true`, it stages every skill write for `/skills approve`; with `false`, it applies the write immediately. This setting does not grant source-code or shell access. A container that copies bundled skills into the writable profile on every startup can overwrite those edits. Seed bundled files only when absent or unchanged since the previous bundle, and verify an owner edit remains after startup. Evidence: pinned `tools/skill_manager_tool.py` and `tools/write_approval.py`; isolated and deployed Life Manager profile checks on 2026-10-15. This is a deployment pattern, not an upstream guarantee about custom entrypoints.

Evidence: [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins), [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp), [plugin developer guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins). Consult pinned files through `scripts/find_docs.py` and review if extension contracts change.
