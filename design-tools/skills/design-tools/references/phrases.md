# Phrases

The user's words → the tool they usually mean, in the phrasing people actually use, English and
Russian. Since 0.4.0 this is **not a route**: `scripts/discover.py` reads these rows as one input to
its lexical pre-rank, and the discovery skill reads them as a hint when it ranks candidates. A row
here raises a tool's score; it never decides alone.

Where a row lands on accessibility, performance, motion, polish, or review, **read `collisions.md`**
— those five are contested by two or three vendors each, and discovery must say which and why.

## Look

| They say | Tool |
|---|---|
| "the headings are enormous" · «заголовки огромные» · "typography is off" · «типографика поехала» | `typeset` |
| "the colours are wrong" · «цвета не те» · "dark mode looks broken" · «тёмная тема сломана» | `colorize` |
| "it falls apart on mobile" · «на телефоне разъезжается» · "check the breakpoints" | `adapt` |
| "too busy" · «слишком много всего» · "there's too much on this page" | `distill` |
| "it's bland" · «пресно, добавь характера» · "give it some personality" | `bolder` |
| "too loud" · «слишком кричаще» · «сделай спокойнее» · "tone it down" | `quieter` |
| "this markup repeats everywhere" · «одно и то же копипастится» | `extract` |
| "it should feel more expensive" · «должно выглядеть дороже» | `high-end-visual-design` |
| "sketch this new section before we build it" · «набросай секцию» | `shape` |
| "final finish pass" · «финальная полировка» · "it's right, now make it finished" | `polish` |

## Feel

| They say | Tool |
|---|---|
| "add some motion" · «оживи страницу» · "it feels static" | `find-animation-opportunities` (R) → `motion-design` (W) |
| "the timing feels wrong" · «анимация не та по ощущению» | `motion-design` |
| "this component feels cheap" · «компонент ощущается дёшево» | `emil-design-eng` |
| "the drawer should follow my finger" · «свайп должен тянуться за пальцем» | `apple-design` |
| "it stutters" · «дёргается» · "janky" · «лагает при скролле» | `fixing-motion-performance` |
| "add a nice touch on hover" · «микро-взаимодействие на ховер» | `delight` |
| "audit all the animation in here" · «отревьюй весь моушн» | `improve-animations` (R) |
| "I want to see the motion review" · «хочу посмотреть отчёт по анимации» | `design-motion-principles` (audit mode) |
| "what's it called when a popover pops" · «как называется этот эффект» | `animation-vocabulary` |

## Fix

| They say | Tool |
|---|---|
| "what if there's no data" · «а если данных нет» · "empty state" · «пустое состояние» | `unhappy` |
| "is this production ready" · «готово к проду?» · "what about errors and loading" | `harden` |
| "the error message is useless" · «текст ошибки бессмысленный» · "rewrite the empty state copy" | `clarify` |
| "keyboard navigation is broken" · «с клавиатуры не работает» · "focus ring missing" | `fixing-accessibility` |
| "run an accessibility audit" · «проверь доступность» · "WCAG compliance" | `accessibility` |
| "LCP is bad" · "fix CLS" · «плохие Core Web Vitals» | `core-web-vitals` |
| "the page is heavy" · «страница медленно грузится» · "too many requests" | `performance` |
| "we don't rank" · «нас не находят в поиске» · "add structured data" · «микроразметка» | `seo` |
| "security headers" · «проверь безопасность» · "is this code modern" | `best-practices` |

## Judge

| They say | Tool |
|---|---|
| "what would you change" · «что скажешь по этой странице» | `critique` |
| "score it" · «оцени по десятибалльной» · "give me a PM-ready audit" | `heuristic` |
| "check a11y while we build" · «проверь доступность по ходу» | `audit` |
| "run lighthouse" · «прогони полный аудит качества» | `web-quality-audit` |
| "can I merge this" · «можно мержить?» · "is it done" · «это готово?» | `finalize` |
| "review this diff properly" · «отревьюй дифф» | `ui-craft:design-reviewer` + `ui-craft:a11y-auditor` |
| "review this animation code" · «отревьюй код анимации» · "is this motion up to standard" | `review-animations` |

## Escalate — not this plugin

| They say | Route |
|---|---|
| "build the product page" · «собери страницу товара» | `design-pipeline` |
| "redesign the homepage" · «переделай главную» | `design-pipeline` |
| "make it look completely different" · «сделай совсем другой вид» | `design-pipeline` |
| "we need a landing for the campaign" · «нужен лендинг» | `design-pipeline` |

## Named outright — do not route, engage

"run impeccable on the hero" · «прогони impeccable» · "use typeset here" · «возьми typeset» — the
user has chosen. `/design-tools:<vendor>-<tool>` — or `/design-tools:<vendor>` for the vendor's master
skill run as designed — or the same resolve-and-load by hand (`loading.md`). The
only check left is the orchestrator one: a second orchestrator in this context is still a no.

## Ask, do not route

"make it better" · «сделай красиво» · "improve this" · «улучши» · "make it pop" — one clarifying
question: which aspect is wrong — the type, the colour, the layout, the motion, or the copy?
