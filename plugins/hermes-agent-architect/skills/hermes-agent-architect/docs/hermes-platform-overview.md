# Hermes Agent: полный обзор возможностей и расширения

**Снимок:** 15 октября 2026 года. Официальный индекс `llms.txt` повторно получен
в этот день; его SHA-256 совпал с каталогом от 13 октября. Каталог содержит
239 уникальных страниц, 227 из них прямо сопоставлены с файлами документации
закреплённого тега `v2026.9.14`; в теге всего 457 Markdown-документов.
Закреплённый commit: `345cd2b057a452236de401d3534b8502a7465e8d`.

Этот документ — единая карта платформы и точка входа в документацию. Он
объясняет, что выбирать при проектировании бота, и содержит полный список
страниц официального индекса в приложении. Детальные схемы памяти и разбор
провайдеров вынесены в [архитектуру памяти](hermes-memory-architecture.md) и
[обзор провайдеров](hermes-memory-providers-review-2026-10-15.md). Никакая
страница сайта или файл тега не доказывает, что функция включена в конкретном
контейнере. Для работающего бота отдельно проверяются image, конфигурация,
плагины, права и фактический ответ. [Официальный индекс](https://hermes-agent.nousresearch.com/docs/llms.txt),
[закреплённый исходник](https://github.com/NousResearch/hermes-agent/tree/v2026.9.14).

## 1. Модель системы

Hermes — агентный runtime с циклом «модель → инструмент → наблюдение → модель»,
устойчивыми сессиями, инструментами, памятью и интерфейсами доставки. Для
архитектуры полезно разделять **код Hermes**, **профиль**, **сессию**, **канал**
и **сервис развёртывания**. Они обновляются и изолируются по разным правилам.
[Features Overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview),
[Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration),
[Sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions).

| Слой | Что выбирает или хранит | Типичное изменение |
| --- | --- | --- |
| Release и image | Версия ядра, встроенные инструменты и контракты расширений | Проверить tagged source; обновить образ отдельным выпуском |
| Профиль | Идентичность агента, модель и провайдер, конфигурация, навыки, память и состояние | Создать отдельный профиль для отдельного бота |
| Сессия | История конкретного разговора и его текущий контекст | `/new`, resume, поиск, модель сессии |
| Gateway и adapter | Приём/отправка сообщений на платформе, маршрутизация, авторизация | Подключить канал, webhook или свой adapter |
| Инструменты и плагины | Действия агента, lifecycle hooks и провайдеры | Настройка toolset, MCP, plugin или точечный патч |
| Внешний сервис | Секреты, mounts, сеть, процесс, расписание, health и журнал | Compose/systemd и профиль целевого бота |

**Профиль** — граница идентичности и состояния Hermes, но сам по себе не
ограничивает файловые права ОС или сетевой доступ. **Сессия** не создаёт нового
бота: она продолжает работу внутри профиля. **Bot Mode** представляет профили
как набор именованных ботов с собственными чатами и настройками; это UI и
организационный слой над профилями. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles),
[Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode),
[Multi-profile gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways).

## 2. Что доступно пользователю

| Семейство | Возможности | Начать с документации |
| --- | --- | --- |
| Интерфейсы | CLI, TUI, Desktop, web dashboard, Bot Mode; разные оболочки поверх ядра | [CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli), [TUI](https://hermes-agent.nousresearch.com/docs/user-guide/tui), [Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/desktop), [Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard) |
| Диалоги | Сессии, resume/search, персональные и проектные контексты, ссылки на файлы и diff | [Sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions), [Context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files), [Context references](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references) |
| Модели | Nous Portal и другие провайдеры, OpenAI-совместимые endpoint, локальные модели, маршрутизация и fallback | [Configuring Models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models), [Local Models](https://hermes-agent.nousresearch.com/docs/user-guide/local-models), [Model provider plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin) |
| Инструменты | Файлы, терминал, web, браузер, программные вызовы, наборы инструментов и поиск по ним | [Tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools), [Tools Reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference), [Toolsets Reference](https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference), [Tool Search](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search) |
| Доставка | Telegram и другие messaging adapters, webhooks, relay, групповые и многопрофильные схемы | [Messaging index](https://hermes-agent.nousresearch.com/docs/llms.txt), [Relay](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/relay), [Webhooks](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks) |
| Медиа и web | Vision, voice/STT/TTS, изображения, браузер, web search, извлечение документов, вложения-артефакты | [Voice](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode), [Vision](https://hermes-agent.nousresearch.com/docs/user-guide/features/vision), [Document extraction](https://hermes-agent.nousresearch.com/docs/user-guide/features/document-extraction), [Deliverable mode](https://hermes-agent.nousresearch.com/docs/user-guide/features/deliverable-mode) |
| Автоматизация | Cron, loops, heartbeat, persistent goals, delegation, Kanban, batch и hooks | [Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron), [Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation), [Kanban](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban), [Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) |
| Разработка | Git worktrees, Docker/SSH и другие terminal backends, checkpoints, LSP diagnostics, code execution | [Worktrees](https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees), [Docker backend](https://hermes-agent.nousresearch.com/docs/user-guide/docker), [Checkpoints](https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback), [LSP](https://hermes-agent.nousresearch.com/docs/user-guide/features/lsp) |

Наличие инструмента в справочнике означает, что Hermes знает его контракт.
Доступ в конкретной сессии зависит от версии, разрешённых toolsets, платформы,
настроенного backend и учётных данных. Для внешних действий отдельно проверяй
авторизацию пользователя и способ ограничения побочных эффектов.

## 3. Память: что где живёт

В Hermes слово «память» обозначает несколько разных слоёв. Смешение этих
слоёв даёт ложные ожидания: длинный лог не становится автоматически фактом о
пользователе, а векторная база не заменяет предметную БД. Подробный жизненный
цикл и параметры тега описаны в [локальном руководстве](hermes-memory-architecture.md).
[Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory),
[Which File Does What?](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what).

| Слой | Назначение | Граница |
| --- | --- | --- |
| Активный контекст | Текущие реплики и результат инструментов | Ограничен окном модели; сжатие не заменяет долговременную запись |
| `SOUL.md` и проектный контекст | Роль, стиль, правила проекта | Инструкции; не фактический архив пользователя |
| `USER.md` | Короткие устойчивые предпочтения и профиль человека | Снимок добавляется при старте сессии; сведения должны быть исправляемы |
| `MEMORY.md` | Отобранные факты и договорённости бота | Малый бюджет; не для документов и транзакций |
| `state.db` и `session_search` | История диалогов и поиск по ним | Поиск исходных сообщений; не гарантия семантического вывода |
| Skills | Повторяемые процедуры | Загружаются по мере надобности; не личные воспоминания |
| MemoryProvider plugin | Внешнее извлечение и сохранение памяти | Отдельный backend, схема данных, права и политика записи |
| Предметный источник | Финансы, задачи, CRM, документы и другие записи приложения | Источник истины для домена; агентская память может лишь ссылаться на него |

В закреплённом теге `MEMORY.md` и `USER.md` входят в системный промпт как
снимок на начало сессии. Команда памяти может сохранить изменение сразу, но
уже собранный префикс текущей сессии не переписывается. `/new` даёт новую
границу загрузки; `session_search` нужен для обращения к прошлым репликам.
В теге для штатного memory tool документированы `add`, `replace`, `remove`;
текущая страница также может описывать более новые операции. При проектировании
под `v2026.9.14` ориентируйся на tagged source.
[Tagged memory docs](https://github.com/NousResearch/hermes-agent/blob/v2026.9.14/website/docs/user-guide/features/memory.md),
[Tagged MemoryStore](https://github.com/NousResearch/hermes-agent/blob/v2026.9.14/tools/memory_tool_store.py).

Внешний провайдер нужен, когда встроенных коротких файлов и поиска сессий
недостаточно: большой корпус, смысловой recall, временные версии фактов,
межагентные связи или отдельная политика retention. Выбор начинается с
вопросов о владельце данных, источнике истины, единице записи, scope
пользователя/бота, исправлении, удалении и измеримом качестве ответа. В
[обзоре провайдеров](hermes-memory-providers-review-2026-10-15.md) разобраны
штатные интеграции, сторонние плагины и исследовательские подходы. Их список
на сайте может меняться; совместимость с образом нужно проверять отдельно.
[Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers),
[Provider plugin API](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin).

## 4. Как кастомизировать Hermes

Иди от настройки к расширению контракта, затем к изменению ядра. Выбор зависит
от того, нужна ли новая **инструкция**, **инструмент**, **источник данных**,
**транспорт** или **runtime-семантика**. [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills),
[Build a Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins).

| Механизм | Когда подходит | Что проверить |
| --- | --- | --- |
| `config.yaml`, профиль, модель, toolset | Меняется поведение уже поддерживаемых функций и доступные инструменты | Версию, значения по умолчанию, секреты вне Git, права и rollout |
| `SOUL.md`, контекст проекта | Нужны роль, стиль или правила работы с проектом | Приоритет файлов, границы доверия, отсутствие секретов |
| Skill и tap | Нужна повторяемая процедура, знание или команда с постепенной загрузкой | Формат `SKILL.md`, вызов, обновление и права на действия |
| General plugin | Нужны новый tool, hook, slash command или интеграция | `plugin.yaml`, enablement, API, ошибки и побочные эффекты |
| MCP server | Уже есть внешняя служба с инструментами | Scope и фильтрацию tools, transport, авторизацию, latency |
| Provider plugin | Нужно заменить специализированный backend: memory, model, browser, web, media, secrets или context engine | Контракт провайдера, хранение, миграцию и версию ядра |
| Platform adapter / relay | Нужен новый канал сообщений или сложная маршрутизация | Авторизация, delivery, retry, duplicate effects и владение poller |
| API server / ACP / library | Hermes вызывается из другого приложения или редактора | Точки входа, изоляцию сессий, аутентификацию и лимиты |
| Core patch / fork | Документированных точек расширения действительно недостаточно | Diff к закреплённому тегу, совместимость обновления и rollback |

### Детали расширения

- **Skills** дают агенту инструкции и поддерживающие файлы, которые он читает
  по запросу. Система допускает agent-created skills и фоновый curator для
  обзора, старения и архивации навыков. Проверяй порядок активации и право
  навыка изменять файлы. [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills),
  [Curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator).
- **Plugins** добавляют исполняемые возможности и lifecycle hooks. Read-only
  observer подходит для телеметрии; изменяющий поведение hook требует явной
  политики ошибок и доверия к входным данным. [Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins),
  [Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks),
  [Observer hooks](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks).
- **MCP** подключает инструменты внешнего сервиса через стандартный протокол.
  Для бота важны конкретные разрешённые серверы и tools, а не наличие MCP как
  флага. [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp),
  [MCP config](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference).
- **Provider plugins** позволяют заменить одну подсистему без форка ядра.
  Документация разработчика отдельно описывает memory, model, context engine,
  browser, web, image, TTS и другие интерфейсы; сверяй точный контракт тега в
  `../../upstream/hermes-agent/website/docs/developer-guide`.
  [Developer Guide index](https://hermes-agent.nousresearch.com/docs/llms.txt).
- **Dashboard, язык и внешний UX** расширяются отдельно от ядра: темы, вкладки,
  slots и backend routes dashboard, language packs, Desktop и Bot Mode. Эти
  поверхности имеют разные release и deployment требования.
  [Dashboard extension](https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard),
  [Language Packs](https://hermes-agent.nousresearch.com/docs/user-guide/features/language-packs).

## 5. Автоматизация: какой примитив выбрать

| Задача | Механизм | Граница |
| --- | --- | --- |
| Надёжный запуск по времени, включая script-only | Cron | Проверить delivery target, retry и идемпотентность |
| Повтор команды внутри живой сессии | Loop | Прекращается вместе с жизненным циклом сессии |
| Периодическое возвращение к idle-сессии | Heartbeat | Привязано к owning process и session |
| Цель с продолжением между ходами | Persistent goal | Собственный критерий выполнения, внешняя проверка результата |
| Параллельные задачи одного хода | Delegation | Контекст и инструменты дочерних агентов задаются явно |
| Работа нескольких профилей с durable задачами | Kanban | Один dispatcher и ясный владелец побочных действий |
| Много вызовов инструментов за один inference turn | Code execution | RPC permissions и лимиты остаются обязательными |
| Реакция на lifecycle события | Hooks / webhooks | Авторизация и обработка повторного события |

[Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron),
[Loops](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops),
[Heartbeat](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat),
[Goals](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals),
[Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation),
[Kanban](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban),
[Code execution](https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution).

## 6. Доставка, интеграции и эксплуатация

Hermes имеет множество transport adapters; у Telegram, Discord, Slack, SMS,
Matrix и остальных каналов различаются auth, формат сообщений, ограничения
медиа, webhook/polling и адресация. Список платформ в приложении ниже — карта
документации, а не обещание одинакового поведения. Для Telegram один token не
должен одновременно обслуживаться двумя poller. Если несколько gateway
работают с разными профилями, назначь явные маршруты и владельца доставки.
[Messaging docs](https://hermes-agent.nousresearch.com/docs/llms.txt),
[Multiple gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways).

Внешние интеграции включают MCP, Google Workspace, A2A, ACP, OpenAI-совместимый
API server и relay. При подключении приложения сначала выбери контракт вызова,
затем session ownership, credential scope, rate/size limits и проверку
идемпотентности. [Programmatic Integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration),
[API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server),
[ACP](https://hermes-agent.nousresearch.com/docs/user-guide/features/acp).

Безопасность строится из нескольких независимых границ: права пользователя,
доступные toolsets, approvals, mounts, сеть/egress, секреты и изоляция процесса.
Профиль и prompt не являются заменой этих механизмов. Для изменения работающего
бота сравни исходный Git, Compose/systemd, запущенный image ID и runtime mount;
коммит в этом справочнике ничего не развёртывает.
[Security](https://hermes-agent.nousresearch.com/docs/user-guide/security),
[Secrets](https://hermes-agent.nousresearch.com/docs/user-guide/secrets),
[Managed Scope](https://hermes-agent.nousresearch.com/docs/user-guide/managed-scope),
[Network Isolation](https://hermes-agent.nousresearch.com/docs/user-guide/egress/network-isolation).

## 7. Практический маршрут проектирования бота

1. Запиши роль, аудиторию, каналы, допустимые действия, данные и критерий
   полезного ответа. Раздели знания о пользователе, предметную БД и историю
   диалога.
2. Проверь release: официальный индекс даёт кандидатов, `data/docs-catalog.json`
   находит локальный файл `v2026.9.14`, а tagged source подтверждает точный
   интерфейс. Если файл не найден, исследуй изменение отдельно.
3. Выбери отдельный профиль и gateway для отдельного bot identity. Назначь
   собственные секреты и writable state; shared mount допускай только там,
   где есть конкретная причина и контролируемые права.
4. Настрой модель, toolsets, контекстные файлы и минимальный skill. Добавляй
   MCP или plugin только для реального недостающего действия; внешний
   MemoryProvider — после измерения недостатка встроенной памяти.
5. Для расписания выбери cron, loop, heartbeat, goal или Kanban по жизненному
   циклу задачи. Проверь повторный запуск и единственного владельца side effect.
6. Проверь credentials, network/FS boundaries, сообщения платформы, состояние
   после рестарта и rollback. Зафиксируй архитектурное решение в
   `references/decisions/` по [policy](../references/knowledge-policy.md).

Для работающего бота проверь приватный реестр сервиса, исходный репозиторий,
развёрнутый образ и профиль; этот документ не подменяет такую проверку.

## 8. Как читать полный каталог

Приложение ниже перечисляет **все 239 URL** официального индекса из снимка.
`✓` означает, что найден одноимённый файл документации в закреплённом теге;
`?` означает, что прямого соответствия пути нет. `?` не доказывает отсутствие
функции: страница могла появиться позже, переехать или сменить имя. Для
документов тега без URL текущего индекса используй
`python3 scripts/find_docs.py --tag-only` из корня скилла и поле
`tag_documents` в `data/docs-catalog.json`.

## Приложение: все страницы официального индекса

### Getting Started (7)

- ✓ [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- ✓ [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
- ✓ [Learning Path](https://hermes-agent.nousresearch.com/docs/getting-started/learning-path)
- ✓ [Updating](https://hermes-agent.nousresearch.com/docs/getting-started/updating)
- ✓ [Nix Setup](https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup)
- ✓ [Platform Support](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support)
- ✓ [Android / Termux](https://hermes-agent.nousresearch.com/docs/getting-started/termux)

### Using Hermes (31)

- ✓ [CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli)
- ✓ [TUI (Ink terminal UI)](https://hermes-agent.nousresearch.com/docs/user-guide/tui)
- ✓ [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- ✓ [Configuring Models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
- ✓ [Sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions)
- ✓ [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- ✓ [Git Worktrees](https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees)
- ✓ [Docker Backend](https://hermes-agent.nousresearch.com/docs/user-guide/docker)
- ✓ [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- ✓ [Checkpoints & Rollback](https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback)
- ✓ [Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)
- ✓ [Hermes Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/desktop)
- ✓ [Egress proxy](https://hermes-agent.nousresearch.com/docs/user-guide/egress)
- ✓ [Egress credential-injection proxy (iron-proxy)](https://hermes-agent.nousresearch.com/docs/user-guide/egress/iron-proxy)
- ✓ [Network Egress Isolation (Docker)](https://hermes-agent.nousresearch.com/docs/user-guide/egress/network-isolation)
- ✓ [Import from Other Agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents)
- ✓ [Local Models](https://hermes-agent.nousresearch.com/docs/user-guide/local-models)
- ✓ [Managed Scope](https://hermes-agent.nousresearch.com/docs/user-guide/managed-scope)
- ✓ [Connecting Desktop to Many Hermes Instances](https://hermes-agent.nousresearch.com/docs/user-guide/multi-connection-desktop)
- ✓ [Running Many Gateways at Once](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- ✓ [Profile Distributions: Share a Whole Agent](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions)
- ✓ [Secrets](https://hermes-agent.nousresearch.com/docs/user-guide/secrets)
- ✓ [Bitwarden Secrets Manager](https://hermes-agent.nousresearch.com/docs/user-guide/secrets/bitwarden)
- ✓ [Command Helper Secret Source](https://hermes-agent.nousresearch.com/docs/user-guide/secrets/command)
- ✓ [1Password](https://hermes-agent.nousresearch.com/docs/user-guide/secrets/onepassword)
- ? [Session Storage Recovery](https://hermes-agent.nousresearch.com/docs/user-guide/session-storage-recovery)
- ✓ [Google Workspace — Gmail, Calendar, Drive, Sheets & Docs](https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace)
- ? [Switching to a Source Install](https://hermes-agent.nousresearch.com/docs/user-guide/switching-to-source)
- ✓ [Which File Does What?](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what)
- ✓ [Windows (Native) Guide](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native)
- ✓ [Windows (WSL2) Guide](https://hermes-agent.nousresearch.com/docs/user-guide/windows-wsl-quickstart)

### Core Features (36)

- ✓ [Features Overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview)
- ✓ [Tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)
- ✓ [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- ✓ [Curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator)
- ✓ [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- ✓ [Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers)
- ✓ [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)
- ✓ [Context References](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references)
- ✓ [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)
- ✓ [Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- ✓ [Built-in Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins)
- ? [Bot Screen](https://hermes-agent.nousresearch.com/docs/user-guide/features/bot-screen)
- ✓ [Codex App-Server Runtime (optional)](https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime)
- ✓ [Computer Use](https://hermes-agent.nousresearch.com/docs/user-guide/features/computer-use)
- ✓ [Passwords & Logins](https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-vault)
- ✓ [Deliverable Mode (Artifacts in Chat)](https://hermes-agent.nousresearch.com/docs/user-guide/features/deliverable-mode)
- ✓ [Document Extraction](https://hermes-agent.nousresearch.com/docs/user-guide/features/document-extraction)
- ✓ [Extending the Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard)
- ✓ [Session Heartbeats](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat)
- ✓ [Kanban Multi-Gateway Deployment](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-multi-gateway)
- ✓ [Kanban worker lanes](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes)
- ? [Language Packs](https://hermes-agent.nousresearch.com/docs/user-guide/features/language-packs)
- ✓ [Recurring Loops](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops)
- ✓ [LSP — Semantic Diagnostics](https://hermes-agent.nousresearch.com/docs/user-guide/features/lsp)
- ✓ [Mixture of Agents](https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents)
- ✓ [Pets (Petdex Mascots)](https://hermes-agent.nousresearch.com/docs/user-guide/features/pets)
- ✓ [Plugin Catalog](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog)
- ✓ [Skins & Themes](https://hermes-agent.nousresearch.com/docs/user-guide/features/skins)
- ✓ [Spotify](https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify)
- ✓ [Subscription Proxy](https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy)
- ✓ [Nous Tool Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway)
- ✓ [Tool Search](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search)
- ✓ [Wake Word](https://hermes-agent.nousresearch.com/docs/user-guide/features/wake-word)
- ✓ [Hermes Web Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)
- ✓ [Web Search & Extract](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search)
- ✓ [X (Twitter) Search](https://hermes-agent.nousresearch.com/docs/user-guide/features/x-search)

### Automation (8)

- ✓ [Cron Jobs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- ✓ [Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)
- ✓ [Kanban Multi-Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban)
- ✓ [Kanban Tutorial](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial)
- ✓ [Persistent Goals](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals)
- ✓ [Code Execution](https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution)
- ✓ [Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks)
- ✓ [Batch Processing](https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing)

### Media & Web (5)

- ✓ [Voice Mode](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)
- ✓ [Browser](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser)
- ✓ [Vision](https://hermes-agent.nousresearch.com/docs/user-guide/features/vision)
- ✓ [Image Generation](https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation)
- ✓ [Text-to-Speech](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts)

### Messaging Platforms (35)

- ✓ [Overview](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)
- ✓ [Telegram](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)
- ✓ [Discord](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord)
- ✓ [Slack](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack)
- ✓ [WhatsApp](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp)
- ✓ [Signal](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal)
- ✓ [Email](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email)
- ✓ [SMS](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms)
- ✓ [Matrix](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix)
- ✓ [Mattermost](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost)
- ✓ [Home Assistant](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant)
- ✓ [Webhooks](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks)
- ✓ [A2A (Agent-to-Agent)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a)
- ✓ [BlueBubbles (iMessage)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/bluebubbles)
- ✓ [Buzz](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/buzz)
- ✓ [DingTalk](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/dingtalk)
- ✓ [Feishu / Lark](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu)
- ✓ [Google Chat](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/google_chat)
- ✓ [IRC](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/irc)
- ✓ [LINE](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/line)
- ✓ [Microsoft Graph Webhook Listener](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/msgraph-webhook)
- ✓ [ntfy](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ntfy)
- ✓ [Open WebUI](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui)
- ✓ [Photon iMessage](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/photon)
- ✓ [QQ Bot](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot)
- ✓ [Raft](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/raft)
- ✓ [Hermes Relay](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/relay)
- ✓ [SimpleX Chat](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/simplex)
- ✓ [Microsoft Teams](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams)
- ✓ [Teams Meetings](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams-meetings)
- ✓ [WeCom (Enterprise WeChat)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom)
- ✓ [WeCom Callback (Self-Built App)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom-callback)
- ✓ [Weixin (WeChat)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin)
- ✓ [WhatsApp Business (Cloud API)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud)
- ✓ [Yuanbao](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/yuanbao)

### Integrations (11)

- ✓ [Integrations Overview](https://hermes-agent.nousresearch.com/docs/integrations)
- ✓ [Providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- ✓ [MCP (Model Context Protocol)](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- ✓ [ACP (Agent Context Protocol)](https://hermes-agent.nousresearch.com/docs/user-guide/features/acp)
- ✓ [API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server)
- ✓ [Honcho Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho)
- ✓ [Provider Routing](https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing)
- ✓ [Fallback Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers)
- ✓ [Credential Pools](https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools)
- ✓ [Buzz Integration](https://hermes-agent.nousresearch.com/docs/integrations/buzz)
- ✓ [Nous Portal](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)

### Guides & Tutorials (35)

- ✓ [Tips & Best Practices](https://hermes-agent.nousresearch.com/docs/guides/tips)
- ✓ [Local LLMs on Mac](https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac)
- ✓ [Daily Briefing Bot](https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot)
- ✓ [Team Telegram Assistant](https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant)
- ✓ [Use Hermes as a Python Library](https://hermes-agent.nousresearch.com/docs/guides/python-library)
- ✓ [Use MCP with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes)
- ✓ [Use Voice Mode with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes)
- ✓ [Use SOUL.md with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes)
- ✓ [Automate with Cron](https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron)
- ✓ [Work with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
- ✓ [Delegation Patterns](https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns)
- ✓ [GitHub PR Review Agent](https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent)
- ✓ [Give Your Agent Its Own Email Address](https://hermes-agent.nousresearch.com/docs/guides/agent-email-address)
- ✓ [Automation Blueprints](https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints)
- ✓ [AWS Bedrock](https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock)
- ✓ [Microsoft Foundry](https://hermes-agent.nousresearch.com/docs/guides/azure-foundry)
- ✓ [Script-Only Cron Jobs (No LLM)](https://hermes-agent.nousresearch.com/docs/guides/cron-script-only)
- ✓ [Cron Troubleshooting](https://hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting)
- ✓ [Desktop Native Sign-In (RFC 8252)](https://hermes-agent.nousresearch.com/docs/guides/desktop-native-signin)
- ✓ [Google Gemini](https://hermes-agent.nousresearch.com/docs/guides/google-gemini)
- ✓ [Google Vertex AI](https://hermes-agent.nousresearch.com/docs/guides/google-vertex)
- ✓ [Run Hermes Locally with Ollama — Zero API Cost](https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup)
- ✓ [Manage Hermes Cloud with MCP](https://hermes-agent.nousresearch.com/docs/guides/manage-hermes-cloud-with-mcp)
- ✓ [Register a Microsoft Graph Application](https://hermes-agent.nousresearch.com/docs/guides/microsoft-graph-app-registration)
- ✓ [Migrate from OpenClaw](https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw)
- ✓ [MiniMax OAuth](https://hermes-agent.nousresearch.com/docs/guides/minimax-oauth)
- ✓ [OAuth over SSH / Remote Hosts](https://hermes-agent.nousresearch.com/docs/guides/oauth-over-ssh)
- ✓ [Operate the Teams Meeting Pipeline](https://hermes-agent.nousresearch.com/docs/guides/operate-teams-meeting-pipeline)
- ✓ [Pipe Script Output to Messaging Platforms](https://hermes-agent.nousresearch.com/docs/guides/pipe-script-output)
- ✓ [Run Hermes Agent with Nous Portal](https://hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal)
- ✓ [Run Nemotron 3 Ultra free in Hermes Agent](https://hermes-agent.nousresearch.com/docs/guides/run-nemotron-3-ultra-free)
- ✓ [Running Hermes on a Personal or Work Machine](https://hermes-agent.nousresearch.com/docs/guides/secure-hermes-on-a-work-machine)
- ✓ [Troubleshooting: \"My Agent Feels Dumber\"](https://hermes-agent.nousresearch.com/docs/guides/troubleshooting-agent-quality)
- ✓ [Automated GitHub PR Comments with Webhooks](https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review)
- ✓ [xAI Grok OAuth (SuperGrok / X Premium+)](https://hermes-agent.nousresearch.com/docs/guides/xai-grok-oauth)

### Developer Guide (56)

- ✓ [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing)
- ✓ [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- ✓ [Agent Loop](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop)
- ✓ [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)
- ✓ [Context Compression & Caching](https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching)
- ✓ [Gateway Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals)
- ✓ [Session Storage](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage)
- ✓ [Provider Runtime](https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime)
- ✓ [Adding Tools](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools)
- ✓ [Adding Providers](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers)
- ✓ [Adding Platform Adapters](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters)
- ✓ [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- ✓ [Extending the CLI](https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli)
- ✓ [ACP Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals)
- ✓ [Billing Lifecycle (TUI)](https://hermes-agent.nousresearch.com/docs/developer-guide/billing-lifecycle)
- ✓ [Browser Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/browser-provider-plugin)
- ✓ [Browser CDP Supervisor](https://hermes-agent.nousresearch.com/docs/developer-guide/browser-supervisor)
- ✓ [Chronos Managed-Cron Contract](https://hermes-agent.nousresearch.com/docs/developer-guide/chronos-managed-cron-contract)
- ✓ [CLI Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/cli-internals)
- ✓ [Codebase Ownership Map](https://hermes-agent.nousresearch.com/docs/developer-guide/codebase-ownership)
- ✓ [Background completion backlogs](https://hermes-agent.nousresearch.com/docs/developer-guide/completion-backlog-delivery)
- ✓ [Context Engine Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin)
- ✓ [Cron Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals)
- ✓ [Desktop Plugin SDK (@hermes/plugin-sdk)](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk)
- ✓ [Egress proxy internals](https://hermes-agent.nousresearch.com/docs/developer-guide/egress-internals)
- ✓ [Gateway Monitoring](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-monitoring)
- ✓ [Gateway Session Lifecycle](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-session-lifecycle)
- ✓ [Image Generation Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin)
- ? [macOS bundle updates](https://hermes-agent.nousresearch.com/docs/developer-guide/macos-bundle-updates)
- ✓ [Memory Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin)
- ✓ [Micro-compaction](https://hermes-agent.nousresearch.com/docs/developer-guide/micro-compaction)
- ✓ [Middleware](https://hermes-agent.nousresearch.com/docs/developer-guide/middleware)
- ✓ [Model Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin)
- ✓ [Multiplexing Gateway Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/multiplexing-gateway)
- ✓ [Observer Hooks](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks)
- ✓ [Plugin LLM Access](https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access)
- ✓ [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
- ? [Application declarations](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/application-declarations)
- ? [Submitting to the Plugin Catalog](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission)
- ? [PM audit remediation status](https://hermes-agent.nousresearch.com/docs/developer-guide/pm-audit-status)
- ✓ [Programmatic Integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration)
- ✓ [Relay ↔ Connector Contract](https://hermes-agent.nousresearch.com/docs/developer-guide/relay-connector-contract)
- ✓ [Relay Shared Metrics](https://hermes-agent.nousresearch.com/docs/developer-guide/relay-shared-metrics)
- ✓ [Secret Source Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/secret-source-plugin)
- ? [Shared bundle builds](https://hermes-agent.nousresearch.com/docs/developer-guide/shared-bundle-builds)
- ? [Source update completion ownership](https://hermes-agent.nousresearch.com/docs/developer-guide/source-update-completion)
- ? [Stable release admission and promotion](https://hermes-agent.nousresearch.com/docs/developer-guide/stable-releases)
- ✓ [State DB Recovery](https://hermes-agent.nousresearch.com/docs/developer-guide/state-db-recovery)
- ✓ [Streaming TTS Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/streaming-tts)
- ✓ [Public Subagent Lifecycle API](https://hermes-agent.nousresearch.com/docs/developer-guide/subagent-lifecycle-api)
- ✓ [Terminal Environment Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin)
- ✓ [Tools Runtime](https://hermes-agent.nousresearch.com/docs/developer-guide/tools-runtime)
- ✓ [Trajectory Format](https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format)
- ✓ [Video Generation Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/video-gen-provider-plugin)
- ✓ [Web Search Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/web-search-provider-plugin)
- ✓ [TUI & Desktop from Worktrees](https://hermes-agent.nousresearch.com/docs/developer-guide/worktree-ui-dev)

### Reference (14)

- ✓ [CLI Commands](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
- ✓ [Slash Commands](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)
- ✓ [Profile Commands](https://hermes-agent.nousresearch.com/docs/reference/profile-commands)
- ✓ [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables)
- ✓ [Tools Reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)
- ✓ [Toolsets Reference](https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference)
- ✓ [MCP Config Reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)
- ✓ [Model Catalog](https://hermes-agent.nousresearch.com/docs/reference/model-catalog)
- ✓ [Bundled Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)
- ✓ [Optional Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)
- ✓ [FAQ & Troubleshooting](https://hermes-agent.nousresearch.com/docs/reference/faq)
- ✓ [Automation Blueprints Catalog](https://hermes-agent.nousresearch.com/docs/reference/automation-blueprints-catalog)
- ✓ [CLI Symbols Glossary](https://hermes-agent.nousresearch.com/docs/reference/cli-symbols)
- ? [Package Management](https://hermes-agent.nousresearch.com/docs/reference/package-management)

### More (1)

- ✓ [User Stories & Use Cases](https://hermes-agent.nousresearch.com/docs/user-stories)
