# kylezantos — design-motion-principles

Проектирование или аудит UI-motion через подходы Emil Kowalski, Jakub Krehel и Jhey Tompkins.

**Как работает.** Один скилл design-motion-principles выбирает режим Create или Audit. Audit обычно создаёт HTML-отчёт с зацикленными демонстрациями; флаги --terminal, --inline и --no-html меняют вывод.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-motion-principles:overview` или `/design-motion-principles:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-motion-principles:design-motion-principles` или `$design-motion-principles:design-motion-principles` — создать полезный hover-переход.
- `/design-motion-principles:design-motion-principles` или `$design-motion-principles:design-motion-principles` — провести audit motion страницы --terminal.

**Ограничения.** При неясном запросе требуется выбрать Create или Audit; аудит по умолчанию пишет HTML-файл.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `design-motion-principles` | `/design-motion-principles:design-motion-principles` | `$design-motion-principles:design-motion-principles` | Builds motion or audits it with Emil / Krehel / Tompkins lenses; audit emits an HTML report with looping demos. |
