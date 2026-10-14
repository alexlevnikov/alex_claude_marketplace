# Loading a tool

A name is not a skill until the file behind it is in context. This is the procedure between
"the tool is `typeset`" and "`typeset` is running" — it is the same whether the
tool came out of discovery (`/design-tools:discover`) or the user named it with `/design-tools:<vendor>:<tool>`.

## The procedure

1. **Resolve.** Run the resolver with the tool's name:

   ```
   bash <plugin-root>/scripts/resolve.sh <tool>
   ```

   Locate `<plugin-root>` from this installed skill's path. Claude plugin commands also expose it
   as `${CLAUDE_PLUGIN_ROOT}`.

   It searches, in order: `$DESIGN_TOOLS_ROOTS` → `.claude/design-tools.local.md` `roots:` →
   the plugin's `vendors/` → project/user skill scopes → optional registry roots. The bundled copy
   is the normal source; explicit overrides are for testing a different revision.

2. **Read the manifest.** It tells you four things:

   | Field | Meaning |
   |---|---|
   | `status: OK` / `MISSING` | found, or not found anywhere — if MISSING, stop (see below) |
   | `load: skill` | found in project or user scope → use the runtime's skill invocation mechanism, if available |
   | `load: read` | bundled or found in an override root → Read the `skill:` file and follow it as if it had been invoked |
   | `base:` | present for ui-craft lenses → Read the base **first**, then the lens |

   `dir:` is where the skill's relative `references/…` and `scripts/…` resolve.

3. **Load.** `load: skill` → invoke the skill with the user's request, or read its file if the
   runtime cannot invoke it by name.
   `load: read` → Read `base:` (if any), then `skill:`, then follow the skill's own instructions
   exactly — its "load X", "read references/Y" steps included — against `dir:`.

4. **Only then** the brand-contract step and the read-only-first order from the prompt, and run.

## When it is MISSING

Stop. Say which tool, and where the resolver looked (it prints the list). The installed pack is
incomplete; repair or reinstall it. **Do not run the pass from
memory** — a route into a skill that is not loaded produces generic work with a specialist's name on
it, and that is the exact failure this plugin exists to prevent.

## Why two load modes

The vendor skills live under this plugin's `vendors/` directory, outside the automatic skill list.
The resolver returns their exact files and supporting directory so only selected skills enter
context. This works from any project without separate vendor installs.

## Notes that bite

- **ui-craft lenses are thin.** `typeset` is 60 lines that open with "read `ui-craft/SKILL.md`
  first". Loaded without the base they lose the anti-slop rules and knobs. The resolver prints the
  base; load it.
- **`impeccable` scripts.** Run its current launcher as `<dir>/scripts/impeccable context` from the project directory;
  use the resolver's absolute `dir:` because the upstream skill mentions project-local paths.
- **`disable-model-invocation` skills** (`prototype`, `review-animations`) are fine to load by
  reading — the flag only governs auto-triggering.
- **Two orchestrators never share a context.** Loading is not exempt: if a second orchestrator is
  already loaded in this session, do not load another — hand off to `design-pipeline`.
