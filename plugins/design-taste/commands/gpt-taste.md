---
description: "taste-skill by Leonxlnx · gpt-taste — taste-skill variant tuned for GPT-style output."
argument-hint: "[цель или файл] [инструкции]"
---

# design-taste:gpt-taste

Запрос: **$ARGUMENTS**

Если аргументов нет, прочитай `${CLAUDE_PLUGIN_ROOT}/OVERVIEW.md`, дай краткий обзор пакета и несколько примеров прямого вызова. Не запускай работу над проектом.

Если цель указана:

Контракт вендора: Orchestrator-class skills here want a context of their own. Image-generation skills need an image tool in the session.

1. Прочитай `${CLAUDE_PLUGIN_ROOT}/vendors/gpt-taste/SKILL.md` и выполни его процедуру для запроса.

Относительные ссылки разрешай из папки исходного скилла.
