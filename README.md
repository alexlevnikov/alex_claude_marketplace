# AI capability library

One versioned marketplace for reusable Claude Code and Codex capability packs.
Install only the packs you need. A pack owns its skills, tools, MCP configuration,
and supporting files; a role combines packs for a type of work without copying
their contents.

| Pack | Use it for | Contents |
| --- | --- | --- |
| [browser-lab](plugins/browser-lab/) | Live browser investigation and debugging | Browser skill and local MCP tools |
| [web-harvest](plugins/web-harvest/) | Search, scrape, crawl, and extraction | Routing skill and hosted MCP connections; credentials stay local |
| [hermes-agent-architect](plugins/hermes-agent-architect/) | Research Hermes and design bots | Living component library, deep research, decisions, bot workflows, pinned upstream |
| [telegram-bot-development](plugins/telegram-bot-development/) | Develop Telegram bots | Feature map, implementation guides, and links to current official Bot API docs |
| [vps-operator](plugins/vps-operator/) | Audit VPS services and Tailscale access | Portable skills; private host maps stay outside this repository |
| [openviking](plugins/openviking/) | Search and read owner-authorized OpenViking memory | OAuth HTTP MCP connection and retrieval skill |
| [design-tools](plugins/design-tools/) | Discover design tools or build a new web surface | Discovery and pipeline skills, commands, wiki, and a compatibility copy of 87 vendor skills |
| [design vendor plugins](plugins/design-tools/registry/vendor-plugin-overviews.json) | Install and invoke one vendor independently | 15 standalone packs with direct skills, commands, resources, and license evidence |

The one marketplace catalog is [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json).
Codex can read that catalog too. [Roles](roles/README.md) describe useful pack
combinations; they are workflows, not extra installations or tool permission
boundaries. See [setup](docs/SETUP.md) for install and update commands, and
[library design](docs/LIBRARY.md) for the rules behind this layout.
The [research record](docs/RESEARCH.md) collects source links and lessons for
future changes.

## Use design-tools

Install `design-tools` for discovery and the whole-surface pipeline, or install only
the vendor packs you use. The umbrella keeps its pinned copy for compatibility.
[LOCK.json](plugins/design-tools/vendors/LOCK.json) pins the upstream revisions and
content hashes; [attribution](plugins/design-tools/third-party/README.md) records
the licenses and two path adaptations. Each standalone pack contains its own
copy, lock subset, and license evidence.

| Runtime | One skill | Whole vendor |
| --- | --- | --- |
| Claude Code | `/design-tools:ui-craft:typeset <task>` | `/design-tools:ui-craft <task>` |
| Codex umbrella | `$design-tools:design-tools ui-craft:typeset <task>` | `$design-tools:design-tools ui-craft <task>` |
| Codex vendor pack | `$design-ui-craft:typeset <task>` | `$design-ui-craft:ui-craft <task>` |
| Claude Code vendor pack | `/design-ui-craft:typeset <task>` | `/design-ui-craft:ui-craft <task>` |

For a standalone pack's short overview, invoke `$design-ui-craft:overview` in
Codex or `/design-ui-craft:overview` in Claude Code. Any direct skill or command
without a target also shows the overview instead of changing the project. The
vendor form runs its master skill when it has one; otherwise the overview lists
the available tools. The full command and skill catalog is in each pack's
`OVERVIEW.md`, for example [ui-craft](plugins/design-ui-craft/OVERVIEW.md),
[Emil](plugins/design-emil/OVERVIEW.md), and
[Three.js](plugins/design-threejs/OVERVIEW.md). Use `$` for Codex skills and `/`
for Claude Code commands; `@` is a mention picker, not a skill invocation.

| Standalone pack | Best fit |
| --- | --- |
| [design-ui-craft](plugins/design-ui-craft/OVERVIEW.md) | Web UI system, phases, polish, and review |
| [design-taste](plugins/design-taste/OVERVIEW.md) | Art direction for public websites |
| [design-impeccable](plugins/design-impeccable/OVERVIEW.md) | Design director with shape, audit, polish, and live modes |
| [design-emil](plugins/design-emil/OVERVIEW.md) | Component feel, gestures, and motion critique |
| [design-ibelick](plugins/design-ibelick/OVERVIEW.md) | Fast UI, accessibility, and motion-performance fixes |
| [design-osmani](plugins/design-osmani/OVERVIEW.md) | Web quality, Core Web Vitals, WCAG, and SEO |
| [design-iart](plugins/design-iart/OVERVIEW.md) | Technique-specific web animation recipes |
| [design-lottie](plugins/design-lottie/OVERVIEW.md) | System-agnostic UI motion design |
| [design-motion-principles](plugins/design-motion-principles/OVERVIEW.md) | Create or audit UI motion with visual reports |
| [design-motion-dev](plugins/design-motion-dev/OVERVIEW.md) | Motion.dev and Framer Motion implementation |
| [design-threejs](plugins/design-threejs/OVERVIEW.md) | Vanilla Three.js implementation references |
| [design-awwwards](plugins/design-awwwards/OVERVIEW.md) | Ambitious visual direction for web pages |
| [design-calm-design](plugins/design-calm-design/OVERVIEW.md) | Calm-premium interface concepts and DESIGN.md |
| [design-frontend-god-mode](plugins/design-frontend-god-mode/OVERVIEW.md) | Broad frontend design and build workflow |
| [design-skill-os](plugins/design-skill-os/OVERVIEW.md) | Read-only design principles and rationale |

For a whole new surface, invoke `/design-tools:design-pipeline` in Claude Code or
`$design-tools:design-pipeline` in Codex.

## Check the library

```bash
python3 scripts/check.py
python3 scripts/codex-smoke.py  # if the Codex CLI is installed
```

The first command checks the catalog, role references, skill paths, vendor
hashes, and generated files. The second installs each pack into a temporary
Codex home and checks that its skills load. If `claude` is installed, also run
`claude plugin validate . --strict`. Before publishing changes, run the pinned
Gitleaks pre-commit hook described in [setup](docs/SETUP.md).

To refresh vendor content, clone the 15 upstream repositories under one
directory, then run:

```bash
python3 plugins/design-tools/scripts/update_vendors.py <vendor-checkouts-dir>
python3 plugins/design-tools/scripts/build.py
python3 plugins/design-tools/scripts/export_vendor_plugins.py
```
