# Capability packs and roles

This repository is a library of reusable AI capabilities. Its marketplace is
the installation catalog, not the whole library model.

## Units

| Unit | Owns | Example |
| --- | --- | --- |
| Skill | One procedure and its supporting references or scripts | `browser-lab`'s browser workflow |
| Pack | An installable set with one enable/disable decision | `browser-lab`, `web-harvest` |
| Discovery pack | An index and selection workflow over skills shipped with the pack | The target for `design-tools` |
| Role | A task-focused combination of packs and instructions | [Web researcher](../roles/web-researcher.md) |
| Runtime agent | A Claude or Codex subagent definition used when delegation adds value | A future UI reviewer |

Use a pack when its parts belong to the same installation lifecycle. A role
may recommend several packs without copying their skills. A role is guidance
until it has a native agent definition; it does not itself install or restrict
tools. Native agent definitions must be checked in each supported runtime.

## Where `design-tools` fits

`design-tools` is a self-contained design pack with two entry skills. `design-tools`
ranks candidate tools for existing UI; `design-pipeline` builds a new surface
through ten verified gates. Both load selected skills from the same `vendors/`
inventory. One plugin installation provides the workflows, 87 curated vendor
skills, their supporting files, and the commands and wiki. Vendor skills stay
outside the top-level `skills/` directory so they do not flood automatic
skill discovery.

The first inventory came from `alexlevnikov/design-studio`. The current bundle is refreshed
from 15 upstream repositories; `plugins/design-tools/vendors/LOCK.json` pins each source commit,
source path, copied tree hash, and two packaging path adaptations.
`plugins/design-tools/third-party/README.md` records licenses and attribution. Explicit local roots can override the bundle for development;
normal use needs no path configuration or separate vendor installation.

The registry is an index, the bundle is the actual content, and a successful
agent run is a separate outcome. Structural checks establish that the package
is complete; they do not prove each vendor procedure performs well on every
task. Keep those claims separate when reviewing the library.

## Roles to validate in real work

| Role | Packs | Trigger | Evidence to collect before making it a native agent |
| --- | --- | --- | --- |
| [Web researcher](../roles/web-researcher.md) | `web-harvest`; `browser-lab` when needed | A task needs web retrieval and possibly live browser investigation | Correct routing, source evidence, and a completed representative task |
| [Interface builder](../roles/interface-builder.md) | `design-tools`; `browser-lab` when needed | A task asks to improve existing UI or build a new surface | Correct new-versus-existing routing, dependency checks, and a completed representative task |

The role guides and their machine-readable catalog are in `roles/`. Add a native
Claude or Codex agent only if delegation proves useful. A plugin's MCP servers can be available
throughout an enabled session, so a role description is not a tool-permission
boundary.

## Public library boundary

This repository can remain public. Reusable procedures, catalog metadata, and
non-sensitive examples belong here. Credentials, machine-specific settings,
live host or account maps, and work-only skills belong in their own sources or
local configuration. A public catalog may refer to an upstream skill without
vendoring it; vendoring requires a license and provenance review.
