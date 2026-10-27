# Mini Apps, идентификация и экосистема

Официально: [Bot Features — Integration](https://core.telegram.org/bots/features#integration), [Mini Apps](https://core.telegram.org/bots/webapps), [Bot API](https://core.telegram.org/bots/api).

## Mini Apps

Mini App можно открыть из клавиатуры, inline-кнопки, меню, профиля как Main Mini App, direct link, inline-результата или attachment menu (последний режим ограничен доступностью). Точка запуска влияет на доступные `initData`, способ возврата данных и контекст чата; выбери её до реализации. Официальное руководство описывает [запуск](https://core.telegram.org/bots/webapps#launching-mini-apps) и [инициализацию](https://core.telegram.org/bots/webapps#initializing-mini-apps).

- На сервер передавай исходный `Telegram.WebApp.initData` и проверяй подпись и свежесть `auth_date` по [алгоритму Telegram](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app). `initDataUnsafe` и query-параметры браузера не служат аутентификацией. Для стороннего сервиса есть отдельная Ed25519-проверка; не подменяй один алгоритм другим.
- `sendData` работает для Mini App из keyboard button; `answerWebAppQuery` — для подходящего query flow. Не проектируй универсальный «вернуть данные боту» без проверки точки запуска.
- Учитывай тему, viewport, safe area, Back/Main/Secondary buttons, события активности и платформенные возможности. QR, буфер обмена, биометрия, геолокация, motion, local/secure/cloud storage, fullscreen, sharing и stories могут требовать разрешения пользователя или поддерживаться не каждым клиентом. Вызовы feature-detect и деградация интерфейса нужны для выбранных функций; полный список — [WebApp JS API](https://core.telegram.org/bots/webapps#initializing-mini-apps).
- Продукционный URL использует HTTPS; проверяй домен и origin. Telegram усилил проверку исходного домена Mini Apps в 2026 году — см. [Recent changes](https://core.telegram.org/bots/api#recent-changes). Если нужен публичный каталог, проверь требования [Main Mini App](https://core.telegram.org/bots/webapps#launching-the-main-mini-app), медиа-превью и [design guidelines](https://core.telegram.org/bots/webapps#designing-mini-apps).

## Web Login и внешняя учётная запись

[Login widget / `login_url`](https://core.telegram.org/bots/features#web-login) связывает Telegram с веб-сайтом. Настрой домен бота, проверь хэш и срок полученных данных на сервере по [документации авторизации](https://core.telegram.org/widgets/login#checking-authorization). Не считай введённый username доказательством личности и не прикрепляй аккаунт без защищённой сессии сайта.

## Business, каналы, сообщества

- [Business Bots](https://core.telegram.org/bots/features#business-bots) работают через `BusinessConnection` и его `rights`; учитывай `business_connection_id`, обновления создания/изменения/отключения и временные ограничения некоторых действий. Разрешения проверяй на каждый запрос по актуальному состоянию. Не смешивай сообщения от имени бизнеса с обычным чат-ботом.
- [Channel Direct Messages / Suggested Posts](https://core.telegram.org/bots/features#channel-direct-messages-and-suggested-posts): связанный канал, topic ID, отправка в директ, подготовка/одобрение/отклонение предложения. Нужные права различаются (`can_post_messages`, `can_manage_direct_messages`); проверь [Bot API](https://core.telegram.org/bots/api) перед действием.
- [Communities](https://core.telegram.org/bots/features#communities) связывают группы, каналы и ботов. Обрабатывай отдельные service updates и не предполагай, что участие в одном чате даёт доступ к другому.

## Боты как участники и объекты управления

- [Managed Bots](https://core.telegram.org/bots/features#managed-bots): включение Bot Management Mode, `managed_bot` updates, получение/замена токена и access settings. Токен дочернего бота — отдельный секрет; его хранение, изоляция и отзыв должны быть спроектированы до создания ботов от имени пользователей.
- [Bot-to-Bot Communication](https://core.telegram.org/bots/features#bot-to-bot-communication) имеет разные условия в группе, личном чате и Business; BotFather mode обязателен по соответствующему сценарию. Дедупликация, rate limits, предельная глубина и таймаут исключают циклы. Не строй архитектуру на старом абсолютном правиле «боты не видят ботов»: текущий обзор описывает исключения.
- [Guest Bots](https://core.telegram.org/bots/features#guest-bots) получают разовый контекст вызова без истории чата и списка участников; это отдельный механизм от inline mode.
- [HTML5 Games](https://core.telegram.org/bots/games) требуют регистрации игры в BotFather; обрабатывай `game_short_name` callback, возвращай URL через `answerCallbackQuery` и используй методы score/highscores.
