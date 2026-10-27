# Интерфейсы и взаимодействия

Основной обзор: [Telegram Bot Features — Inputs and Interactions](https://core.telegram.org/bots/features).

## Команды, меню и клавиатуры

- Поддержи `/start` и `/help`, `/settings` — если есть настройки. Списки команд задаются через [setMyCommands](https://core.telegram.org/bots/api#setmycommands), при необходимости по [scope](https://core.telegram.org/bots/api#botcommandscope) и языку. При этом любой пользователь может прислать произвольную строку команды; роутер и авторизацию реализуй отдельно.
- [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup) удобна для заранее определённых ответов и запроса контакта, локации, чата или пользователей. Нажатие текстовой кнопки отправляет сообщение; текст не должен быть единственным идентификатором действия в локализованном интерфейсе. Убирай клавиатуру, когда она больше не нужна. `ForceReply` полезен для конкретного вопроса.
- [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup) прикреплена к сообщению. Callback data — ограниченный недоверенный payload; храни краткий opaque ID и состояние на сервере, если контекст сложен. Сразу вызывай [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery), затем редактируй сообщение/клавиатуру или отправляй результат.
- [Menu button](https://core.telegram.org/bots/api#setchatmenubutton) может показывать команды или открывать Mini App. Проверяй доступность в нужном чате.
- [KeyboardButtonRequestChat](https://core.telegram.org/bots/api#keyboardbuttonrequestchat) и [KeyboardButtonRequestUsers](https://core.telegram.org/bots/api#keyboardbuttonrequestusers) дают удобный выбор, но возвращённый ID сам по себе не гарантирует доступ к чату или пользователю. Проверяй фактические права.

## Вход из другого контекста

- [Deep links](https://core.telegram.org/bots/features#deep-linking): `?start=` для личного чата, `?startgroup=` для добавления в группу. Payload ограничен длиной и алфавитом; передавай короткий код/nonce, а чувствительное состояние держи на сервере с TTL и одноразовым использованием по задаче.
- [Inline mode](https://core.telegram.org/bots/api#inline-mode) включается в BotFather. Получай `inline_query`, возвращай результаты через `answerInlineQuery`, учитывай кэширование, пагинацию и доступность выбранного результата. Это пользовательский поиск с отправкой выбранного элемента.
- [Guest Mode](https://core.telegram.org/bots/features#guest-bots) позволяет упомянуть бота в чате, где он не состоит, и получить один ответ. Нужен переключатель BotFather; бот получает только контекст вызова, без истории и списка участников. Проектируй функцию без предположения о последующих обновлениях.
- [Attachment menu](https://core.telegram.org/bots/features#attachment-menu) доступно ограниченному кругу одобренных ботов. Не закладывай его как обязательный путь доступа без проверки допуска.

## Группы, каналы и темы

- [Privacy Mode](https://core.telegram.org/bots/features#privacy-mode) по умолчанию ограничивает сообщения группы; бот-администратор видит больше. Изменение настройки может потребовать повторного добавления бота. Минимизируй доступ и настраивай права администратора по функции, а не «на всякий случай».
- Для тем используй `message_thread_id` только там, где соответствующий тип чата и права это допускают. [Темы в личных чатах](https://core.telegram.org/bots/features#topics-in-private-chats) требуют включения в BotFather; проверь поддержку клиента и API перед созданием/редактированием темы.
- [Ephemeral messages](https://core.telegram.org/bots/features#ephemeral-messages) дают адресный ответ внутри группы. Для новых методов используй текущую модель [EphemeralMessageParameters](https://core.telegram.org/bots/api#ephemeralmessageparameters), а не старые примеры с отдельными `receiver_user_id`/`callback_query_id`. Не считай временное сообщение долговременным хранилищем результата.
- [Communities](https://core.telegram.org/bots/features#communities), директ канала и suggested posts вводят отдельные chat/topic IDs, service updates и права. Для каждого действия проверяй конкретный тип чата, текущую роль бота и [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights).

## Локализация

`language_code` опционален. Держи явный fallback, локализуй команды и публичные тексты через [setMyName](https://core.telegram.org/bots/api#setmyname), [setMyDescription](https://core.telegram.org/bots/api#setmydescription) и смежные методы; проверяй длину строк после перевода. Не используй язык как признак авторизации. См. [Language Support](https://core.telegram.org/bots/features#language-support).
