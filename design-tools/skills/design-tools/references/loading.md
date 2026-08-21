# Loading a tool

A route is a name. A name is not a skill until the file behind it is in context. This is the
procedure between "the route is `typeset`" and "`typeset` is running" — it is the same whether the
router chose the tool or the user named it with `/design-tools:<tool>`.

## The procedure

1. **Resolve.** Run the resolver with the tool's name:

   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh" <tool>
   ```

   If `${CLAUDE_PLUGIN_ROOT}` was not substituted, find it:
   `find ~/.claude/plugins "$HOME/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins" -path '*design-tools/scripts/resolve.sh'`.

   It searches, in order: `$DESIGN_TOOLS_ROOTS` → `.claude/design-tools.local.md` `roots:` →
   the project's `.claude/skills` (walking up) → `~/.claude/skills` → the plugin's `vendors/` →
   the registry roots (`registry/tools.json`, today the design-studio inventory). First hit wins.

2. **Read the manifest.** It tells you four things:

   | Field | Meaning |
   |---|---|
   | `status: OK` / `MISSING` | found, or not found anywhere — if MISSING, stop (see below) |
   | `load: skill` | found in project or user scope → the Skill tool knows it by name; invoke it that way |
   | `load: read` | found in a root → Read the `skill:` file and follow it as if it had been invoked |
   | `base:` | present for ui-craft lenses → Read the base **first**, then the lens |

   `dir:` is where the skill's relative `references/…` and `scripts/…` resolve.

3. **Load.** `load: skill` → Skill tool with the user's request as the argument.
   `load: read` → Read `base:` (if any), then `skill:`, then follow the skill's own instructions
   exactly — its "load X", "read references/Y" steps included — against `dir:`.

4. **Only then** do the brand-contract step and the read-only-first step from `SKILL.md`, and run.

## When it is MISSING

Stop. Say which tool, and where the resolver looked (it prints the list). Point at the tool's wiki
page (`wiki/tools/<tool>.md` → *Where it lives*) for the install line. **Do not run the pass from
memory** — a route into a skill that is not loaded produces generic work with a specialist's name on
it, and that is the exact failure this plugin exists to prevent.

## Why two load modes

The Skill tool can only invoke skills in the session's scope — the project's `.claude/skills`, the
user's `~/.claude/skills`, or a plugin's own `skills/`. The seventy-odd vendor skills live in
design-studio's project scope, so from any *other* project they are invisible to the Skill tool by
name. Reading the file and following it is the same thing the Skill tool does, done by hand; the
manifest makes the by-hand path deterministic instead of a guess at a path.

## Notes that bite

- **ui-craft lenses are thin.** `typeset` is 60 lines that open with "read `ui-craft/SKILL.md`
  first". Loaded without the base they lose the anti-slop rules and knobs. The resolver prints the
  base; load it.
- **`impeccable` scripts.** Its `allowed-tools` assume `.claude/skills/impeccable/scripts/*`
  relative to the project. When loaded from a root, call them as `node "<dir>/scripts/<x>.mjs"`.
- **`disable-model-invocation` skills** (`prototype`, `review-animations`) are fine to load by
  reading — the flag only governs auto-triggering.
- **Two orchestrators never share a context.** Loading is not exempt: if a second orchestrator is
  already loaded in this session, do not load another — hand off to `design-pipeline`.
