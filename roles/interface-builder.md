# Interface builder

Install **`design-tools`**. Add **`browser-lab`** when the task needs live
browser inspection or visual verification. Design tools and vendor resources
come with one `design-tools` installation.

## Start

| Task | Claude Code | Codex |
| --- | --- | --- |
| Improve an existing UI | `/design-tools:discover <task>` | `$design-tools:design-tools <task>` |
| Use a named vendor skill | `/design-tools:ui-craft:typeset <task>` | `$design-tools:design-tools ui-craft:typeset <task>` |
| Build a new surface | `/design-tools:design-pipeline <task>` | `$design-tools:design-pipeline <task>` |

Use `/design-tools:<vendor>` in Claude Code or
`$design-tools:design-tools <vendor>` in Codex to run a vendor master skill or
list the vendor's skills.
The [design catalog](../plugins/design-tools/wiki/README.md) lists all vendor
choices. For a live page, use `browser-lab` to collect browser evidence and
verify the result after the design pass.

## Handoffs

The design pack owns choice of a design procedure and the code pass. The
browser pack owns interaction with a running page, console/network inspection,
and screenshots. Keep project-specific brand rules in the project, not in this
role. Record what changed and what was verified against the running page.
