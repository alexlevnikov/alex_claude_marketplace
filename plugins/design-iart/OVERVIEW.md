# iart-ai web-animation — design-iart

Девять технических рецептов веб-анимации: GSAP, SVG, Lottie playback, переходы, микровзаимодействия и 60fps.

**Как работает.** Выберите конкретную технику после решения о том, какое движение нужно. Каждый скилл ведёт реализацию своего типа эффекта.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-iart:overview` или `/design-iart:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-iart:gsap-web` или `$design-iart:gsap-web` — сделать эффект на GSAP/ScrollTrigger.
- `/design-iart:accessible-animation` или `$design-iart:accessible-animation` — добавить reduced-motion.
- `/design-iart:lottie-animation` или `$design-iart:lottie-animation` — встроить и управлять Lottie.
- `/design-iart:60fps-animation` или `$design-iart:60fps-animation` — исправить производительность эффекта.

**Ограничения.** Это рецепты реализации, а не арт-дирекшн. Lottie здесь означает интеграцию и playback; отдельный LottieFiles-пакет помогает спроектировать движение.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `60fps-animation` | `/design-iart:60fps-animation` | `$design-iart:60fps-animation` | Makes janky CSS animation hit 60fps. |
| `accessible-animation` | `/design-iart:accessible-animation` | `$design-iart:accessible-animation` | Honours prefers-reduced-motion with accessible motion patterns. |
| `ascii-animation` | `/design-iart:ascii-animation` | `$design-iart:ascii-animation` | ASCII and text-based animation effects. |
| `glassmorphism` | `/design-iart:glassmorphism` | `$design-iart:glassmorphism` | Frosted-glass surfaces done right. |
| `gsap-web` | `/design-iart:gsap-web` | `$design-iart:gsap-web` | GSAP recipes: ScrollTrigger, pinning, scrub, SplitText, Flip, Lenis. |
| `lottie-animation` | `/design-iart:lottie-animation` | `$design-iart:lottie-animation` | Embeds and controls Lottie animations. |
| `micro-interaction` | `/design-iart:micro-interaction` | `$design-iart:micro-interaction` | Micro-interaction recipes: hover, press, toggle, feedback. |
| `page-transition-animation` | `/design-iart:page-transition-animation` | `$design-iart:page-transition-animation` | Page and view transitions. |
| `svg-animation` | `/design-iart:svg-animation` | `$design-iart:svg-animation` | SVG path, morph and line-drawing animation. |
