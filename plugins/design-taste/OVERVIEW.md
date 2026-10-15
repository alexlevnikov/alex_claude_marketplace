# taste-skill by Leonxlnx — design-taste

Арт-дирекшн публичных сайтов: выбор выразительного визуального направления, сборка страницы и проверка рендера в браузере.

**Как работает.** Основной design-taste-frontend v2 изучает контекст, предлагает направления, реализует выбранное и инспектирует страницу. Остальные скиллы отвечают за визуальные стили, изображения и передачу макета.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-taste:overview` или `/design-taste:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-taste:design-taste-frontend` или `$design-taste:design-taste-frontend` — сделать выразительный лендинг.
- `/design-taste:brandkit` или `$design-taste:brandkit` — собрать базовую визуальную систему бренда.
- `/design-taste:image-to-code` или `$design-taste:image-to-code` — воссоздать страницу по референсу.
- `/design-taste:redesign-existing-projects` или `$design-taste:redesign-existing-projects` — переработать существующий публичный сайт.
- `/design-taste:stitch-design-taste` или `$design-taste:stitch-design-taste` — подготовить работу через Google Stitch.

**Ограничения.** Основной сценарий рассчитан на публичные страницы, а не дашборды. Для v2 нужны Node 22+ и Chromium; imagegen-сценариям нужен инструмент генерации изображений.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `design-taste-frontend` | `/design-taste:design-taste-frontend` | `$design-taste:design-taste-frontend` | Deals researched website art directions from its bundled library, builds the chosen direction, and inspects rendered output in a browser. |
| `design-taste-frontend-v1` | `/design-taste:design-taste-frontend-v1` | `$design-taste:design-taste-frontend-v1` | Original taste-skill v1, kept for projects that need its earlier behavior. |
| `gpt-taste` | `/design-taste:gpt-taste` | `$design-taste:gpt-taste` | taste-skill variant tuned for GPT-style output. |
| `high-end-visual-design` | `/design-taste:high-end-visual-design` | `$design-taste:high-end-visual-design` | Makes an existing surface read as expensive: shadows, cards, spacing, 'absolute zero' anti-patterns. |
| `brandkit` | `/design-taste:brandkit` | `$design-taste:brandkit` | Generates brand identity boards and logo systems; needs an image tool. |
| `imagegen-frontend-web` | `/design-taste:imagegen-frontend-web` | `$design-taste:imagegen-frontend-web` | Generates one horizontal reference image per section of a web surface before any code. |
| `imagegen-frontend-mobile` | `/design-taste:imagegen-frontend-mobile` | `$design-taste:imagegen-frontend-mobile` | Generates reference imagery for mobile screens before any code. |
| `image-to-code` | `/design-taste:image-to-code` | `$design-taste:image-to-code` | Generates a visual reference, analyses it, then codes the UI from it; tuned for Codex. |
| `full-output-enforcement` | `/design-taste:full-output-enforcement` | `$design-taste:full-output-enforcement` | Modifier: bans placeholders, ellipses and truncated output in whatever the next tool writes. |
| `minimalist-ui` | `/design-taste:minimalist-ui` | `$design-taste:minimalist-ui` | Direction preset: minimalist UI. |
| `industrial-brutalist-ui` | `/design-taste:industrial-brutalist-ui` | `$design-taste:industrial-brutalist-ui` | Direction preset: industrial-brutalist UI. |
| `redesign-existing-projects` | `/design-taste:redesign-existing-projects` | `$design-taste:redesign-existing-projects` | taste-skill's redesign protocol for an existing project. |
| `stitch-design-taste` | `/design-taste:stitch-design-taste` | `$design-taste:stitch-design-taste` | taste-skill tuned for Google Stitch handoff. |
