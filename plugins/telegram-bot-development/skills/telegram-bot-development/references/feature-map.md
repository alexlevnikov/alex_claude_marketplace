# Карта возможностей

Это маршрутизатор по [официальному обзору](https://core.telegram.org/bots/features). За точными сигнатурами переходи в [Bot API](https://core.telegram.org/bots/api). Функции, включаемые в BotFather, не следует считать активными у конкретного бота без проверки настроек. Новые возможности отдельно проверяй в [журнале Bot API](https://core.telegram.org/bots/api#recent-changes).

| Поверхность / задача | Возможность и главный нюанс | Куда идти |
| --- | --- | --- |
| Личный чат | `/start`, `/help`, `/settings`, список команд по scope/языку, кнопка меню | [Commands](https://core.telegram.org/bots/features#commands), [setMyCommands](https://core.telegram.org/bots/api#setmycommands) |
| Пошаговый ввод | Reply keyboard, запрос контакта/локации/чата/пользователя/опроса | [Keyboards](https://core.telegram.org/bots/features#keyboards), [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup) |
| Действие под сообщением | Inline keyboard, callback, URL, copy, inline switch, game/pay | [Inline keyboards](https://core.telegram.org/bots/features#inline-keyboards), [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton) |
| Вызов из любого чата | Inline query ищет контент; Guest Mode позволяет боту ответить своим сообщением без вступления в чат | [Inline mode](https://core.telegram.org/bots/features#inline-requests), [Guest Bots](https://core.telegram.org/bots/features#guest-bots) |
| Передача контекста по ссылке | `start`, `startgroup`; для Mini App — `startapp`/`startattach` | [Deep linking](https://core.telegram.org/bots/features#deep-linking), [Mini Apps](https://core.telegram.org/bots/webapps) |
| Публичный групповой чат | Privacy Mode, admin rights, темы, join requests, модерация и service updates | [Privacy Mode](https://core.telegram.org/bots/features#privacy-mode), [ChatMember](https://core.telegram.org/bots/api#chatmember) |
| Приватный ответ внутри группы | Ephemeral message и команда с `is_ephemeral`; новые параметры проверяй по текущей версии | [Ephemeral](https://core.telegram.org/bots/features#ephemeral-messages), [EphemeralMessageParameters](https://core.telegram.org/bots/api#ephemeralmessageparameters) |
| Долгий ответ AI | `sendMessageDraft`/`sendRichMessageDraft`, затем постоянное сообщение; остановка генерации | [Streaming replies](https://core.telegram.org/bots/features#streaming-replies), [sendMessageDraft](https://core.telegram.org/bots/api#sendmessagedraft) |
| Разделение личного диалога | Темы в личном чате после включения в BotFather | [Topics](https://core.telegram.org/bots/features#topics-in-private-chats), [createForumTopic](https://core.telegram.org/bots/api#createforumtopic) |
| Сложный контент | Обычный текст/MarkdownV2/HTML или Rich Messages с блоками, медиа и таблицами | [Formatting](https://core.telegram.org/bots/features#messages-and-formatting), [sendRichMessage](https://core.telegram.org/bots/api#sendrichmessage) |
| Вовлечение | Файлы, альбомы, Live Photos, опросы/викторины, checklists, stickers/custom emoji | [Media](https://core.telegram.org/bots/features#media-and-messaging), [Bot API](https://core.telegram.org/bots/api) |
| Полный интерфейс | Mini App: клавиатура, кнопка, меню, главный экран, direct/inline/attachment entry points | [Mini Apps](https://core.telegram.org/bots/webapps), [design guidelines](https://core.telegram.org/bots/webapps#designing-mini-apps) |
| Управление чужими диалогами | Business connection с конкретными правами; channel direct messages и suggested posts | [Business](https://core.telegram.org/bots/features#business-bots), [Channel DMs](https://core.telegram.org/bots/features#channel-direct-messages-and-suggested-posts) |
| Экосистема ботов | Managed Bots, bot-to-bot communication, Guest Bots, Communities; отдельные режимы и ограничения | [Features](https://core.telegram.org/bots/features), [Bot API](https://core.telegram.org/bots/api) |
| Авторизация и игры | Telegram Web Login / `login_url`; HTML5 Games, счёт и лидерборд | [Web Login](https://core.telegram.org/bots/features#web-login), [Games](https://core.telegram.org/bots/games) |
| Продажа | Stars для цифровых товаров; провайдер для физических; платные медиа/подписки/подарки | [Digital](https://core.telegram.org/bots/payments-stars), [Physical](https://core.telegram.org/bots/payments) |
| Глобальная аудитория | `language_code`, локализация имени/описания/команд, явный fallback | [Language support](https://core.telegram.org/bots/features#language-support), [Bot API](https://core.telegram.org/bots/api) |
| Управление ботом | BotFather: токен, профиль, команды, режимы, Mini App, тестирование и alerts | [Bot Management](https://core.telegram.org/bots/features#bot-management), [FAQ](https://core.telegram.org/bots/faq) |

Выбирай минимальный интерфейс, который решает задачу: сообщение и кнопки подходят для короткого потока, Mini App оправдана сложной формой или постоянным интерактивным экраном. Это проектное правило, а не ограничение Telegram.
