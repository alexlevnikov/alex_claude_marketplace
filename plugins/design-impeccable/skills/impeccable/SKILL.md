---
name: impeccable
description: "Use impeccable by pbakaus skill impeccable for high-variance art direction (DESIGN_VARIANCE ≥ 7) with internal modes: shape · audit|critique · animate|bolder|colorize|delight|layout|overdrive|quieter|typeset · adapt|clarify|distill · harden|onboard|optimize|polish · init|document|extract|live"
---

# impeccable

Если пользователь вызвал навык без цели, файла и инструкций, прочитай `../../OVERVIEW.md` и дай короткий обзор возможностей, прямых вызовов и примеров применения. Ничего не запускай и не меняй.

При конкретной задаче этот вендорский скилл уже выбран:

Контракт вендора: Orchestrator. Give it its own context. Run the launcher at the absolute `<dir>/scripts/impeccable` path returned by the resolver; project-relative `.claude/skills/impeccable` paths in the upstream text need that substitution.

Для Impeccable запускай launcher из абсолютного пути к `../../vendors/impeccable/scripts/impeccable` при cwd проекта; не используй относительный `.claude/skills/impeccable` путь.

1. Прочитай `../../vendors/impeccable/SKILL.md` и следуй процедуре для указанной пользователем цели.

Относительные ссылки исходного скилла разрешай из его папки в `../../vendors/`. Slash-команды в исходном тексте относятся к Claude Code, не к Codex. Полный каталог пакета: `../../OVERVIEW.md`.
