# ui-craft by educlopez — design-ui-craft

Система проектирования веб-интерфейсов: базовые правила, бриф, токены, этапы, точечные улучшения и оценка результата.

**Как работает.** Базовый ui-craft задаёт правила и формат результата; узкие скиллы сначала читают базу. Этапы brief/tokens/shape/craft могут вести диалог и записывать .ui-craft/brief.md и .ui-craft/spec.md.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-ui-craft:overview` или `/design-ui-craft:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-ui-craft:ui-craft` или `$design-ui-craft:ui-craft` — создать или переработать конкретный экран.
- `/design-ui-craft:start` или `$design-ui-craft:start` — выбрать следующий этап.
- `/design-ui-craft:typeset` или `$design-ui-craft:typeset` — исправить типографику существующего интерфейса.
- `/design-ui-craft:unhappy` или `$design-ui-craft:unhappy` — проработать ошибки, пустые и крайние состояния.
- `/design-ui-craft:critique` или `$design-ui-craft:critique` — получить оценку без правок.

**Ограничения.** Ориентирован на веб-интерфейсы; некоторые этапы интерактивны. Визуальные пресеты уступают существующему бренд-контракту.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `ui-craft` | `/design-ui-craft:ui-craft` | `$design-ui-craft:ui-craft` | The ui-craft base: discovery, anti-slop rules, knobs and Craft Report; actions build \| animate \| review \| polish \| audit. |
| `ui-craft-minimal` | `/design-ui-craft:ui-craft-minimal` | `$design-ui-craft:ui-craft-minimal` | ui-craft base with a minimal, whitespace-led aesthetic fixed in. |
| `ui-craft-editorial` | `/design-ui-craft:ui-craft-editorial` | `$design-ui-craft:ui-craft-editorial` | ui-craft base with an editorial, type-led aesthetic fixed in. |
| `ui-craft-dense-dashboard` | `/design-ui-craft:ui-craft-dense-dashboard` | `$design-ui-craft:ui-craft-dense-dashboard` | ui-craft base tuned for dense data dashboards and tables. |
| `start` | `/design-ui-craft:start` | `$design-ui-craft:start` | Explains the ui-craft ladder and names your next rung; changes nothing. |
| `brief` | `/design-ui-craft:brief` | `$design-ui-craft:brief` | Interviews you and writes .ui-craft/brief.md — purpose, user, principles, success metric, out of scope. |
| `tokens` | `/design-ui-craft:tokens` | `$design-ui-craft:tokens` | Establishes or audits the three-layer design-token spine (primitive → semantic → component). |
| `shape` | `/design-ui-craft:shape` | `$design-ui-craft:shape` | Wireframes one new section into .ui-craft/spec.md — layout, state lattice, acceptance bar; writes a spec, not code. |
| `craft` | `/design-ui-craft:craft` | `$design-ui-craft:craft` | Builds a surface from the spec with ui-craft recipes (dashboard, landing, auth). |
| `sddesign` | `/design-ui-craft:sddesign` | `$design-ui-craft:sddesign` | ui-craft's six-gate conveyor for one surface: brief → tokens → shape → craft → converge → ship. |
| `finalize` | `/design-ui-craft:finalize` | `$design-ui-craft:finalize` | Ship gate: READY / NOT READY / BLOCKED with findings; never edits. |
| `remember` | `/design-ui-craft:remember` | `$design-ui-craft:remember` | Appends a learned design constraint to .ui-craft/brief.md §6 so future sessions obey it. |
| `polish` | `/design-ui-craft:polish` | `$design-ui-craft:polish` | Final finish pass on a surface that is already right: alignment, spacing, micro-details, using project tokens. |
| `typeset` | `/design-ui-craft:typeset` | `$design-ui-craft:typeset` | Retunes the typography of existing UI: modular scale, tracking, leading, weight hierarchy, micro-typography. |
| `colorize` | `/design-ui-craft:colorize` | `$design-ui-craft:colorize` | Applies and tunes colour on existing UI: palette use, theming, dark mode, accent budget. |
| `adapt` | `/design-ui-craft:adapt` | `$design-ui-craft:adapt` | Makes an existing layout responsive: breakpoints, touch targets, safe areas, fluid type, container queries. |
| `distill` | `/design-ui-craft:distill` | `$design-ui-craft:distill` | Removes noise from an over-built surface: cuts sections, elements and decoration that earn nothing. |
| `bolder` | `/design-ui-craft:bolder` | `$design-ui-craft:bolder` | Amplifies personality inside the current direction: stronger type, contrast, signature details. |
| `quieter` | `/design-ui-craft:quieter` | `$design-ui-craft:quieter` | Tones a loud surface down: fewer accents, calmer type and motion, more whitespace. |
| `extract` | `/design-ui-craft:extract` | `$design-ui-craft:extract` | Pulls repeated markup into reusable components and tokens. |
| `redesign` | `/design-ui-craft:redesign` | `$design-ui-craft:redesign` | ui-craft's redesign lens: re-composes an existing surface against the brief and tokens. |
| `delight` | `/design-ui-craft:delight` | `$design-ui-craft:delight` | Adds purposeful micro-interactions — hover, press, success moments — within the motion tokens. |
| `animate` | `/design-ui-craft:animate` | `$design-ui-craft:animate` | Adds or adjusts animation inside the project's motion token system (durations, easings, intensity). |
| `unhappy` | `/design-ui-craft:unhappy` | `$design-ui-craft:unhappy` | Designs the non-happy states first — empty, loading, error, partial — and turns boolean soup into a state machine. |
| `harden` | `/design-ui-craft:harden` | `$design-ui-craft:harden` | Production-hardens a surface: skeletons, empty/error/partial states, i18n, offline, permissions, first run. |
| `clarify` | `/design-ui-craft:clarify` | `$design-ui-craft:clarify` | Rewrites UX copy: error messages, empty states, CTAs, voice matrix, reading level. |
| `audit` | `/design-ui-craft:audit` | `$design-ui-craft:audit` | Technical accessibility audit inside a build session: contrast, focus, ARIA, keyboard; report only. |
| `critique` | `/design-ui-craft:critique` | `$design-ui-craft:critique` | UX critique of a surface — what to change and why; no code changes. |
| `heuristic` | `/design-ui-craft:heuristic` | `$design-ui-craft:heuristic` | Scores a surface 0–100 against heuristics and personas; PM-ready audit, read-only. |
