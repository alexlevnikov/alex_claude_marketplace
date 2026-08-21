# Loading, roots and maintenance

How a tool name becomes a running skill, where the plugin looks, how to point it somewhere else,
and how to keep the generated layer honest.

## The moving parts

| Part | File | Role |
|---|---|---|
| Registry | `registry/tools.json` | source of truth: roots, vendors, every tool with vendor · mode · class · group · routable · for / not-for |
| Resolver | `scripts/resolve.sh <tool>` → `resolve.py` | finds `<root>/<tool>/SKILL.md`, prints a load manifest |
| Generator | `scripts/build.py` | writes `commands/<tool>.md`, `wiki/tools/<tool>.md`, `wiki/README.md` from the registry + installed frontmatter |
| Discovery | `skills/design-tools/SKILL.md` + `commands/discover.md` → `scripts/discover.sh` | runs the task through the whole set (index + lexical pre-rank), the model ranks, the user selects |
| Compose | `scripts/compose.sh` | turns the selected tools into a prompt skeleton with resolved `Load:` lines; the model fills it and writes `.design-tools/<slug>.prompt.md` |
| Run | `commands/run.md` | executes a written prompt: loads each tool as its `Load:` line says, follows the procedure |
| Per-tool commands | `commands/<vendor>-<tool>.md` | `/design-tools:<vendor>-<tool>` — skip discovery, load one tool by name. Vendor-first names so the picker groups them; no double prefix when the tool already starts with the vendor key; `command` in the registry overrides |
| Vendor entry commands | `commands/<vendor>.md` | `/design-tools:<vendor>` — runs the vendor's `master` skill exactly as the vendor designed it (discovery's guardrails not layered on), or lists and dispatches the vendor's tools when there is no master |
| Demo | `commands/demo.md` → `scripts/dashboard.sh` | `/design-tools:demo [tool]` — open the design-studio dashboard or a tool's bake-off demo, if present (`registry/tools.json` → `studio`, override `$DESIGN_STUDIO_DIR`) |

Hand-written and never overwritten: `commands/discover.md`, `commands/run.md`, `commands/tools-list.md`, `commands/demo.md`,
`wiki/vendors/*.md`, this file, and everything under `skills/`.

## Search order

```
1. $DESIGN_TOOLS_ROOTS                      colon-separated dirs, each holding <tool>/SKILL.md
2. .claude/design-tools.local.md  roots:    walk-up from the working directory
3. <project>/.claude/skills/<tool>          walk-up from the working directory, stops at $HOME
4. ~/.claude/skills/<tool>
5. <plugin>/vendors/<tool>                  (empty today — a place to vendor MIT skills verbatim)
6. registry/tools.json → roots[]            today: design-studio/.claude/skills
```

Hits in 3–4 are in the session's skill scope, so the manifest says `load: skill` and the Skill tool
is used by name. Everything else is `load: read`: the model reads the file and follows it.

## Pointing the plugin at another inventory

Per project — `.claude/design-tools.local.md`:

```markdown
---
roots:
  - /absolute/path/to/skills-dir
  - ~/another/skills-dir
---
Notes for humans go here; the resolver reads only the frontmatter.
```

Per shell — `export DESIGN_TOOLS_ROOTS=/path/one:/path/two`.

Permanently — edit `roots` in `registry/tools.json` and rebuild.

Putting the skills *into* a project (`bash design-studio/scripts/skillset.sh install <set> <project>`)
is still the best option where the session will do a lot of design work: the Skill tool then sees
them by name, their `allowed-tools` apply, and nothing depends on an iCloud path.

## Maintenance

| After… | Do |
|---|---|
| installing / removing / upgrading a vendor skill in design-studio | `python3 scripts/build.py` — the wiki pages re-read frontmatter and file lists |
| adding a tool to the set | add an entry under `tools` in `registry/tools.json` (and the vendor under `vendors` if new — with `display`, and `master` if it has one), rebuild; the command and wiki page appear. Commands are `<vendor>-<tool>` and descriptions come from the tool's `does` sentence |
| retiring a tool | remove its registry entry, rebuild — the generator deletes the stale command and page |
| editing `phrases.md` / `collisions.md` / `stacking.md` | rebuild — tool pages quote the phrasings and cross-links; `discover.sh` reads `phrases.md` live |
| before committing | `python3 scripts/build.py --check` must print ✔; `bash scripts/resolve.sh --all` must show N/N |

`resolve.sh --all` is also the honest answer to "which of my tools are actually installed right now".

## Known caveats

- `${CLAUDE_PLUGIN_ROOT}` is the plugin's install directory. Claude Code substitutes it as text in
  a plugin command's markdown body and in its `allowed-tools` Bash rules (docs: plugins-reference,
  skills). The generated commands use it in an inline `!`bash …`` block so the manifest is in the
  prompt before the model reads the command. Injected commands never prompt — if no `allowed-tools`
  rule matches, the invocation aborts — so each command carries the rule in both quoted and
  unquoted forms (the iCloud path has spaces). If a harness does not substitute the variable at
  all, the command says so and gives a `find` one-liner as a fallback.
- Skills loaded by reading do not get their frontmatter `allowed-tools` applied by the harness;
  the usual permission flow applies instead.
- `impeccable`'s own scripts are referenced project-relative in its frontmatter; when loaded from a
  root, call them by the absolute `dir:` the manifest prints.
