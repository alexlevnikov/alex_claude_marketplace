---
name: openviking
description: Use when the owner asks Codex or Claude Code to find, read, or verify context in their OpenViking memory through the configured MCP server.
---

# OpenViking memory

Use the `openviking` MCP connection for owner-authorized retrieval. If the connection needs authorization, follow the one-time-code flow in [setup](../../README.md); do not request the owner API key in chat.

Start with `find` for semantic discovery or `grep`/`glob` for exact text and paths. Use `list` and `tree` to browse, then `read` the most relevant nodes. Report the returned source paths and any IDs, versions, or hashes that matter to the answer. A retrieval result can be a summary or projection, so inspect the full node before treating it as source evidence.

The current gateway exposes only `find`, `read`, `list`, `tree`, `grep`, `glob`, and `health`. Do not infer that a write, import, or bot migration was performed from a successful read. If a user requests a change, handle that as a separate task in the appropriate source repository and verify the live service before claiming deployment.
