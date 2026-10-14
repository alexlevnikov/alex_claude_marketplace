# AI capability library

One versioned marketplace for reusable Claude Code and Codex capability packs.
Install only the packs you need. A pack owns its skills, tools, MCP configuration,
and supporting files; a role combines packs for a type of work without copying
their contents.

| Pack | Use it for | Contents |
| --- | --- | --- |
| [browser-lab](plugins/browser-lab/) | Live browser investigation and debugging | Browser skill and local MCP tools |
| [web-harvest](plugins/web-harvest/) | Search, scrape, crawl, and extraction | Routing skill and hosted MCP connections; credentials stay local |
| [design-tools](plugins/design-tools/) | Improve UI or build a new web surface | Discovery and pipeline skills, commands, wiki, and 87 bundled vendor skills |

The one marketplace catalog is [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json).
Codex can read that catalog too. [Roles](roles/README.md) describe useful pack
combinations; they are workflows, not extra installations or tool permission
boundaries. See [setup](docs/SETUP.md) for install and update commands, and
[library design](docs/LIBRARY.md) for the rules behind this layout.
The [research record](docs/RESEARCH.md) collects source links and lessons for
future changes.

## Use design-tools

Install `design-tools` once. It contains all 87 selected vendor skills and their
support files. No individual vendor installation or `design-studio` checkout is
needed. [LOCK.json](plugins/design-tools/vendors/LOCK.json) pins each upstream
revision and content hash; [attribution](plugins/design-tools/third-party/README.md)
records the licenses and two path adaptations.

| Runtime | One skill | Whole vendor |
| --- | --- | --- |
| Claude Code | `/design-tools:ui-craft:typeset <task>` | `/design-tools:ui-craft <task>` |
| Codex | `$design-tools:design-tools ui-craft:typeset <task>` | `$design-tools:design-tools ui-craft <task>` |

The vendor form runs its master skill when it has one; otherwise it lists that
vendor's choices. Codex 0.155 exposes the two pack skills rather than the nested
Claude commands, so use the `$design-tools:design-tools` form for explicit routing.
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
```
