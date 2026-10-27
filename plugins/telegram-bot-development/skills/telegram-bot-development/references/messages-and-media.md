# Сообщения, форматирование и медиа

Официально: [Messages and Formatting](https://core.telegram.org/bots/features#messages-and-formatting), [Bot API](https://core.telegram.org/bots/api), [Recent changes](https://core.telegram.org/bots/api#recent-changes).

## Выбор формата

| Нужный результат | Механизм | Проверка |
| --- | --- | --- |
| Короткий ответ, подпись, ссылка | [sendMessage](https://core.telegram.org/bots/api#sendmessage) с plain text, `entities` либо поддерживаемым `parse_mode` | Экранируй пользовательский текст для MarkdownV2/HTML; проверь длину и entities |
| Навигация и изменение состояния | Сообщение с inline keyboard, затем [editMessageText](https://core.telegram.org/bots/api#editmessagetext) или reply markup | Callback ack; сообщение может быть уже изменено/удалено |
| Структурный отчёт, таблицы, блоки, сложный AI-ответ | [sendRichMessage](https://core.telegram.org/bots/api#sendrichmessage), Rich Markdown/HTML или блоки | Проверяй поддержку клиентов, допустимые теги/блоки и право отправлять вложенные медиа |
| Видимый прогресс в личном чате | [sendMessageDraft](https://core.telegram.org/bots/api#sendmessagedraft) / [sendRichMessageDraft](https://core.telegram.org/bots/api#sendrichmessagedraft) | Черновик — временный preview; отправь окончательное постоянное сообщение; обработай `stopped_message_generation` |
| Ход длительной операции без черновика | [sendChatAction](https://core.telegram.org/bots/api#sendchataction) и/или редактируемое сообщение статуса | Не обещай процент выполнения, если его нельзя измерить |

Rich Messages появились в Bot API 10.1 и расширены в 10.2–10.3. Устаревшая библиотека может не поддерживать новые типы; сверяй текущие [InputRichMessage](https://core.telegram.org/bots/api#inputrichmessage), [Rich Markdown](https://core.telegram.org/bots/api#rich-markdown-style) и [Rich HTML](https://core.telegram.org/bots/api#rich-html-style). Форматирование обычных сообщений отличается от rich; не смешивай правила экранирования.

## Вложения и интерактивный контент

- Фото, видео, анимации, audio, voice, video notes, документы, контакты, геолокация, venue и `sendMediaGroup` — разные методы и свойства [Message](https://core.telegram.org/bots/api#message). Обрабатывай медиа по типу, а не по одному полю `text`. Для альбома учитывай `media_group_id` и то, что элементы могут приходить отдельными updates.
- [getFile](https://core.telegram.org/bots/api#getfile) даёт путь для загрузки; проверяй размер и срок доступности ссылки. `file_id` пригоден для повторной отправки тем же ботом, `file_unique_id` — для сравнения файлов между ботами, но не для отправки.
- [Poll](https://core.telegram.org/bots/api#poll) и [sendPoll](https://core.telegram.org/bots/api#sendpoll): обычный опрос, quiz, анонимность, варианты, время закрытия; `poll_answer` обрабатывай отдельно от `message` и проверяй, доступен ли нужный тип ответа.
- [Checklist](https://core.telegram.org/bots/api#checklist): создание и изменение пунктов, совместный доступ и права зависят от метода и контекста. Проверяй, кто может отмечать задачи и какие updates приходят при изменении.
- [LivePhoto](https://core.telegram.org/bots/api#livephoto) и [sendLivePhoto](https://core.telegram.org/bots/api#sendlivephoto) передают фото с коротким видео; проверь ограничения формата, размера и совместимость клиента.
- [Стикеры и custom emoji](https://core.telegram.org/stickers): бот может создавать и редактировать собственные наборы через [sticker methods](https://core.telegram.org/bots/api#stickers). Следуй техническим требованиям файла; методы редактирования не распространяй на чужой набор.
- Платные фото/видео, публикации каналов и rich media требуют отдельных разрешений и бизнес-правил; см. [платежи](payments.md) и [интеграции](integrations.md).

## Что проверить в реализации

Раздели сбор ответа и отправку: можно заранее проверить длину, разметку, доступность медиа и чат. Логируй метод, безопасные идентификаторы запроса, код/описание ошибки без содержимого токена и приватных вложений. Для пользовательского контента предусмотри понятное сообщение, если Telegram отклонит форматирование или файл.
