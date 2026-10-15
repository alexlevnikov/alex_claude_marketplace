---
description: "impeccable by pbakaus · impeccable — pbakaus's design director with internal modes — shape, audit, critique, typeset, colorize, polish, harden, live and more."
argument-hint: "[цель или файл] [инструкции]"
---

# design-impeccable:impeccable

Запрос: **$ARGUMENTS**

Если аргументов нет, прочитай `${CLAUDE_PLUGIN_ROOT}/OVERVIEW.md`, дай краткий обзор пакета и несколько примеров прямого вызова. Не запускай работу над проектом.

Если цель указана:

Контракт вендора: Orchestrator. Give it its own context. Run the launcher at the absolute `<dir>/scripts/impeccable` path returned by the resolver; project-relative `.claude/skills/impeccable` paths in the upstream text need that substitution.

1. Прочитай `${CLAUDE_PLUGIN_ROOT}/vendors/impeccable/SKILL.md` и выполни его процедуру для запроса.

Относительные ссылки разрешай из папки исходного скилла.
