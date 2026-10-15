# cloudai-x threejs — design-threejs

Десять технических справочников по vanilla Three.js: сцена, модели, материалы, свет, шейдеры, геометрия, текстуры, анимация, ввод и постобработка.

**Как работает.** Единого master-дизайнера нет. Выберите одну техническую задачу и соответствующий скилл.

**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. Не запускай скилл и не меняй проект без конкретной задачи.

**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. Для обзора: `$design-threejs:overview` или `/design-threejs:overview`. Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.

**Примеры задач:**

- `/design-threejs:threejs-fundamentals` или `$design-threejs:threejs-fundamentals` — собрать renderer, сцену и камеру.
- `/design-threejs:threejs-loaders` или `$design-threejs:threejs-loaders` — загрузить GLTF-модель.
- `/design-threejs:threejs-interaction` или `$design-threejs:threejs-interaction` — добавить raycast picking.
- `/design-threejs:threejs-postprocessing` или `$design-threejs:threejs-postprocessing` — включить bloom.

**Ограничения.** Ориентирован на vanilla Three.js и не определяет визуальный стиль страницы.

## Все отдельные скиллы

Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. Для запуска добавьте цель или файл после команды/навыка.

| Скилл | Команда Claude Code | Навык Codex | Применение |
| --- | --- | --- | --- |
| `threejs-fundamentals` | `/design-threejs:threejs-fundamentals` | `$design-threejs:threejs-fundamentals` | Three.js scene setup: cameras, renderer, Object3D hierarchy, coordinates. |
| `threejs-loaders` | `/design-threejs:threejs-loaders` | `$design-threejs:threejs-loaders` | Three.js asset loading: GLTF / OBJ / textures, pipelines, progress. |
| `threejs-materials` | `/design-threejs:threejs-materials` | `$design-threejs:threejs-materials` | Three.js materials and PBR. |
| `threejs-lighting` | `/design-threejs:threejs-lighting` | `$design-threejs:threejs-lighting` | Three.js lights, shadows, environment maps. |
| `threejs-shaders` | `/design-threejs:threejs-shaders` | `$design-threejs:threejs-shaders` | Three.js GLSL and ShaderMaterial. |
| `threejs-geometry` | `/design-threejs:threejs-geometry` | `$design-threejs:threejs-geometry` | Three.js geometries, buffers, instancing. |
| `threejs-textures` | `/design-threejs:threejs-textures` | `$design-threejs:threejs-textures` | Three.js textures, UVs, mapping. |
| `threejs-animation` | `/design-threejs:threejs-animation` | `$design-threejs:threejs-animation` | Three.js animation mixer, clips, keyframes. |
| `threejs-interaction` | `/design-threejs:threejs-interaction` | `$design-threejs:threejs-interaction` | Three.js raycasting, controls, pointer events. |
| `threejs-postprocessing` | `/design-threejs:threejs-postprocessing` | `$design-threejs:threejs-postprocessing` | Three.js EffectComposer passes: bloom, depth of field and more. |
