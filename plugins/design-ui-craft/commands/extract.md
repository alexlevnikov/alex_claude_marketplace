---
description: "ui-craft by educlopez · extract — Pulls repeated markup into reusable components and tokens."
argument-hint: "[цель или файл] [инструкции]"
---

# design-ui-craft:extract

Запрос: **$ARGUMENTS**

Если аргументов нет, прочитай `${CLAUDE_PLUGIN_ROOT}/OVERVIEW.md`, дай краткий обзор пакета и несколько примеров прямого вызова. Не запускай работу над проектом.

Если цель указана:

Контракт вендора: Every lens opens by asking to read `ui-craft/SKILL.md` first — let it. A lens without its base loses the anti-slop rules, the knobs, and the Craft Report format. The resolver prints the base path for you.

1. Сначала прочитай `${CLAUDE_PLUGIN_ROOT}/vendors/ui-craft/SKILL.md`.
2. Прочитай `${CLAUDE_PLUGIN_ROOT}/vendors/extract/SKILL.md` и выполни его процедуру для запроса.

Относительные ссылки разрешай из папки исходного скилла.
