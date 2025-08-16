from bot.loader import _
from bot.data.config import BOT_NAME

"""
Текст вынес в отдельный файл для удобного редактирования
"""


class MessageText:
    @property
    def WELCOME(self):
        return _(f"""
Привет! 👋

Добро пожаловать в наш бот знакомств {BOT_NAME}! 💕
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
    def ARCHIVE_SEARCH(self):
        return _("Твоя анкета понравилась {} людям! Давай посмотрим, кто это:")

    @property
    def INVALID_PROFILE_SEARCH(self):
        return _("Подходящих анкет не найдено. Попробуй изменить фильтр 😊")

    @property
    def EMPTY_PROFILE_SEARCH(self):
        return _("Анкеты закончились. Попробуй позже! 😊")

    @property
    def MESSAGE_TO_YOU(self):
        return _("Сообщение для тебя:\n{}")

    def LIKE_ACCEPT(self, language: str):
        return _("Надеюсь вы хорошо проведете время ;) <a href='{}'>{}</a>", locale=language)

    def LIKE_ACCEPT_ALERT(self, language: str):
        return _(
            "На ваш лайк ответили взаимно, надеюсь вы хорошо проведете время ;) <a href='{}'>{}</a>",
            locale=language,
        )

    @property
    def LIKE_ARCHIVE(self):
        return _("Пока никто не поставил тебе лайк, но всё ещё впереди!")

    @property
    def MAILING_TO_USER(self):
        return _(
            "Можешь написать пользователю, до 250 символов. ✉️\n\nЕсли не хочешь писать, нажми на кнопку ниже."
        )

    @property
    def INVALID_MAILING_TO_USER(self):
        return _("Не корректное сообщение. Пожалуйста, напиши до 250 символов.")

    @property
    def DISABLE_PROFILE(self):
        return _("""
❌ Твоя анкета отключена, некоторые функции теперь недоступны.
💬 Чтобы снова активировать анкету, отправь команду /start.""")

    @property
    def INVALID_RESPONSE(self):
        return _("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝")

    @property
    def INVALID_LONG_RESPONSE(self):
        return _("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")

    @property
    def INVALID_CITY_RESPONSE(self):
        return _("Такой город не найдет :(")

    @property
    def INVALID_AGE(self):
        return _("Неверный формат, возраст нужно указывать цифрами. 🔢")

    @property
    def INVALID_HEIGHT(self):
        return _("Неверный формат, рост нужно указывать цифрами. 🔢")

    @property
    def INVALID_WEIGHT(self):
        return _("Неверный формат, вес нужно указывать цифрами. 🔢")

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
    def REPORT_TO_PROFILE(self):
        return _("✅ Жалоба успешно отправлена на рассмотрение!")

    @property
    def COMPLAINT(self):
        return _("""
Укажи причину жалобы:
🔞 Неприличный контент
💰 Реклама
🔫 Другое

↩️ Назад
""")

    @property
    def CHANCE_USER_LINK(self):
        return _("""
💌 Ты дал(а) шанс этому человеку!
Посмотри ещё раз его анкету — вдруг это начало чего-то особенного?
👉 <a href="{link}">Открыть профиль</a>
""")

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

    # ОПИСАНИЕ ФИЛЬТРА
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

    # ОПИСАНИЕ ПРОФИЛЯ
    @property
    def PROFILE_HEADER(self):
        return _("<b>Ваш профиль:</b>")

    @property
    def PROFILE_NAME(self):
        return _("<b>Имя:</b> {}")

    @property
    def PROFILE_SURNAME(self):
        return _("<b>Фамилия:</b> {} <i>(Видно только вам)</i>")

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
    def PROFILE_CHILDREN_LIVE_WITH_ME(self):
        return _("<b>Дети живут со мной:</b> {}")

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
    def PROFILE_POLYGAMY(self):
        return _("<b>Многожёнство:</b> {}")

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
    def GENDER_MALE(self):
        return _("Парень")

    @property
    def GENDER_FEMALE(self):
        return _("Девушка")

    @property
    def MARITAL_STATUS_SINGLE(self):
        return _("Не женат / не замужем")

    @property
    def MARITAL_STATUS_DIVORCED(self):
        return _("Разведён / разведена")

    @property
    def MARITAL_STATUS_WIDOWED(self):
        return _("Вдовец / вдова")

    @property
    def EDUCATION_PRIMARY(self):
        return _("Начальное")

    @property
    def EDUCATION_SECONDARY(self):
        return _("Среднее")

    @property
    def EDUCATION_HIGHER(self):
        return _("Высшее")

    @property
    def GOAL_FRIENDSHIP(self):
        return _("Дружба")

    @property
    def GOAL_COMMUNICATION(self):
        return _("Общение")

    @property
    def GOAL_MARRIAGE(self):
        return _("Брак")

    @property
    def RELIGION_ISLAM(self):
        return _("Ислам")

    @property
    def RELIGION_CHRISTIANITY(self):
        return _("Христианство")

    @property
    def RELIGION_JUDAISM(self):
        return _("Иудаизм")

    @property
    def RELIGION_BUDDHISM(self):
            return _("Буддизм")

    @property
    def RELIGIOUS_LEVEL_LOW(self):
        return _("Низкий")

    @property
    def RELIGIOUS_LEVEL_MEDIUM(self):
        return _("Средний")

    @property
    def RELIGIOUS_LEVEL_HIGH(self):
        return _("Высокий")



    # ЗАПОЛНЕНИЕ ПРОФИЛЯ
    @property
    def CREATE_PROFILE(self):
        return _("Создать профиль")

    @property
    def ASK_NAME(self):
        return _("Как вас зовут?")

    @property
    def ASK_SURNAME(self):
        return _("Укажите фамилию:")

    @property
    def ASK_GENDER(self):
        return _("Укажите пол:")

    @property
    def ASK_AGE(self):
        return _("Укажите возраст:")

    @property
    def ASK_CITY(self):
        return _("Укажите город:")

    @property
    def ASK_ETHNICITY(self):
        return _("Укажите национальность:")

    @property
    def ASK_RELIGION(self):
        return _("Укажите религию:")

    @property
    def ASK_RELIGIOUS_LEVEL(self):
        return _("Насколько вы религиозны?")

    @property
    def ASK_EDUCATION(self):
        return _("Укажите образование:")

    @property
    def ASK_JOB(self):
        return _("Чем вы занимаетесь?")

    @property
    def ASK_HEIGHT(self):
        return _("Укажите рост в см:")

    @property
    def ASK_WEIGHT(self):
        return _("Укажите вес в кг:")

    @property
    def ASK_MARITAL_STATUS(self):
        return _("Ваше семейное положение?")

    @property
    def ASK_HAS_CHILDREN(self):
        return _("Есть ли у вас дети?")

    @property
    def ASK_POLYGAMY(self):
        return _("Вы приемлете полигамию?")

    @property
    def ASK_GOAL(self):
        return _("Какова ваша цель знакомства?")

    @property
    def PRFILE_SUCCESSFULLY_CREATED(self):
        return _("✅ Ваш профиль успешно создан!")

    @property
    def FILTER_SUCCESSFULLY_ADDED(self):
        return _("✅ Фильтр успешно установлен!")

    # КЛАВИАТУРА
    @property
    def KB_FILL_PROFILE_AGAIN(self):
        return _("🔄 Заполнить профиль заново")

    @property
    def KB_BACK(self):
        return _("↩️ Назад")

    @property
    def KB_FIND_MATCH(self):
        return _("🔍 Найти пару")

    @property
    def KB_MY_PROFILE(self):
        return _("👤 Мой профиль")

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
    def KB_LOCATION(self):
        return _("📍 Отправить местоположение")

    @property
    def KB_ETHNICITY_UZBEK(self):
        return _("Узбек/чка")

    @property
    def KB_ETHNICITY_RUSSIAN(self):
        return _("Русский/ая")

    @property
    def KB_RELIGION_ISLAM(self):
        return _("Ислам")

    @property
    def KB_RELIGION_CHRISTIANITY(self):
        return _("Христианство")

    @property
    def KB_RELIGION_JUDAISM(self):
        return _("Иудаизм")

    @property
    def KB_RELIGION_BUDDHISM(self):
        return _("Буддизм")

    @property
    def KB_RELIGION_OTHER(self):
        return _("Другое")

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
    def KB_MARITAL_STATUS_SINGLE(self):
        return _("Не женат / Не замужем")

    @property
    def KB_MARITAL_STATUS_DIVORCED(self):
        return _("В разводе")

    @property
    def KB_MARITAL_STATUS_WIDOWED(self):
        return _("Вдовец / Вдова")

    @property
    def KB_HAS_CHILDREN_YES(self):
        return _("Да")

    @property
    def KB_HAS_CHILDREN_NO(self):
        return _("Нет")

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
    def FILL_FILTER(self):
        return _("""
Пожалуйста, заполните фильтр перед использованием функции поиска.""")

    @property
    def FILL_PROFILE_FIRST(self):
        return _("Заполните профиль сначала")

    @property
    def OFFER(self):
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
Используя сервис, вы подтверждаете, что ознакомлены с офертой и принимаете её условия.""")


message_text = MessageText()
