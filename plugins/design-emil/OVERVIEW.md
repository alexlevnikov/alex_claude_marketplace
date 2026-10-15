# Emil Kowalski — design-emil

Набор из девяти скиллов Эмиля Ковальски про ощущение компонентов, жесты, пружины и осмысленную анимацию.

**Как работает.** Единого master-скилла нет. Выберите конкретный скилл для анализа, правки или прототипа; review-animations и prototype запускаются только по явному запросу.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-emil:overview` или `/design-emil:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-emil:emil-design-eng` или `$design-emil:emil-design-eng` — настроить жест и пружину компонента.
- `/design-emil:find-animation-opportunities` или `$design-emil:find-animation-opportunities` — найти места для анимации.
- `/design-emil:review-animations` или `$design-emil:review-animations` — проверить существующий motion без правок.
- `/design-emil:animation-vocabulary` или `$design-emil:animation-vocabulary` — назвать описанный эффект.

**Ограничения.** Работа с ощущением движения, а не диагностика производительности кадров; prototype может построить несколько вариантов.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `emil-design-eng` | `/design-emil:emil-design-eng` | `$design-emil:emil-design-eng` | Polishes how a component feels: springs, interruptibility, the invisible details — Emil Kowalski's bar. |
| `apple-design` | `/design-emil:apple-design` | `$design-emil:apple-design` | Direct-manipulation motion: drag, swipe, sheets, velocity handoff, momentum, interruptibility. |
| `find-animation-opportunities` | `/design-emil:find-animation-opportunities` | `$design-emil:find-animation-opportunities` | Read-only: finds where motion is missing but earned, and proposes it. |
| `improve-animations` | `/design-emil:improve-animations` | `$design-emil:improve-animations` | Read-only: audits all existing motion and writes a plan for other agents. |
| `review-animations` | `/design-emil:review-animations` | `$design-emil:review-animations` | Read-only review of animation code against Emil's craft bar; defaults to flagging. |
| `animation-vocabulary` | `/design-emil:animation-vocabulary` | `$design-emil:animation-vocabulary` | Reverse dictionary: describe an effect, get its name and a reference. |
| `pick-ui-library` | `/design-emil:pick-ui-library` | `$design-emil:pick-ui-library` | Recommends a UI component library for your stack. |
| `ask-sonner` | `/design-emil:ask-sonner` | `$design-emil:ask-sonner` | Answers questions about the Sonner toast library. |
| `prototype` | `/design-emil:prototype` | `$design-emil:prototype` | Builds several genuinely different versions of one UI piece behind a live picker; promote the winner. |
