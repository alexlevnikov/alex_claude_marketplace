# Research: reusable AI harness libraries

Reviewed 2026-10-14. This is a source-backed record for future changes, not an
installation guide. Repository layouts and host behavior can change; follow the
links and recheck them before adopting a pattern. Popularity helped select
examples for study, but is not evidence that a skill works well or is safe.

For this repository's current decisions, see [LIBRARY.md](LIBRARY.md),
[ARCHITECTURE.md](ARCHITECTURE.md), [AUTHORING.md](AUTHORING.md), and the
[improvement log](IMPROVEMENT-LOG.md).

## Vocabulary and decision rule

The [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)
defines a skill as a `SKILL.md` folder with optional scripts, references, and
assets. Its name and description support discovery; detailed instructions and
resources are loaded when needed. Use that format for the reusable procedure.

| Unit | Job in this repository | Add one when |
| --- | --- | --- |
| Skill | A procedure with a clear trigger and optional supporting files | One task needs repeatable guidance |
| Pack/plugin | One install and enable decision for related skills and MCP configuration | The contents share a domain, dependencies, and update lifecycle |
| Discovery pack | Selects among many bundled skills without registering all of them as top-level skills | A collection is useful as one install but too large for automatic discovery |
| Role | Describes which installed packs to combine for a recurring job | A job crosses pack boundaries |
| Native agent | Gives delegated work its own context or execution policy | A representative workflow proves that delegation improves the result |

These are different responsibilities, not interchangeable names. A role guide
does not install tools or enforce permissions. A marketplace registers packs;
registering it does not itself install or enable every pack. See the
[Claude Code marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces)
and [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins).

## GitHub repositories examined

These are concrete examples to revisit. The “takeaway” column is our inference
from each linked repository, not a claim made by its maintainers.

| Source | Observed organization | Takeaway for this library |
| --- | --- | --- |
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | Small `SKILL.md` root with optional `scripts/`, `references/`, and `assets/`; progressive loading | Keep skill instructions portable and put detailed material in referenced files |
| [Anthropic skills](https://github.com/anthropics/skills) | Self-contained skill folders, a template, specification material, and a Claude marketplace | Use individual upstream skills as references, but check each skill's license separately before copying |
| [OpenAI skills](https://github.com/openai/skills) | A catalog of Codex skills with system and installable skill folders | Keep Codex entry skills small and inspectable; do not assume Claude command files become Codex skills |
| [Vercel agent-skills](https://github.com/vercel-labs/agent-skills/blob/main/AGENTS.md) | Skill folders with `SKILL.md`, optional scripts/references, specific trigger descriptions, and usage examples | Make discovery descriptions concrete; keep scripts and reference material close to the skill |
| [Vercel skills installer](https://github.com/vercel-labs/skills) | Installs skills from Git repositories into many agent hosts | Useful distribution option for standalone skills; a skill installer does not replace our pack's MCP and command configuration |
| [Anthropic official plugin directory](https://github.com/anthropics/claude-plugins-official) | Marketplace catalog with separate plugin folders and external entries; documented skill-bundle entries | Keep plugin names stable; consider an external skill-bundle entry when we need a curated subset without copying content |
| [wshobson/agents](https://github.com/wshobson/agents/blob/main/docs/architecture.md) and its [usage guide](https://github.com/wshobson/agents/blob/main/docs/usage.md) | Domain plugins group skills, agents, and commands; adapters and a capability matrix handle different hosts | Packs are a sound installation boundary; add host adapters only when measured compatibility gaps justify their maintenance |
| [Superpowers](https://github.com/obra/superpowers) | A focused software-development workflow expressed as skills, with skill-behavior evaluations alongside infrastructure tests | Evaluate whether the agent follows the procedure and improves an outcome, not only whether files load |
| [ECC](https://github.com/affaan-m/ECC) | Broad harness with skills, agents, commands, hooks, rules, configuration, and per-host directories | Keep portable source separate from host-specific integration; avoid adopting a large harness wholesale for a small personal library |
| [Awesome GitHub Copilot](https://github.com/github/awesome-copilot) | Distinct catalogs for agents, instructions, skills, hooks, and plugins, plus search and browse surfaces | A catalog helps humans discover components, but catalog size alone is not a quality signal |
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills) | Large skill inventory with a catalog and machine-readable index | Indexing becomes valuable at scale; do not automatically load an entire inventory into the agent's skill list |

### Patterns that recur

1. **Portable content, host-specific packaging.** `SKILL.md` is the common
   denominator. Commands, hooks, MCP declarations, native agents, and tool
   permissions vary by host. The [wshobson capability matrix](https://github.com/wshobson/agents/blob/main/tools/adapters/capabilities.py)
   makes this difference explicit. Keep a canonical procedure and add a small
   adapter only for a verified host-specific need.
2. **Install at the right granularity.** A marketplace is a catalog; a plugin
   is the installable bundle. The [wshobson usage guide](https://github.com/wshobson/agents/blob/main/docs/usage.md)
   explicitly separates these operations. Our three packs let browser runtime
   dependencies be enabled separately from HTTP retrieval and design guidance.
3. **Discovery differs from installation.** Large catalogs need a searchable
   index or router. The [Agentic Awesome Skills catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md)
   and [Awesome Copilot catalog](https://github.com/github/awesome-copilot)
   illustrate browse-first organization. Our `design-tools` router is the
   agent-facing counterpart of that pattern.
4. **Structural validity is only the first check.** Superpowers documents
   [behavior evaluations](https://github.com/obra/superpowers#contributing),
   while wshobson distinguishes [static checks from outcome evidence](https://github.com/wshobson/agents#quality-evaluation).
   A plugin install smoke test proves packaging; a representative task proves
   whether the skill and tools actually work together.

## Why `design-tools` is a one-install discovery pack

The first vendor inventory came from
[alexlevnikov/design-studio](https://github.com/alexlevnikov/design-studio).
The current pack contains 87 selected vendor skills from 15 pinned upstream
repositories, plus a registry, two entry workflows, generated Claude commands,
and the vendor files needed to execute each skill. The
[lockfile](../plugins/design-tools/vendors/LOCK.json) records source commits and
copied tree hashes; [third-party notes](../plugins/design-tools/third-party/README.md)
record attribution, license evidence, and local adaptations.

Bundling is deliberate: installing `design-tools` once must make the actual
vendor instructions available. A catalog entry or resolver that points to a
missing `design-studio` checkout would only make the skill discoverable, not
usable. The vendor files live under `vendors/`, outside top-level `skills/`, so
Codex sees the two entry skills rather than 87 competing automatic triggers.
The router resolves `design-tools:<vendor>:<skill>` or
`design-tools:<vendor>` to bundled content. Claude exposes generated slash
commands; Codex uses `$design-tools:design-tools <vendor>:<skill> <task>`.

The [Anthropic plugin directory's skill-bundle form](https://github.com/anthropics/claude-plugins-official#skill-bundle-plugins)
is an alternative worth revisiting if we later want a small subset of vendor
skills registered directly. It does not currently replace the one-install
bundle and selector that this project requires. Some vendor procedures still
need network access or other runtime tools after their instructions are loaded.

## Migration findings that shaped the current layout

The October 2026 inventory behind the first architecture proposal found that
Codex loaded the marketplace and its top-level `SKILL.md` files, while the
generated Claude `commands/*.md` files were not exposed as separate Codex
skills in the tested version. That is why the Codex router is an explicit
entry point. Treat command support in later Codex versions as a behavior to
retest, not as a reason to generate dozens of Codex entry skills now.

The old design tooling also had absolute paths into an iCloud checkout and
Claude-only loading syntax. The current bundle and resolver removed the
machine-specific dependency for ordinary use. A Git working copy in a sync
folder had produced conflicting Git refs, so the [setup guide](SETUP.md)
recommends a normal checkout outside iCloud, with GitHub as the sync channel.

`agents-os` and `alex-git` were removed because they embedded facts that age
quickly: hosts, paths, repository maps, and active account assumptions. The
public library boundary in [LIBRARY.md](LIBRARY.md) also keeps work-only skills
and credentials out. An earlier local `vps` plugin was not part of this
consolidation; its inclusion remains an inventory decision, not an implicit
dependency of the three current packs.

## Distribution, privacy, and dependency boundaries

- **Public or private GitHub works as a marketplace source.** The
  [Claude marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces)
  permits private repositories; the
  [Claude install guide](https://code.claude.com/docs/en/discover-plugins)
  explains that each machine needs working Git credentials for a private
  source. The [OpenAI plugin guide](https://developers.openai.com/plugins/build/plugins)
  documents local and Git-backed Codex marketplaces and the legacy-compatible
  `.claude-plugin/marketplace.json` path. Repo visibility is a distribution
  choice, not a secret-management mechanism.
- **Keep personal state out of skill prose.** Account identities, hosts,
  machine paths, credentials, active sessions, and work-only procedures change
  independently of a reusable skill. Read live state when needed or keep a
  dated, local configuration file outside the public bundle. This was the
  reason `agents-os` and `alex-git` were removed from this marketplace.
- **Treat third-party skills as dependencies.** Before bundling: inspect the
  license, pin the upstream revision, record the original path and copied
  content hash, document adaptations, then exercise a representative task.
  Recheck all of those when updating. A GitHub star count, a passing parser,
  or a persuasive README is not enough.
- **Keep host integrations explicit.** Claude's command injection and
  `allowed-tools` do not automatically map to Codex. Preserve portable
  instructions in `SKILL.md`; verify each native command, hook, agent, and MCP
  declaration in the host that will run it.

## Runtime and verification lessons from this repository

The [architecture](ARCHITECTURE.md) and
[improvement log](IMPROVEMENT-LOG.md) contain the detailed measurements and
decisions. The reusable lesson is to test four separate claims:

| Claim | Evidence required | Current check |
| --- | --- | --- |
| Files and catalog are complete | Paths, hashes, generated outputs, references | `python3 scripts/check.py` |
| A host can install the pack | Disposable install and visible entry skills | `python3 scripts/codex-smoke.py`; `claude plugin validate . --strict` where Claude is installed |
| Dependencies are ready | Browser runtimes, endpoint reachability, credential source | `bash doctor.sh`; `bash validate-keys.sh` on the user's machine |
| The workflow succeeds | A real tool call and a representative task with reviewed output | Manual host-specific test; record the task, result, and failure mode |

`doctor.sh` and `validate-keys.sh` cannot prove that every MCP tool responds or
that a skill routes correctly. In August 2026 they passed while Chrome DevTools
still failed in concurrent sessions; see the [improvement log](IMPROVEMENT-LOG.md).
Codex's disposable install check also does not verify a user's desktop cache,
provider credentials, or browser. Keep those limits visible in future reports.

The split between `web-harvest` (hosted HTTP backends) and `browser-lab`
(local stdio backends) is a runtime decision as well as a subject boundary.
The old key failure showed that a secret present in an interactive shell may
still be absent from a GUI-launched agent. Validate the source of credentials
and an actual authenticated request on each host; never commit values.

Earlier focused surveys remain useful when the corresponding question returns:

| Local record | What it established |
| --- | --- |
| [Marketplace structure](specs/2026-08-12-plugin-marketplace-structure-design.md) | Plugin boundaries and bundle-versus-reference connector models |
| [Dynamic loading prior art](specs/2026-08-18-mcp-dynamic-loading-prior-art.md) | Existing MCP gateways and the difference between tool-schema cost and process cost |
| [Gateway decision](specs/2026-08-19-mcp-gateway-design.md) | Why a gateway was considered and then declined for the current browser setup |
| [Web-harvest split](specs/2026-08-19-web-harvest-split-design.md) | Why hosted retrieval and local browser tooling became separate packs |

## What to revisit next

1. **Role promotion:** run the [interface-builder](../roles/interface-builder.md)
   and [web-researcher](../roles/web-researcher.md) guides on real tasks. Add
   native agents only if separate context or delegation measurably helps.
2. **Desktop acceptance tests:** on each installed machine, record installed
   plugin versions, one vendor selector invocation, one browser MCP action,
   and one authenticated retrieval request. The VPS packaging tests cannot
   stand in for those results.
3. **Vendor refresh:** rerun the updater and lockfile checks against pinned
   upstream revisions; review behavior and licenses before accepting diffs.
4. **Cross-host adapters:** add them when a concrete Claude/Codex difference
   breaks an important workflow. Re-run both hosts after each runtime update.
5. **Discovery quality:** watch for incorrect automatic triggering, hard-to-find
   skills, and stale catalog entries before expanding the pack or role count.

Avoid copying another repository's full harness merely because it is popular.
Choose one observed pattern to solve one measured problem, then test it here.
