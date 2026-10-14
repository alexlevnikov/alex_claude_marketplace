---
description: Run a prompt written by /design-tools:discover — loads the selected tools exactly as the prompt says and executes its procedure
argument-hint: "[path to .design-tools/<slug>.prompt.md — default: the newest]"
allowed-tools: Bash(ls:*), Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh:*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh":*), Bash(find:*), Read
---

Run a design-tools prompt: **$ARGUMENTS**

## Prompts on disk (newest first)

!`ls -t .design-tools/*.prompt.md 2>/dev/null | head -8 || echo "(no .design-tools/*.prompt.md in this directory)"`

## Do

1. **Pick the file.** The argument if given; otherwise the newest listed above. If there is none,
   say so and point at `/design-tools:discover`. Read it whole.
2. **Honour the prompt as written.** Its *Task*, *Context*, *Tools in order*, *Procedure*,
   *Guardrails* and *Report* are the contract; do not re-rank, add or swap tools. If something in it
   is impossible now (a target file gone, a brand contract moved), say so and stop.
3. **Load each tool as its `Load:` line says**, in the listed order, when its turn comes:
   - `skill · <path>` → the Skill tool by name, with the tool's Role as the request.
   - `read · <path>` → Read the file and follow it as if invoked; if a `base first:` path is given,
     Read that first. Relative `references/` resolve against the file's directory.
   - `MISSING` → do not run, do not improvise; record it as skipped in the report. If you believe it
     may have been installed since, re-resolve once:
     `bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve.sh" <tool>` — and use the new path only if it says OK.
4. **Read-only tools first**, their findings carried into the writes; the brand contract and project
   memory re-read between write tools; an orchestrator-class tool runs as its vendor designed it.
5. **Verify** as the prompt's step 4 says, then **report** in the prompt's format: one line per file
   changed, findings from the read-only tools, what was not done and why.
