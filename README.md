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
psql "postgresql://postgres@127.0.0.1:5432/matcher" \
  -v ON_ERROR_STOP=1 -1 \
  -f migrations/init_001.sql
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
- **DOMAIN** — URL веб-приложения, связанного с ботом (должен смотреть на порт 8000).

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