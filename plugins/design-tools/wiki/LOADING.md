# Loading, roots and maintenance

How a tool name becomes a running skill, where the plugin looks, how to point it somewhere else,
and how to keep the generated layer honest.

## The moving parts

| Part | File | Role |
|---|---|---|
| Registry | `registry/tools.json` | source of truth: vendors and every tool with vendor · mode · class · group · routable · for / not-for |
| Resolver | `scripts/resolve.sh <tool>` → `resolve.py` | finds `<root>/<tool>/SKILL.md`, prints a load manifest |
| Generator | `scripts/build.py` | writes `commands/<vendor>/<tool>.md`, `wiki/tools/<tool>.md`, `wiki/README.md` from the registry + installed frontmatter |
| Discovery | `skills/design-tools/SKILL.md` + `commands/discover.md` → `scripts/discover.sh` | runs the task through the whole set (index + lexical pre-rank), the model ranks, the user selects |
| Compose | `scripts/compose.sh` | turns the selected tools into a prompt skeleton with resolved `Load:` lines; the model fills it and writes `.design-tools/<slug>.prompt.md` |
| Run | `commands/run.md` | executes a written prompt: loads each tool as its `Load:` line says, follows the procedure |
| Per-tool commands | `commands/<vendor>/<tool>.md` | `/design-tools:<vendor>:<tool>` — skip discovery, load one tool by name. Commands live in vendor subdirectories |
| Vendor entry commands | `commands/<vendor>.md` | `/design-tools:<vendor>` — runs the vendor's `master` skill exactly as the vendor designed it (discovery's guardrails not layered on), or lists and dispatches the vendor's tools when there is no master |
| Demo | `commands/demo.md` → `scripts/dashboard.sh` | `/design-tools:demo [tool]` — open the design-studio dashboard or a tool's bake-off demo, if present (`registry/tools.json` → `studio`, override `$DESIGN_STUDIO_DIR`) |

Hand-written and never overwritten: `commands/discover.md`, `commands/run.md`, `commands/tools-list.md`, `commands/demo.md`,
`wiki/vendors/*.md`, this file, and everything under `skills/`.

## Search order

```
1. $DESIGN_TOOLS_ROOTS                      colon-separated dirs, each holding <tool>/SKILL.md
2. .claude/design-tools.local.md  roots:    walk-up from the working directory
3. <plugin>/vendors/<tool>                  pinned upstream snapshot
4. <project>/.claude/skills or .agents/skills/<tool>   walk-up from the working directory
5. ~/.claude/skills or ~/.agents/skills/<tool>
6. registry/tools.json → roots[]            optional fallback
```

Hits in project and user skill scope produce `load: skill`, so use the runtime's skill
invocation mechanism when available. The bundled copy and other roots produce `load: read`:
read the file and follow it.

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

The bundled inventory is used by default from any project. Use explicit roots only to test a
different version; they override the pinned copy and can change outcomes.

## Maintenance

| After… | Do |
|---|---|
| refreshing vendor checkouts | run `python3 scripts/update_vendors.py /path/to/vendor-checkouts`, review attribution, then `python3 scripts/build.py` |
| adding a tool to the set | add an entry under `tools` in `registry/tools.json` (and the vendor under `vendors` if new — with `display`, and `master` if it has one), rebuild; the command and wiki page appear. Set `upstream_path` to the vendor skill file; command descriptions come from the tool's `does` sentence |
| retiring a tool | remove its registry entry, rebuild — the generator deletes the stale command and page |
| editing `phrases.md` / `collisions.md` / `stacking.md` | rebuild — tool pages quote the phrasings and cross-links; `discover.sh` reads `phrases.md` live |
| before committing | `python3 scripts/check_bundle.py` and `python3 scripts/build.py --check` must pass; `bash scripts/resolve.sh --all` must show N/N |

`resolve.sh --all` is the answer to "which of the bundled tools can this install load right now".

## Known caveats

- `${CLAUDE_PLUGIN_ROOT}` is the plugin's install directory. Claude Code substitutes it as text in
  a plugin command's markdown body and in its `allowed-tools` Bash rules (docs: plugins-reference,
  skills). The generated commands use it in an inline `!`bash …`` block so the manifest is in the
  prompt before the model reads the command. Injected commands never prompt — if no `allowed-tools`
  rule matches, the invocation aborts — so each command carries the rule in both quoted and
  unquoted forms. If a harness does not substitute the variable at
  all, the command says so and gives a `find` one-liner as a fallback.
- Skills loaded by reading do not get their frontmatter `allowed-tools` applied by the harness;
  the usual permission flow applies instead.
- `impeccable`'s own scripts are referenced project-relative in its frontmatter; when loaded from a
  root, call them by the absolute `dir:` the manifest prints.
