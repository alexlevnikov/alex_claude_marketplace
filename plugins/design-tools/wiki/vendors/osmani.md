# web-quality-skills — Addy Osmani

**Upstream:** https://github.com/addyosmani/web-quality-skills
**Bundled:** six v2 skills: `web-quality-audit`, `core-web-vitals`, `seo`, `accessibility`, `performance`, and `best-practices`. See [pinned revision](../../vendors/LOCK.json) and [MIT attribution](../../third-party/README.md).

The current skills prioritize field and browser evidence before broad source inspection. The umbrella audit covers performance, accessibility, SEO, best practices, and agentic browsing. It uses live Lighthouse and browser traces when available, with fallbacks when those tools are absent. The focused skills handle named problems such as LCP, keyboard access, or indexing.

`design-pipeline` uses these skills at its audit gate. Read their current `SKILL.md` and references for tool routing; the earlier design-studio inventory carried v1 guidance.

## Invoke

- Claude Code: `/design-tools:osmani <task>` lists the focused choices; `/design-tools:osmani:core-web-vitals <task>` runs a named one.
- Codex: `$design-tools:design-tools osmani:core-web-vitals <task>`.
