from pathlib import Path
import os
from dotenv import load_dotenv
from environs import Env

DIR = Path(__file__).absolute().parent.parent

APP_ENV = os.getenv("APP_ENV", "dev").lower()
load_dotenv(DIR / ".env", override=False)

if APP_ENV == "prod":
    load_dotenv(DIR / ".env.prod", override=True)
else:
    load_dotenv(DIR / ".env.dev", override=True)

ENV_FILE = os.getenv("ENV_FILE")
if ENV_FILE:
    load_dotenv(ENV_FILE, override=True)

env = Env()

# ---< Database >---
class DatabaseSettings:
    NAME: str | None = env.str("DB_NAME", default=None)
    HOST: str = env.str("DB_HOST", default="localhost")
    PORT: int = env.int("DB_PORT", default=5432)
    USER: str = env.str("DB_USER", default="postgres")
    PASS: str = env.str("DB_PASS", default="postgres")

    URL: str = env.str("DB_URL", default=f"sqlite+aiosqlite:///{DIR}/database/db.sqlite3")

    if all((NAME, HOST, PORT, USER, PASS)):
        URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO: bool = env.bool("DB_ECHO", default=False)
    POOL_SIZE: int = env.int("DB_POOL_SIZE", default=5)
    MAX_OVERFLOW: int = env.int("DB_MAX_OVERFLOW", default=10)

# ---< Redis >---
class RedisSettings:
    DB: int = env.int("REDIS_DB", default=5)
    HOST: str | None = env.str("REDIS_HOST", default=None)
    PORT: int = env.int("REDIS_PORT", default=6379)
    USER: str | None = env.str("REDIS_USER", default=None)   # <-- было int, это баг
    PASS: str | None = env.str("REDIS_PASS", default=None)

    URL: str | None = env.str("RD_URL", default=None)

    if all((HOST, PORT)) and DB is not None:
        if USER and PASS:
            URL = f"redis://{USER}:{PASS}@{HOST}:{PORT}/{DB}"
        else:
            URL = f"redis://{HOST}:{PORT}/{DB}"

# ---< Telegram bot >---
BOT_NAME: str | None = env.str("BOT_NAME", default=None)
BOT_TOKEN: str | None = env.str("TELEGRAM_BOT_TOKEN", default=None)
SKIP_UPDATES: bool = env.bool("SKIP_UPDATES", default=False)
NEW_USER_ALERT_TO_GROUP: bool = env.bool("NEW_USER_ALERT_TO_GROUP", default=True)

ADMINS: list[int] | None = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP: int | None = env.int("MODERATOR_GROUP_ID", default=None)

# AI
OPENAI_API_KEY: str | None = env.str("OPENAI_API_KEY", default=None)

# PAYMENT
CLICK_LIVE_TOKEN: str | None = env.str("CLICK_LIVE_TOKEN", default=None)
PAYME_LIVE_TOKEN: str | None = env.str("PAYME_LIVE_TOKEN", default=None)

TIME_ZONE: str = env.str("TIME_ZONE", default="Asia/Tashkent")  # удобнее, чем жёстко "UTC"

I18N_DOMAIN = "bot"

# ---< Search >---
CHANCE_COST: int = env.int("CHANCE_COST", default=0)
STARTER_CHANCE_COUNT: int = env.int("STARTER_CHANCE_COUNT", default=0)

# ---< Web App >---
WEB_APP_URL: str | None = env.str("WEB_APP_URL", default=None)
PUBLIC_BASE_URL: str | None = env.str("PUBLIC_BASE_URL", default=None)

# ---< Path/Dir >---
IMAGES_DIR: Path = DIR / "images"
LOGO_DIR = f"{IMAGES_DIR}/logo.png"
GRAPH_FILE_PATH: Path = IMAGES_DIR / "stats_graph.png"
LOCALES_DIR: Path = DIR / "data" / "locales"
LOG_FILE_PATH: Path = DIR / "logs" / "logs.log"

# ---< Other >---
database = DatabaseSettings()
redis = RedisSettings()
