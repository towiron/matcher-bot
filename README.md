

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/towiron/matcher-bot.git
cd matcher-bot
```

### 2. Установка PostgreSQL (P.S. нужно будет дать доступ на запросы через docker)

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. Создание пользователя и базы

Подключаемся к Postgres:
```bash
psql -h localhost -U "$(id -un)" -d postgres
```
Выполняем в psql:
```bash
CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'secret';
CREATE DATABASE matcher OWNER postgres ENCODING 'UTF8' TEMPLATE template1;
\du
\l matcher
```

#### Проверка подключения из контейнера:
```bash
docker run --rm -it postgres:16 psql \
  -h host.docker.internal -U postgres -d matcher -c '\conninfo'
```

### 3. Запуск docker-compose.yml
```bash
docker-compose up --build -d
```

### 4. Запуск миграций Alembic
```bash
docker compose exec matcher_service alembic current
docker compose exec matcher_service alembic upgrade head
```

### 5. Запуск сидов
```bash
docker compose exec matcher_service python database/seed/seed.py
```

## Переменное окружения (.env):
#### TELEGRAM BOT

- **BOT_NAME** — название Telegram-бота, отображаемое в коде или сообщениях (здесь: `Matcher`).
- **TELEGRAM_BOT_TOKEN** — токен, выданный BotFather, для авторизации и работы с Telegram Bot API.
- **SKIP_UPDATES** — флаг, указывающий, нужно ли пропускать накопившиеся обновления при старте бота (`True` — бот начнет с текущих сообщений).
- **ADMINS** — список ID администраторов бота, которым доступен полный контроль.
- **MODERATOR_GROUP_ID** — ID группы модераторов, куда отправляются уведомления.
- **NEW_USER_ALERT_TO_GROUP** — флаг, указывает, нужно ли отправлять уведомление в группу при появлении нового пользователя.
- **WEB_APP_URL** — URL веб-приложения, связанного с ботом (должен смотреть на порт 8000).

#### AI

- **OPENAI_API_KEY** — API-ключ для доступа к OpenAI (используется для генерации текста или ответов ИИ).

#### PAYMENT

- **CLICK_LIVE_TOKEN** — токен для подключения к платежной системе Click в боевом режиме.
- **PAYME_LIVE_TOKEN** — токен для подключения к платежной системе Payme в боевом режиме.

#### SEARCH

- **CHANCE_COST** — стоимость одной попытки (в условных единицах, здесь: `1000` валюта sum).
- **STARTER_CHANCE_COUNT** — количество бесплатных попыток, доступных новому пользователю.

#### DATABASE

- **DB_NAME** — название базы данных.
- **DB_USER** — имя пользователя для подключения к базе.
- **DB_PASS** — пароль для подключения к базе.
- **DB_HOST** — хост, где развернута база данных.
- **DB_PORT** — порт для подключения к базе.
- **DB_URL** — полный URL-адрес подключения к базе данных (формат для SQLAlchemy с asyncpg).

#### REDIS

- **REDIS_HOST** — имя или адрес хоста, где развернут Redis.
- **REDIS_PORT** — порт подключения к Redis.
- **REDIS_DB** — номер базы Redis.
- **RD_URL** — полный URL подключения к Redis.

P.S. Для проверку нужно открыть бота в тг и попробовать пройти весь flow.


## Структура файлов и их назначение

### Основные файлы запуска
- **`bot-runner.py`** - Точка входа для Telegram-бота
- **`service-runner.py`** - Точка входа для веб-сервиса (FastAPI)
- **`loader.py`** - Инициализация бота и диспетчера

### Папка `app/` - Основная логика бота
- **`commands.py`** - Установка команд бота
- **`routers.py`** - Роутеры для разных типов обработчиков
- **`text.py`** - Текстовые константы
- **`constans.py`** - Константы приложения

#### `app/handlers/` - Обработчики сообщений
- **`admin/`** - Административные функции (статистика, рассылка, баны)
- **`dating/`** - Логика знакомств (профили, поиск, фильтры)
- **`common/`** - Общие функции (помощь, язык, оплата)
- **`other/`** - Дополнительные обработчики

#### `app/business/` - Бизнес-логика
- **`alert_service.py`** - Уведомления
- **`dating_service.py`** - Логика знакомств
- **`filter_service.py`** - Фильтрация пользователей
- **`menu_service.py`** - Управление меню
- **`profile_service.py`** - Работа с профилями

#### `app/keyboards/` - Клавиатуры
- **`default/`** - Обычные клавиатуры
- **`inline/`** - Инлайн-клавиатуры

#### `app/middlewares/` - Промежуточное ПО
- **`admin.py`** - Проверка прав администратора
- **`database.py`** - Работа с базой данных
- **`i18n.py`** - Интернационализация
- **`log.py`** - Логирование

#### `app/states/` - Состояния FSM
- **`admin.py`** - Состояния для админ-панели
- **`default.py`** - Общие состояния

### Папка `database/` - Работа с базой данных
- **`connect.py`** - Подключение к базе данных
- **`models/`** - Модели данных (пользователи, профили, матчи)
- **`services/`** - Сервисы для работы с данными
- **`migrations/`** - Миграции Alembic
- **`seed/`** - Начальные данные

### Папка `frontend/` - Веб-интерфейс
- **`profile_page.html`** - Страница профиля
- **`filter_page.html`** - Страница фильтров
- **`static/`** - CSS и JavaScript файлы

### Папка `data/` - Конфигурация
- **`config.py`** - Настройки приложения
- **`locales/`** - Файлы локализации

### Папка `utils/` - Утилиты
- **`logging.py`** - Настройка логирования
- **`geopy.py`** - Работа с геолокацией
- **`graphs.py`** - Графики и визуализация
- **`base62.py`** - Кодирование

### Docker файлы
- **`Dockerfile.bot`** - Образ для Telegram-бота
- **`Dockerfile.service`** - Образ для веб-сервиса
- **`docker-compose.yml`** - Оркестрация контейнеров