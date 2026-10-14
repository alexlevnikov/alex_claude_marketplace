---
name: design-tools
description: >
  Use for a design task on existing UI or an explicit design-tools vendor selection such as
  design-tools:ui-craft:typeset or design-tools:ui-craft. Discover suitable skills when the user
  describes a problem without naming a tool; resolve and run the selected bundled vendor skill
  when the user names one. Use design-pipeline for a whole new surface.
metadata:
  version: "0.6.0"
---

# Design Tools — discovery

Eighty-seven design skills are in the set. A real request is rarely one of them: "looks cheap and
slow on mobile" is a taste pass, a responsive pass and a performance pass, from two or three vendors
— or one orchestrator that does all of it its own way. Guessing the one right tool was the old
router's job and its weakness. This skill does not guess. It runs the request through the whole set,
shows the candidates, lets the owner choose, and writes the prompt that uses the choice.

An explicit vendor or skill name is the user's selection. Run that route directly. For an unnamed
task, discover candidates and let the user pick before running them.

## Explicit invocation

- **Claude Code:** `/design-tools:<vendor>:<skill> <task>` runs one selected skill;
  `/design-tools:<vendor> <task>` runs that vendor's master skill, or lists its choices when it has
  no master. The native command files are under `commands/<vendor>/<skill>.md` and `commands/<vendor>.md`.
- **Codex:** invoke `$design-tools:design-tools` with `<vendor>:<skill> <task>` or `<vendor> <task>`.
  The same selector can be written as `design-tools:<vendor>:<skill>` in a normal request.
- Locate the installed plugin root from this `SKILL.md`, then run
  `python3 <plugin-root>/scripts/invoke.py <vendor>[:<skill>]`. Check that the vendor and skill
  exist. A vendor with no master returns a list; ask the user to choose a skill. Otherwise read
  the returned `skill:` file, reading `base:` first when present, and follow the vendor's own
  procedure with the user's task. Resolve its relative resources against `dir:`. Stop if it says
  `MISSING`; do not substitute a skill from memory.
- The explicit selection needs no discovery or second selection question. Follow the user's
  requested scope, the project's brand contract, and the selected skill's instructions. Report
  what the selected skill did and any missing runtime dependencies.

## The flow

1. **Understand the need.** From the user's words, fix three things before ranking: *what* is wrong
   or wanted (aspect: type, colour, layout, motion, states, copy, a11y, perf, SEO, judgement);
   *where* (files, URL, component — ask if nothing is named and it matters); *scope* (one component
   ↔ one surface ↔ a new surface). A new surface is `design-pipeline` — say so and stop.
2. **Run it through the set.** Locate this plugin's root from this `SKILL.md`, then run
   `bash <plugin-root>/scripts/discover.sh "<the words>"`. In a Claude plugin command,
   `${CLAUDE_PLUGIN_ROOT}` is the root. It
   prints a lexical pre-rank (a hint with the matched terms shown), the whole-vendor options, and the
   index of every tool — vendor · tool · mode · class · what it does · the skill's own trigger phrases.
   Read the **whole index**, not just the pre-rank: the pre-rank sees words, you see meaning.
3. **Judge.** Rank candidates by fit to the need. Where two candidates cover the same ground,
   `references/collisions.md` has the discriminator — name it in the list ("`accessibility` for the
   compliance question, `fixing-accessibility` if it is really just the focus rings"). Where an
   orchestrator alone would do the job, list it as a whole-vendor option (`impeccable alone`,
   `ui-craft alone`) and say what it costs: own context, own flow, higher effort for
   impeccable. `references/catalog.md` says what each routable tool is *not* for.
4. **Present.** A ranked list. Each line: vendor · tool · **what it would do for this task** (not its
   generic blurb) · writes / read-only · `/design-tools:<command>`. Mark a recommended subset. Keep it
   to the candidates that genuinely fit — eight is a long list, three is common. Whole-vendor options
   at the end, as single entries. Reading order for the final prompt is read-only → writes, so say
   which are which.
5. **Select.** Ask the user to choose from the ranked list using the available question channel,
   with the recommended subset marked. The user may also
   type names. Two orchestrators in one selection is refused at compose time — warn before, not after.
6. **Compose.** `bash <plugin-root>/scripts/compose.sh <tools…> --task "<the words>"`. It
   prints the prompt skeleton: tools in the right order with **resolved** `Load:` lines (the absolute
   SKILL.md, ui-craft base first, `MISSING` when the bundle is incomplete), brand-contract and
   project-memory paths, guardrails, report format — and every place needing judgement as an
   `<angle-bracket>` placeholder. Fill every placeholder: the title, the task restated with its
   assumptions, the target paths, one *Role in this task* sentence per tool, the verification step.
   Nothing in angle brackets may survive into the file.
7. **Write.** The filled prompt to the `write_to:` path compose printed — `.design-tools/<slug>.prompt.md`
   in the project. Show the user the path and the tool list. If compose reported `missing:`, say so
   now: the prompt is written, those tools will be skipped; repair the plugin before running.
8. **Offer.** "Run it now in this session, or stop here?" Running is `/design-tools:run <path>` —
   load each tool exactly as its `Load:` line says, follow the procedure, report in the format.
   Do not start it unasked.

## What "load" means

A name is not a skill until its text is in context. `Load: skill · <path>` means the runtime's skill
invocation mechanism knows it by name (project or user scope) — invoke it. `Load: read · <path>` means Read the file and follow
it as if invoked, the `base first:` file before it for ui-craft lenses. Full procedure:
`references/loading.md`. A MISSING tool is reported as skipped, never improvised.

## Guardrails

- **Read-only before write.** Compose orders it; `run` respects it. Findings from the judges become
  the brief for the writers.
- **One orchestrator per context.** Compose refuses two. If the user insists, two prompts.
- **The brand contract outranks every vendor.** `BRAND-CONTRACT.md` (working directory, then parents)
  is written into the prompt's Context; vendors that ask "what are your brand colours / fonts /
  preferences" get it as the answer.
- **Whole surfaces are the pipeline's.** Discovery names the escalation instead of composing a
  ten-tool prompt.
- **The user picks the set.** Recommend, pre-mark, explain — then ask. There is no quiet path from
  a request to a write.

## References

- `references/phrases.md` — the owner's phrasings (EN/RU) → the tool usually meant; input to the
  pre-rank and a hint to you.
- `references/collisions.md` — twelve overlaps and their discriminators; say them out loud in the list.
- `references/catalog.md` — the routable tools, what each is and is not for.
- `references/stacking.md` — which chains are safe in one context, in which order.
- `references/loading.md` — resolve → load, and why two load modes exist.
- `wiki/` — one page per vendor and per tool; `registry/tools.json` — the set itself.
