# OpenViking for Codex, Claude Code, and ChatGPT

This plugin bundles one retrieval skill and the owner's read-only HTTP MCP connection. It does not bundle secrets or an OpenViking server. The remote endpoint uses OAuth; access is granted by the owner with a one-time code in private Studio. The currently exposed tools are `find`, `read`, `list`, `tree`, `grep`, `glob`, and `health`.

## Codex desktop or CLI

Install the pack from the existing marketplace:

```bash
codex plugin marketplace add alexlevnikov/alex_claude_marketplace
codex plugin add openviking@alex-claude-marketplace
```

If the marketplace is already configured, skip the first command. Restart Codex after installation and connect the bundled `openviking` MCP server when prompted. If the plugin is installed but no MCP connection appears, add it explicitly on the same machine:

```bash
codex mcp add openviking --url https://vps-919b6444.tail77fcdc.ts.net:10000/mcp --oauth-client-registration dcr
codex mcp login openviking --oauth-client-registration dcr
codex mcp list
```

Use either the plugin's bundled connection or the explicit MCP entry to avoid duplicate tools. The OAuth browser flow shows a one-time code. On a device connected to Tailscale, open [private Studio verification](https://vps-919b6444.tail77fcdc.ts.net:8446/studio/oauth/verify), enter the code, and approve. Return to Codex and check that the seven read tools appear. A useful test is: “Find a published Hermes Corpus exercise about reflection, read its source node, and cite its path and ID.”

## ChatGPT Pro on the web

The Git marketplace installation is for Codex and Claude Code; connect the same MCP endpoint separately in ChatGPT:

1. Open [ChatGPT Plugins](https://chatgpt.com/plugins), select **+ → Add custom MCP server**, and name it `OpenViking`.
2. Enter `https://vps-919b6444.tail77fcdc.ts.net:10000/mcp` as the server URL. Select **OAuth** and automatic client registration if offered. Review the permission warning and create the connection.
3. During authorization, copy the one-time code. Open [private Studio verification](https://vps-919b6444.tail77fcdc.ts.net:8446/studio/oauth/verify) on a Tailscale-connected device, enter the code, and approve. Return to ChatGPT to finish connection and inspect the discovered tools.
4. Install the resulting personal plugin if ChatGPT offers that step. In a new web chat, select it with `@OpenViking` and run a source-backed `find` then `read` query.

ChatGPT Pro supports custom MCP read/fetch access; full MCP permissions require a Business or Enterprise/Edu workspace. Custom MCP connection setup is on the web, not in the mobile app. Availability of the **Add custom MCP server** control depends on account and product rollout. Installing this Git pack in Codex does not automatically install it in ChatGPT.

## Claude Code and Claude.ai

For Claude Code, install `openviking@alex-claude-marketplace`; its `.mcp.json` declares the same HTTP endpoint. For Claude.ai, add a custom connector with that URL in **Customize → Connectors**, then complete the same OAuth code approval. These are separate client registrations.

## Connection boundaries

The MCP endpoint is reachable publicly through an authenticated Tailscale Funnel route. Studio and the owner verification page stay on private Tailscale HTTPS. No owner API key belongs in this repository or in ChatGPT/Codex prompts. Published Corpus and completed Reflection Graph records are currently read-only projections; connecting this plugin does not switch bot writers or change originals. If HTTPS port `10000` is rejected by a cloud client, use a dedicated port-443 ingress rather than changing the private Studio URL.
