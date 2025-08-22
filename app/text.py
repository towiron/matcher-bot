from loader import _

class MessageText:
    ###################
    #  COMMAND + MENU #
    ###################

    @property
    def WELCOME(self):
        return _("""
Привет! 👋

Добро пожаловать в наш бот знакомств <b>Sovchi (Baxt izlab)</b> 💕
Чтобы начать, создай свой профиль — это просто и быстро.

Желаем тебе приятных знакомств и интересных встреч!
""")

    @property
    def MENU(self):
        return _("""
🔍 Найти пару.
👤 Мой профиль.
💎 Пополнить шансы.

❌ Я больше не хочу никого искать.
""")

    @property
    def PROFILE_MENU(self):
        return _("""
🔍 Найти пару. 
🔄 Заполнить профиль заново
↩️ Назад
""")

    @property
    def UNKNOWN_COMMAND(self):
        return _("Неизвестная команда. Если заблудился, напиши /start.")

    @property
    def INFO(self):
        return _("""
👋 Пока что пусто...
""")

    @property
    def SEARCH(self):
        return _("🔍 Выполняется поиск...")

    @property
    def SEARCH_MENU(self):
        return _("""
🔍 Поиск по фильтру
🧠 Умный поиск(3 💎)

✏️ Изменить фильтр
↩️ Назад
""")

    #############
    #  KEYBOARD #
    #############

    @property
    def KB_FILL_PROFILE_AGAIN(self):
        return _("🔄 Заполнить профиль заново")

    @property
    def KB_BACK(self):
        return _("↩️ Назад")

    @property
    def KB_BACK_UZ(self):
        return _("↩️ Орқага")

    @property
    def KB_FIND_MATCH(self):
        return _("🔍 Найти пару")

    @property
    def KB_MY_PROFILE(self):
        return _("👤 Мой профиль")

    @property
    def KB_MY_PROFILE_UZ(self):
        return _("👤 Менинг профилим")

    @property
    def KB_DISABLE_PROFILE(self):
        return _("❌ Я больше не хочу никого искать")

    @property
    def KB_GENDER_MALE(self):
        return _("Парень")

    @property
    def KB_GENDER_FEMALE(self):
        return _("Девушка")

    @property
    def KB_RELIGIOSITY_NONE(self):
        return _("Не религиозен(а)")

    @property
    def KB_RELIGIOSITY_LOW(self):
        return _("Немного")

    @property
    def KB_RELIGIOSITY_MEDIUM(self):
        return _("Средне")

    @property
    def KB_RELIGIOSITY_HIGH(self):
        return _("Очень")

    @property
    def KB_RELIGIOSITY_STRICT(self):
        return _("Следую всем нормам")

    @property
    def KB_EDUCATION_SECONDARY(self):
        return _("Среднее")

    @property
    def KB_EDUCATION_INCOMPLETE_HIGHER(self):
        return _("Неоконченное высшее")

    @property
    def KB_EDUCATION_HIGHER(self):
        return _("Высшее")

    @property
    def KB_POLYGAMY_YES(self):
        return _("Да")

    @property
    def KB_POLYGAMY_NO(self):
        return _("Нет")

    @property
    def KB_POLYGAMY_UNSURE(self):
        return _("Не знаю / Не уверен(а)")

    @property
    def KB_GOAL_MARRIAGE(self):
        return _("Брак")

    @property
    def KB_GOAL_SERIOUS_RELATIONSHIP(self):
        return _("Серьезные отношения")

    @property
    def KB_GOAL_FRIENDSHIP(self):
        return _("Дружба")

    @property
    def KB_GOAL_COMMUNICATION(self):
        return _("Общение")

    @property
    def KB_LEAVE_PREVIOUS(self):
        return _("Оставить предыдущее")

    @property
    def KB_STAT_USER(self):
        return _("Статистика пользователей")

    @property
    def KB_STAT_PROFILE(self):
        return _("Статистика профилей")

    @property
    def KB_SEARCH_FILTER(self):
        return _("Фильтр поиска")

    @property
    def KB_GIVE_CHANCE(self):
        return _("Шанс (1 💎)")

    @property
    def KB_NEXT(self):
        return _("Следующий")

    @property
    def KB_BUY_CHANCES(self):
        return _("💎 Пополнить шансы")

    @property
    def KB_BACK_TO_SEARCH(self):
        return _("Меню поиска")

    @property
    def KB_CREATE_FILTER(self):
        return _("✨ Создать фильтр")

    @property
    def KB_CHANGE_FILTER(self):
        return _("✏️ Изменить фильтр")

    @property
    def KB_SEARCH_BY_FILTER(self):
        return _("🔍 Поиск по фильтру")

    @property
    def KB_SEARCH_BY_AI(self):
        return _("🧠 Умный поиск (3 💎)")

    @property
    def CHANGE_LANG(self):
        return _("Выбери язык 👇")

    def DONE_CHANGE_LANG(self, language: str):
        return _("Язык бота изменён! ✅", locale=language)

    @property
    def YOU_ARE_ADMIN(self):
        return _("""Вы — администратор!
Новые доступные команды:
- <b>/stats</b> — статистика бота.
- <b>/mailing</b> — рассылка всем пользователям.
- <b>/log</b> — просмотр логов бота.
- <b>/ban</b> — заблокировать пользователя по ID.
- <b>/unban</b> — разблокировать пользователя по ID.
""")

    @property
    def REPORT_TO_USER(self):
        return """
User <code>{}</code> (@{}) sent a complaint
about a user profile:<code>{}</code> (@{})

The reason: {}
"""

    @property
    def EMPTY_PROFILE(self):
        return _("""
    ✨ Чтобы продолжить пользоваться ботом, тебе нужно создать профиль!
    """)

    @property
    def USER_STATS(self):
        return _("""
👤 Пользователей: {}\t| 🚫 Заблокированных: {}
🌍 Самый популярный язык: {}
""")

    @property
    def PROFILE_STATS(self):
        return _("""
📂 Профилей: {} | 🔕 Инактивных: {}
🙍‍♂ Парней: {} | 🙍‍♀ Девушек: {}

💘 Мэтчи: {}

🕘 Средний возраст: {}
🏙 Популярный город: {}
""")

    ###########
    #  FILTER #
    ###########
    @property
    def FILTER_HEADER(self):
        return _("<b>Ваш фильтр:</b>")

    @property
    def FILTER_CITY(self):
        return _("<b>Город:</b> {}")

    @property
    def FILTER_AGE_FROM(self):
        return _("<b>Возраст от:</b> {}")

    @property
    def FILTER_AGE_TO(self):
        return _("<b>Возраст до:</b> {}")

    @property
    def FILTER_HEIGHT_FROM(self):
        return _("<b>Рост(см) от:</b> {}")

    @property
    def FILTER_HEIGHT_TO(self):
        return _("<b>Рост(см) до:</b> {}")

    @property
    def FILTER_WEIGHT_FROM(self):
        return _("<b>Вес(кг) от:</b> {}")

    @property
    def FILTER_WEIGHT_TO(self):
        return _("<b>Вес(кг) до:</b> {}")

    @property
    def FILTER_HAS_CHILDREN(self):
        return _("<b>Есть ли дети:</b> {}")

    @property
    def FILTER_GOAL(self):
        return _("<b>Цель:</b> {}")

    @property
    def FILTER_ETHNICITY(self):
        return _("<b>Национальность:</b> {}")

    @property
    def FILTER_SUCCESSFULLY_ADDED(self):
        return _("✅ Фильтр успешно установлен!")

    ###########
    #  PROFILE #
    ###########

    @property
    def DISABLE_PROFILE(self):
        return _("""
❌ Твоя анкета отключена, некоторые функции теперь недоступны.
💬 Чтобы снова активировать анкету, отправь команду /start.""")

    @property
    def FILL_PROFILE_FIRST(self):
        return _("Заполните профиль сначала")

    @property
    def PROFILE_NAME(self):
        return _("<b>Имя:</b> {}")

    @property
    def PROFILE_AGE(self):
        return _("<b>Возраст:</b> {}")

    @property
    def PROFILE_GENDER(self):
        return _("<b>Пол:</b> {}")

    @property
    def PROFILE_CITY(self):
        return _("<b>Город:</b> {}")

    @property
    def PROFILE_HEIGHT(self):
        return _("<b>Рост:</b> {} см")

    @property
    def PROFILE_WEIGHT(self):
        return _("<b>Вес:</b> {} кг")

    @property
    def PROFILE_MARITAL_STATUS(self):
        return _("<b>Семейное положение:</b> {}")

    @property
    def PROFILE_HAS_CHILDREN(self):
        return _("<b>Есть дети:</b> {}")

    @property
    def PROFILE_EDUCATION(self):
        return _("<b>Образование:</b> {}")

    @property
    def PROFILE_JOB(self):
        return _("<b>Профессия:</b> {}")

    @property
    def PROFILE_GOAL(self):
        return _("<b>Цель знакомства:</b> {}")

    @property
    def PROFILE_RELIGION(self):
        return _("<b>Религия:</b> {}")

    @property
    def PROFILE_RELIGIOUS_LEVEL(self):
        return _("<b>Уровень религиозности:</b> {}")

    @property
    def PROFILE_ETHNICITY(self):
        return _("<b>Национальность:</b> {}")

    @property
    def PROFILE_ABOUT(self):
        return _("<b>О себе:</b> {}")

    @property
    def PROFILE_LOOKING_FOR(self):
        return _("<b>Кого ищу:</b> {}")

    @property
    def PROFILE_NOT_SPECIFIED(self):
        return _("Не указано")

    @property
    def PROFILE_YES(self):
        return _("Да")

    @property
    def PROFILE_NO(self):
        return _("Нет")

    @property
    def CREATE_PROFILE(self):
        return _("Создать профиль")

    @property
    def PRFILE_SUCCESSFULLY_CREATED(self):
        return _("✅ Ваш профиль успешно создан!")

    @property
    def FILL_FILTER(self):
        return _("""
Пожалуйста, заполните фильтр перед использованием функции поиска.""")

    ###########
    # PAYMENT #
    ###########

    ###########
    #  OFFER #
    ###########

    def OFFER(self, language: str):
        return _("""
    📄 Публичная оферта

    1. Общие условия
    Сервис предназначен для совершеннолетних (18+) пользователей из Узбекистана.
    ИИ-агент помогает находить собеседников, поддерживает общение и способствует обмену контактами — только по обоюдному желанию.

    2. Конфиденциальность и безопасность
    Мы не собираем личные данные, такие как имя, адрес, номер телефона.
    Все анкеты и переписка оформлены анонимно.
    Данные защищены и используются только для работы сервиса.

    3. Запрещено
    Запрещены:
    – оскорбления, агрессия, домогательства, мошенничество;
    – пропаганда насилия, терроризма, порнографии;
    – попытки навязать услуги или обмануть других.

    4. Ответственность
    ИИ — цифровой помощник. Он не гарантирует результат и не заменяет человека.
    Все решения принимает сам пользователь.
    Сервис не несёт ответственности за последствия общения.

    5. Блокировка
    При подтверждённом нарушении правил анкета может быть заблокирована без предупреждения — для защиты других пользователей.

    6. Платные функции
    Некоторые функции доступны через «Шансы» — внутреннюю валюту.
    Покупка добровольная. Использованные «Шансы» не подлежат возврату.

    7. Принятие условий
    Используя сервис, вы подтверждаете, что ознакомлены с офертой и принимаете её условия.""", locale=language)

    def OFFER_ACCEPT(self, language: str):
        return _("✅ Я согласен", locale=language)

    def OFFER_NOT_ACCEPT(self, language: str):
        return _("❌ Не согласен", locale=language)

    @property
    def OFFER_ACCEPTED_ANSWER(self):
        return _("✅ Спасибо! Теперь вы можете пользоваться ботом.")

    @property
    def OFFER_NOT_ACCEPTED_ANSWER(self):
        return _("❌ Без согласия с офертой вы не можете использовать бота.")

    @property
    def OFFER_REQUIRED(self):
        return _("❗ Вы должны принять оферту перед использованием бота. Введите /start")

    ###########
    #  BONUS #
    ###########
    def DAILY_BONUS(self, streak: int) -> str:
        return _("""
🎁 Вы получили ежедневный бонус: 1 шанс!
🔥 Вы активны уже {streak} дней подряд!
""").format(streak=streak)


    ###########
    #  SEARCH #
    ###########
    @property
    def INVALID_PROFILE_SEARCH(self):
        return _("Подходящих анкет не найдено. Попробуй изменить фильтр 😊")

    @property
    def EMPTY_PROFILE_SEARCH(self):
        return _("Анкеты закончились. Попробуй позже! 😊")

    def SMART_SEARCH_BALANCE_ERROR(self, balance: int):
        return _("""
❌ Для умного поиска нужно <b>3 💎</b>.
Сейчас на балансе: <b>{balance} 💎</b>.
Пополните баланс и попробуйте снова.
""").format(balance=balance)

    @property
    def ERR_CHANCES_DEBIT_FAILED(self):
        return _("❌ Не удалось списать шансы. Попробуйте позже.")

    def SMART_SEARCH_MATCH_REASON(self, reason: str) -> str:
        return _("✨ Почему подходит: {reason}").format(reason=reason)

    @property
    def ERR_NO_CHANCES_LEFT(self) -> str:
        return _("❌ У вас закончились шансы.")

    def GAVE_CHANCE(self, profile_link: str, user_balance: int) -> str:
        return _("""
✨ Вы дали шанс этому человеку!
Посмотри ещё раз анкету — вдруг это начало чего-то особенного?
🚀 <a href=\"{profile_link}\">Открыть профиль</a>

💎 Вы потратили <b>1</b> шанс, осталось: <b>{balance}</b> шанс(ов).
""").format(
    profile_link=profile_link,
    balance=user_balance,
)

    @property
    def GOT_CHANCE(self) -> str:
        return _("✨ Тебе дали шанс!")

    @property
    def SMART_SEARCH_EMPTY_REPEAT(self) -> str:
        return _("""
🧠 Кандидаты умного поиска закончились!
Но у нас есть ещё интересные люди! Нажмите снова «🧠 Умный поиск (3 💎)»,
и я подберу новую подборку 😊
""")

    @property
    def SMART_SEARCH_EMPTY_FALLBACK(self) -> str:
        return _("""
🧠 Кандидаты умного поиска закончились!\n\n"
Попробуйте обычный поиск по фильтру — возможно, там найдутся интересные люди 😊
""")

message_text = MessageText()
