---
description: Open the design-studio dashboard (or one tool's bake-off demo) in the browser, if it exists here
argument-hint: "[tool — e.g. typeset, to open its demo instead of the dashboard]"
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.sh":*), Bash(open:*)
---

# Design-studio dashboard

The bake-off dashboard is a self-contained HTML file in design-studio — every skill card, the
group-by-vendor / group-by-use-case toggle, and the per-skill demos embedded. This command opens it
(or, with a tool name, that tool's `demos/<tool>/index.html`) **only if it exists on this machine**.
It opens nothing else and changes nothing.

## Result

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.sh" --open $ARGUMENTS`

If the block above is empty or an error, `${CLAUDE_PLUGIN_ROOT}` was not substituted — find the script
and run it yourself:
`bash "$(find ~/.claude/plugins "$HOME/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/claude_plugins" -path '*design-tools/scripts/dashboard.sh' 2>/dev/null | head -1)" --open $ARGUMENTS`

## Report

- `status: OK` + `opened: yes` → say what opened (dashboard or which demo), its path, size and
  modified date, and the caveat line — the dashboard's vendor column is known-wrong for twelve
  ui-craft lenses; `wiki/` is the authority.
- `status: MISSING` → say so in one line and repeat the hint (set `DESIGN_STUDIO_DIR`, or rebuild
  with `python3 scripts/build_dashboard.py` inside design-studio). Do not try other paths.
- `opened: no` with a reason → give the path so the user can open it by hand.

The dashboard was built from `candidates/skills-dashboard.json` on the date shown; if the inventory
has changed since (`bash scripts/resolve.sh --all` disagrees with the card count), mention the
rebuild command.
