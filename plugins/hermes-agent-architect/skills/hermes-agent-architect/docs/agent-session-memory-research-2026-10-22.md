# Память агентских сессий: исследования, архитектурные подходы и выбор движка

> Historical research, 2026-10-22. Backend recommendations and access defaults below reflect the study stage. For the current V2 architecture and remaining OpenViking experiments, read the [project context instructions](project-context-routing.md). No OpenViking pilot outcome is claimed here.

**Исследование, 22 октября 2026.** Область: общая долгосрочная память нескольких агентских runtime и ночная консолидация сессий. Это обзор и проектное предложение; новая система пока не развёрнута. Внутренние пути, объёмы сессий и операционные детали VPS сохранены отдельно в приватном локальном документе.

## 1. Модель системы

Нужно разделить три задачи:

1. **Канонический архив:** хранит исходные сессии и позволяет восстановить, кто, когда и в каком контексте что сказал. Не зависит от LLM или memory provider.
2. **Ночная консолидация:** превращает часть эпизодов в кандидаты долгосрочной памяти. Каждый вывод сохраняет ссылку на точную реплику и статус проверки; ошибочный вывод можно отозвать, не переписывая историю.
3. **Извлечение:** перед ответом выбирает только релевантные проверенные карточки памяти, а при необходимости раскрывает первичный эпизод. Общий доступ нескольких агентов не означает, что каждую память надо вставлять в каждый prompt.

Пример: сначала пользователь говорит одному агенту «мы выбрали SQLite», позже другому — «теперь переходим на PostgreSQL». Архив хранит обе реплики. Память хранит две версии решения и временную связь `supersedes`. Если PostgreSQL предложил агент, это остаётся предложением, пока владелец его не подтвердит.

```
Источники сессий → неизменяемый архив → ходы и тематические эпизоды
                                   → ночные кандидаты → проверка → версии памяти
                                                                   ↓
                                                   поиск + ссылки на первоисточник
```

## 2. Что говорят исследования

**Поток эпизодов и рефлексия.** [Generative Agents](https://arxiv.org/abs/2304.03442) записывают наблюдения и ищут их по релевантности, давности и важности; reflections связывают несколько наблюдений в более общий вывод. Это аргумент за хранение и эпизода, и выведенной карточки. Эксперименты статьи проводились в симулированной среде, поэтому их результаты не доказывают качество личной памяти в другом приложении.

**Подходящая гранулярность.** [RMM](https://aclanthology.org/2025.acl-long.413/) индексирует тематическое резюме вместе с исходным фрагментом разговора и строит уровни utterance/turn/session. [LongMemEval](https://arxiv.org/html/2410.10813v1) показал, что индексирование на уровне хода и добавление извлечённых фактов в поисковый ключ помогают находить информацию; замена исходного диалога одними атомарными фактами теряет нюанс. Поэтому единица хранения — точная реплика/ход, единица навигации — цельный тематический эпизод, а факт — производная поисковая карточка.

**Время и изменение знаний.** [Zep/Graphiti](https://arxiv.org/html/2501.13956) различает время действия утверждения и время его записи системой. Новое противоречащее утверждение делает старое неактуальным, но не стирает его. [TiMem](https://aclanthology.org/2026.findings-acl.1091/) добавляет временную иерархию от наблюдений до устойчивых представлений и выбирает уровень retrieval по сложности вопроса. Метрики работ относятся к их benchmark и моделям, не к конкретному развёртыванию.

**Когда запускать дорогую консолидацию.** [RecMem](https://aclanthology.org/2026.findings-acl.1619/) откладывает LLM-анализ до повторения похожей темы. Это снижает вычислительный расход в их экспериментах, но одна важная команда или архитектурное решение могут быть уникальны. Нужны оба триггера: повторяемость и явно важное событие. [Sleep-time Compute](https://arxiv.org/html/2504.13171) переносит часть рассуждений на время до вопроса; польза особенно вероятна, когда будущие вопросы предсказуемы. Его измеренные преимущества главным образом получены на stateful математических задачах и SWE case study. «Ночной dreaming» не должен сочинять факты ради заполнения памяти.

**Ограничения.** [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) показывает, что большое контекстное окно не гарантирует использование релевантного фрагмента, если он теряется внутри длинного текста. [ER-MIA](https://arxiv.org/html/2602.15344) демонстрирует атаки через отравление сохранённой памяти. Диалог, web и tool output нужно извлекать как недоверенные данные, а не выполнять как инструкции.

## 3. Технический контракт архива

Для каждого source connector нужны: стабильный идентификатор источника и сессии, роль автора, время, порядок сообщений, parent/lineage после сжатия, ссылка на исходные байты, SHA-256 и версия парсера. Исходные байты неизменяемы, FTS/embeddings и summaries перестраиваются из них. Повторная загрузка с тем же идентификатором и hash не создаёт дубль; изменённый исходник фиксируется новой ревизией.

**SQLite-источники:** live базу копировать через [SQLite Online Backup API](https://sqlite.org/backup.html), затем читать snapshot. Простая копия одного DB-файла при WAL не является надёжным snapshot. Нельзя полагаться только на `session_end`: долгие чаты могут оставаться открытыми, а процесс может завершиться аварийно.

**JSONL-источники:** сохранять полный завершённый префикс файла и offset; неполная последняя строка ждёт следующего прохода. Нормализатор не должен дважды учитывать одно сообщение, если runtime пишет и raw message, и уведомление о том же событии. Reasoning, tool outputs и системные сообщения могут быть нужны в закрытом raw архиве, но не должны автоматически превращаться в общие факты.

Захват и ночной анализ запускаются раздельно. Сборщик должен сообщать `discovered`, `captured`, `lag`, `errors`, `last_good_snapshot`; каждое несовпадение видно оператору. Резервная копия должна находиться в другом failure domain и проходить тест восстановления.

## 4. Ночной pipeline

1. Из новых ходов строятся тематические эпизоды с целью, действиями, результатом и незавершёнными пунктами. Границы — смысловые, а не фиксированное число токенов.
2. Отбор направляет на LLM только важные решения, новые изменения и повторяющиеся темы. Нулевой результат допустим.
3. LLM предлагает типизированные кандидаты: preference, fact, decision, event, goal, procedure, lesson, pending task, hypothesis. У каждого — точный диапазон evidence, автор, confidence, время действия, срок актуальности и версия extractor.
4. Валидатор проверяет существование цитаты, авторство, время, scope, секреты и запрет на promotion неподтверждённой агентской гипотезы. Важные решения можно отправлять на ручную проверку.
5. Reconciler ищет старые карточки: `same`, `supports`, `supersedes`, `contradicts`, `unresolved`. Конфликт без достаточных данных остаётся нерешённым.
6. Promotion атомарно пишет новую версию и audit. Search отдаёт краткий вывод с ссылкой на точный эпизод; раскрытие исходного диалога — отдельный шаг.

Данные из книг и документов остаются в собственном первичном корпусе. Разговор о книге не превращает пересказ агента в цитату автора. Общая память нескольких агентов должна различать `owner_said`, `agent_said`, `tool_observed`, `external_source`, `derived_inference`.

## 5. Сравнение готовых решений

**Встроенный Hermes.** `state.db` сохраняет сессии и FTS5-индекс, `session_search` возвращает исходные реплики. Короткие `MEMORY.md`/`USER.md` подходят для проверенных заметок. Это отличная baseline одного Hermes-профиля, но не общий архив разных harness. Один профиль выбирает не более одного внешнего `MemoryProvider`; `sync_turn` асинхронен, обычный `on_pre_compress` best effort. Opt-in checkpoint API v2 возможен, но bundled providers его не реализуют: включать `checkpoint_required` без совместимого provider нельзя. [Сессии тега](https://github.com/NousResearch/hermes-agent/blob/v2026.9.14/website/docs/user-guide/sessions.md), [контракт provider](https://github.com/NousResearch/hermes-agent/blob/v2026.9.14/website/docs/developer-guide/memory-provider-plugin.md).

**Signet.** Локальный OSS Apache-2.0 daemon с каноническими транскриптами и перестраиваемыми FTS/vector/graph/MEMORY.md-проекциями. Dreaming выбирает scoped evidence и применяет ограниченный набор проверяемых операций с точной цитатой; queue переживает restart. Есть Hermes provider, Codex hooks/MCP и импорт типизированных transcript JSONL. Для старых исходных форматов требуются конвертеры. Нужно проверить version compatibility, schema import, scope и default `global` visibility; подключение hook не импортирует историю задним числом. Наиболее прямой готовый кандидат для cross-harness dreaming. [Архитектура](https://docs.signetai.sh/architecture/pipeline-storage/), [Hermes](https://docs.signetai.sh/harnesses/hermes-agent/), [Codex](https://docs.signetai.sh/harnesses/codex/), [импорт](https://docs.signetai.sh/sources/), [лицензия](https://github.com/Signet-AI/signetai/blob/main/LICENSE).

**OpenViking.** Локальный OSS сервер AGPLv3. `commit()` сначала сохраняет session archive, затем асинхронно строит abstract/overview и memory diff. Иерархия L0/L1/L2 помогает постепенно раскрывать большие ресурсы. Есть Hermes и Codex интеграции; Codex использует Stop/PreCompact/SessionEnd и idle sweep, потому что graceful end не всегда происходит. Hermes plugin сообщает, что ходы во время запуска/восстановления сервера могут быть не захвачены. Поэтому OpenViking годится для общей контекстной проекции, но независимый архив остаётся нужен. Совместимость plugin с закреплённым Hermes проверять отдельно; Quick Local не поддерживает OAuth-модель без статического ключа или локального llama.cpp. [Сессии](https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/08-session.md), [Hermes](https://github.com/volcengine/OpenViking/blob/main/examples/hermes-plugin/README.md), [Codex](https://github.com/volcengine/OpenViking/blob/main/docs/en/agent-integrations/04-codex.md).

**Hindsight.** `retain` извлекает сущности и временные отношения; `recall` соединяет semantic, BM25, graph и temporal; `reflect` делает дополнительный модельный синтез. Подходит для «что изменилось и когда». Self-host требует PostgreSQL/встроенную pg0 и модели; это производная память, не сборщик всех transcript. [Репозиторий](https://github.com/vectorize-io/hindsight).

**Mem0 OSS.** `add` извлекает атомарные факты и индексирует, `search` ищет их. Официальная документация прямо говорит, что по умолчанию хранится не verbatim transcript; текущий extraction additive, update/delete требуют явного действия. Хорош для предпочтений, но не как архив и не единственный механизм истории изменений. [How it works](https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/how-it-works.mdx).

**Graphiti и Cognee.** Graphiti строит темпоральный граф episodes/entities/edges с provenance, но не собирает сессии всех runtime сам. Cognee Hermes пишет ходы в session cache и переносит в граф через `improve()` на границе сессии. Выбирать позже, если простая память не проходит temporal/multi-hop вопросы. [Graphiti](https://github.com/getzep/graphiti), [Cognee Hermes](https://github.com/topoteretes/cognee-integrations/blob/main/integrations/hermes-agent/README.md).

**Remnic, agentmemory, Basic Memory, Letta.** Remnic и agentmemory предлагают автоматические hooks и общий локальный backend, но hook/capture надо отдельно проверять на crash и повторном запуске. Basic Memory удобен как человекочитаемый Markdown vault решений. Letta sleep-time agents разделяют диалог и работу над memory blocks, но требуют другого agent runtime, а не просто подключаются к уже работающему Hermes. [Remnic](https://github.com/joshuaswarren/remnic/blob/main/docs/plugins/hermes.md), [agentmemory](https://github.com/rohitg00/agentmemory), [Basic Memory](https://github.com/basicmachines-co/basic-memory/tree/main/integrations/hermes), [Letta](https://www.letta.com/blog/sleep-time-compute/).

| Подход | Полный первичный архив | Dreaming | Сильная сторона | Главный риск |
| --- | --- | --- | --- | --- |
| Только штатный Hermes | только его отдельные профили | ограниченно | простота, точные исходные реплики | не покрывает другие harness |
| Signet | новые hook-сессии; исторические после конвертации | да, audited | cross-harness и provenance | capture/import и scope нужно доказать |
| OpenViking | успешно commit-нутые сессии | да, async | иерархия ресурсов и памяти | пробелы захвата при отказе, совместимость |
| Hindsight/Mem0 | нет | extraction/reflect | факты и время | нельзя считать backup transcript |
| Независимый archive + выбранная проекция | да, при сверке адаптеров | настраиваемый | независимость, возможность replay | потребуется своя интеграция |

Единого независимого теста этих продуктов на одних и тех же данных пока нет. Сравнение — по опубликованным контрактам и архитектуре; лицензионная бесплатность self-host не покрывает LLM/embedding compute. Дополнительные Hermes-провайдеры сгруппированы в [предыдущем исследовании](https://github.com/alexlevnikov/alex_claude_marketplace/blob/main/plugins/hermes-agent-architect/skills/hermes-agent-architect/docs/hermes-memory-providers-review-2026-10-15.md).

## 6. Рекомендация и варианты

**A — рекомендуемый старт:** независимый неизменяемый archive и лёгкая SQLite FTS5 память; nightly worker сначала работает в shadow mode. Это даёт полное доказательное основание и позволяет заменить provider без миграции исходных сессий. Сложный граф и отдельную векторную БД отложить до проверки на реальных вопросах.

**B — Signet как слой dreaming/retrieval:** после отдельного пилота на копии архивных данных может заменить большую часть собственной семантической логики. Не заменяет независимый source backup. Критерии: reconciliation всех сообщений, качество русского extraction, точность ссылок, обновление фактов, resource use и исправление/удаление.

**C — OpenViking как общая context database:** полезен, если важнее единое дерево документов, навыков, сессий и памяти. Использовать как производный слой поверх независимого архива, если его поиск на смешанных запросах измеримо лучше. Не ставить несколько тяжёлых сервисов одновременно без оценки CPU/RAM.

Локальную и внешнюю LLM-обработку сравнить на одинаковой разрешённой владельцем выборке. Локальный вариант сохраняет текст у владельца и не требует оплаты API, но ограничен оборудованием и может хуже извлекать русский нюанс. Внешний может быть качественнее/быстрее, но требует явной политики передачи личных диалогов, проверки стоимости и квот. Бесплатный лимит не должен быть единственным гарантированным ночным путём.

## 7. Критерии пилота

Сначала archive-only в read-only режиме: полнота, идемпотентность, восстановление, compaction, незавершённая сессия и crash. Затем 30–50 вопросов: точный старый факт, обновление, межсессионная связь, важная единственная реплика, отсутствие ответа, противоречие, разные агенты, неверный агентский вывод, prompt injection. Измерять отдельно **source recall** и **качество ответа**. Dreaming сначала создаёт только кандидатов; автоматический promotion разрешается после проверки ложных фактов, пропусков, evidence, RAM/CPU, времени и расходов. Сквозная проверка каждого рабочего агента проводится адресно без запуска второго Telegram poller.

**Открытые решения:** срок хранения raw, политика «забудь», возможность внешнего LLM для личных/финансовых диалогов и права агентов на раскрытие полной чужой сессии. До решения этих вопросов рекомендовано общее чтение только проверенных карточек с точным раскрытием источника по запросу.

## Источники

Основные публикации: [Generative Agents](https://arxiv.org/abs/2304.03442), [LongMemEval](https://arxiv.org/html/2410.10813v1), [RMM](https://aclanthology.org/2025.acl-long.413/), [TiMem](https://aclanthology.org/2026.findings-acl.1091/), [RecMem](https://aclanthology.org/2026.findings-acl.1619/), [Sleep-time Compute](https://arxiv.org/html/2504.13171), [Zep temporal graph](https://arxiv.org/html/2501.13956), [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), [ER-MIA](https://arxiv.org/html/2602.15344).

Исходники реализаций: [Hermes](https://github.com/NousResearch/hermes-agent/blob/v2026.9.14/website/docs/developer-guide/session-storage.md), [Signet](https://docs.signetai.sh/architecture/pipeline-storage/), [OpenViking](https://github.com/volcengine/OpenViking/blob/main/docs/en/concepts/08-session.md), [Hindsight](https://github.com/vectorize-io/hindsight), [Mem0](https://github.com/mem0ai/mem0), [Graphiti](https://github.com/getzep/graphiti), [SQLite Online Backup API](https://sqlite.org/backup.html).
