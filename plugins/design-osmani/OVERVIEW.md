# Addy Osmani web-quality — design-osmani

Проверка качества веб-страниц по доступности, Core Web Vitals, скорости, SEO и практикам платформы.

**Как работает.** Если причина проблемы неизвестна, начните с web-quality-audit; при известной оси выберите один профильный скилл.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-osmani:overview` или `/design-osmani:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-osmani:web-quality-audit` или `$design-osmani:web-quality-audit` — найти слабую ось сайта.
- `/design-osmani:core-web-vitals` или `$design-osmani:core-web-vitals` — разобрать LCP, INP и CLS.
- `/design-osmani:accessibility` или `$design-osmani:accessibility` — проверить соответствие WCAG 2.2.
- `/design-osmani:seo` или `$design-osmani:seo` — улучшить поиск и метаданные.

**Ограничения.** Точные выводы зависят от доступных замеров браузера, Lighthouse и трасс; аудит сам по себе работает без правок.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `accessibility` | `/design-osmani:accessibility` | `$design-osmani:accessibility` | Full WCAG 2.2 accessibility pass — POUR, conformance level, fixes. |
| `core-web-vitals` | `/design-osmani:core-web-vitals` | `$design-osmani:core-web-vitals` | Diagnoses and improves LCP, INP, and CLS using field signals and browser traces when available. |
| `performance` | `/design-osmani:performance` | `$design-osmani:performance` | Cuts page weight and load time: payload, critical path, fonts, images, caching. |
| `seo` | `/design-osmani:seo` | `$design-osmani:seo` | On-page SEO: meta, structured data, sitemap, robots, headings, internal links. |
| `best-practices` | `/design-osmani:best-practices` | `$design-osmani:best-practices` | Reviews runtime and source evidence for security, compatibility, and modern platform practices. |
| `web-quality-audit` | `/design-osmani:web-quality-audit` | `$design-osmani:web-quality-audit` | Evidence-led audit of performance, accessibility, SEO, best practices, and agentic browsing; localizes findings with live browser checks. |
