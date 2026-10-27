# Доставка обновлений и архитектура

Официально: [Bot API — запросы и обновления](https://core.telegram.org/bots/api#making-requests), [getUpdates](https://core.telegram.org/bots/api#getupdates), [setWebhook](https://core.telegram.org/bots/api#setwebhook), [FAQ](https://core.telegram.org/bots/faq#getting-updates), [руководство по webhook](https://core.telegram.org/bots/webhooks).

## Сначала зафиксируй контракт

- Bot API — HTTPS API с токеном бота. Каждый ответ проверяй по `ok`, `result`/`description` и `parameters`; HTTP-успех сам по себе не гарантирует успех метода.
- Составь таблицу входных `Update`: `message`, `edited_message`, `callback_query`, `inline_query`, `chosen_inline_result`, `poll_answer`, `my_chat_member`, `chat_member`, `chat_join_request`, `business_connection`/business messages, `pre_checkout_query`, а также типы, нужные новым возможностям. Не предполагай, что все события приходят в `message`. Сверь [Update](https://core.telegram.org/bots/api#update) и `allowed_updates` у выбранного транспорта.
- События из недоверенного ввода: команды, callback data, deep-link payload, `web_app_data`, выбранные chat/user ID, содержимое сообщений и файлы. Проверяй грамматику и право пользователя выполнить действие на сервере. Видимость команды в меню, кнопка или выбор чата не дают разрешения.
- Сохраняй связь `bot_id + chat_id + message_thread_id + user_id` по потребности продукта. Не смешивай пользовательскую тему, групповой чат и Business connection. Telegram ID храни как целое достаточной разрядности или строку; не используй 32-битный тип.

## Polling или webhook

| Вопрос | Long polling | Webhook |
| --- | --- | --- |
| Получение | `getUpdates` с `offset`, `timeout` | Telegram отправляет HTTPS POST на `setWebhook` URL |
| Принцип подтверждения | Обновление подтверждается запросом с `offset` больше его `update_id`; двигай offset после надёжной обработки или постановки в очередь | Быстро прими запрос, проверь секрет и надёжно сохрани работу до HTTP 2xx; повторная доставка возможна |
| Эксплуатация | Один активный получатель на токен; отдельный worker можно масштабировать за очередью | Входящий HTTPS, валидный сертификат/порт, `secret_token`, контроль `getWebhookInfo` |
| Переключение | Не работает, пока webhook установлен | Вызывай `deleteWebhook` при переходе на polling; `drop_pending_updates` лишь при явной политике потери очереди |

Для webhook используй [secret_token](https://core.telegram.org/bots/api#setwebhook) и проверяй `X-Telegram-Bot-Api-Secret-Token`; не помещай токен бота в журналы, URL мониторинга и сообщения об ошибках. Ограничение источника по IP может быть дополнительной защитой, но не заменяет секрет. Секрет и токен храни вне Git. Для обработки с побочными эффектами веди ключ идемпотентности (`update_id`, а для платежа также идентификатор транзакции); повторная доставка не должна повторять выдачу, списание или создание заказа.

## Практические границы

- `allowed_updates` фильтрует будущие события, но может кратко пропустить уже созданные; проверь это при смене конфигурации.
- Callback подтверждай через `answerCallbackQuery`, даже если не показываешь текст: клиент иначе держит индикатор загрузки. Не блокируй ответ долгой работой.
- При 429 используй `retry_after` из [ResponseParameters](https://core.telegram.org/bots/api#responseparameters), очереди и лимиты по назначению. Для сетевых ошибок — ограниченные повторы с backoff; для постоянных 4xx — исправляй запрос или права. Не делай бесконечные повторы.
- Для файлов сначала проверь [getFile](https://core.telegram.org/bots/api#getfile), ограничения облачного API и необходимость [локального Bot API](https://core.telegram.org/bots/api#using-a-local-bot-api-server). `file_id` привязан к боту; `file_unique_id` нельзя использовать для отправки.
- Если система уже работает, проверь текущий webhook/poller, образ контейнера и реальную конфигурацию прежде чем запускать второй экземпляр. Исходный код и runtime могут расходиться.

## Проверки, которые доказывают работу

Отправь сообщение и callback в нужном типе чата; проверь корректный `Update`, ответ и повторное получение того же события. Для webhook проверь неверный секрет, временную ошибку обработчика и восстановление очереди. Для polling проверь перезапуск между выполнением действия и продвижением offset. Не используй продукционный токен для нагрузочных экспериментов.
