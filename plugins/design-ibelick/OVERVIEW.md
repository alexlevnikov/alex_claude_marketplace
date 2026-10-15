# ui-skills by ibelick — design-ibelick

Три коротких практических скилла для базовой чистоты UI, доступности и скорости анимации.

**Как работает.** Выберите один точечный скилл по известной проблеме; это быстрые проверки и исправления конкретного компонента.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-ibelick:overview` или `/design-ibelick:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-ibelick:baseline-ui` или `$design-ibelick:baseline-ui` — выровнять отступы и визуальную консистентность.
- `/design-ibelick:fixing-accessibility` или `$design-ibelick:fixing-accessibility` — исправить фокус или подписи.
- `/design-ibelick:fixing-motion-performance` или `$design-ibelick:fixing-motion-performance` — убрать рывки анимации.

**Ограничения.** Для широкого аудита WCAG и метрик лучше подходит пакет Osmani.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `baseline-ui` | `/design-ibelick:baseline-ui` | `$design-ibelick:baseline-ui` | Reviews a named UI file against its baseline, or applies the baseline during requested UI implementation. |
| `fixing-accessibility` | `/design-ibelick:fixing-accessibility` | `$design-ibelick:fixing-accessibility` | Fast targeted accessibility fixes: focus ring, tab order, labels, ARIA. |
| `fixing-motion-performance` | `/design-ibelick:fixing-motion-performance` | `$design-ibelick:fixing-motion-performance` | Fixes janky animation: compositor-only properties, layout thrash, reduced-motion, perf budget. |
