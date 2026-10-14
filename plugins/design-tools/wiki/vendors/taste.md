# taste-skill — Leonxlnx

**Upstream:** https://github.com/Leonxlnx/taste-skill
**Bundled:** 13 selected skills. See [the live command list](../README.md#commands-grouped-by-vendor) and [pinned revision](../../vendors/LOCK.json).

## Current main skill

`design-taste-frontend` is v2. It draws art-direction choices from bundled research libraries, asks the agent to choose a direction that fits the brief, builds the page, then inspects the rendered result. Its bundled directory includes the direction data, scripts, assets, and references it uses. `design-taste-frontend-v1` remains available explicitly for projects needing the earlier procedure.

The other selected skills cover focused visual direction, brand boards, image generation, redesigns, and output completeness. Image-generation skills need a capable image tool in the running agent.

The earlier design-studio bake-off evaluated an older version of the main skill. Re-test v2 before relying on that comparison for cost or quality decisions.

## Invoke

- Claude Code: `/design-tools:taste <task>` runs the vendor's main skill; `/design-tools:taste:brandkit <task>` runs one named skill.
- Codex: `$design-tools:design-tools taste <task>` or `$design-tools:design-tools taste:brandkit <task>`.
