---
description: Describe a design task in your own words → the set is searched, a ranked list of tools and vendors is proposed, you pick, and a ready-to-run prompt is written
argument-hint: "<the task in your own words — what is wrong or wanted, and where>"
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/discover.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/discover.sh":*), Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/compose.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/compose.sh":*), Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh":*), Bash(find:*), Read, Write, AskUserQuestion
---

Use the `design-tools` skill (discovery) for: **$ARGUMENTS**

## The set, run against the request

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/discover.sh" $ARGUMENTS`

If the block above is empty or an error, `${CLAUDE_PLUGIN_ROOT}` was not substituted — locate the
scripts and run them yourself:
`find ~/.claude/plugins "$HOME/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins" -path '*design-tools/scripts/discover.sh'`

## Do, in this order

1. **Understand the need** — aspect, place, scope. If the place matters and none is named, ask one
   question. If the scope is a whole new surface, say `design-pipeline` and stop.
2. **Judge** — read the whole index above, not only the pre-rank. Rank by fit to *this* task. Apply
   `references/collisions.md` wherever two candidates overlap and say the discriminator.
3. **Present** — a ranked list, each line: vendor · tool · what it would do for this task · writes or
   read-only · `/design-tools:<command>`. Mark the recommended subset. Whole-vendor options last, as
   single entries, with their cost. Three to eight lines; not the whole index.
4. **Select** — `AskUserQuestion`, multi-select, recommended subset pre-marked; accept typed names too.
   Warn before the question if two orchestrator-class entries are on the list together.
5. **Compose** — `bash "${CLAUDE_PLUGIN_ROOT}/scripts/compose.sh" <selected tools…> --task "<the words>"`.
   Fill **every** `<angle-bracket>` placeholder in the skeleton: title, task restated with
   assumptions, target paths, one *Role in this task* per tool, the verification step.
6. **Write** the filled prompt to the `write_to:` path compose printed (`.design-tools/<slug>.prompt.md`
   in the project). Show the path and the ordered tool list. If compose printed `missing:`, say which
   tools will be skipped and give each one's install line from `wiki/tools/<tool>.md`.
7. **Offer** — "Run it now in this session, or stop here?" If yes: proceed exactly as
   `/design-tools:run <path>` would — load each tool as its `Load:` line says (`skill` → Skill tool by
   name; `read` → Read and follow, base first), follow the procedure, report in the prompt's format.
   If no: stop; the file is the deliverable.

Nothing runs before the user has selected, and nothing runs after the prompt is written unless the
user says so.
