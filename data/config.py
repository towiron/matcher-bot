from pathlib import Path

from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()


# ---< Database >---
class DatabaseSettings:
    NAME: str = env.str("DB_NAME", default=None)
    HOST: str = env.str("DB_HOST", default="localhost")
    PORT: int = env.int("DB_PORT", default=5432)
    USER: str = env.str("DB_USER", default="postgres")
    PASS: str = env.str("DB_PASS", default="postgres")

    URL: str = env.str("DB_URL", default=f"sqlite+aiosqlite:///{DIR}/database/db.sqlite3")

    if all((NAME, HOST, PORT, USER, PASS)):
        URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO = False
    POOL_SIZE = 5
    MAX_OVERFLOW = 10


# ---< Redis >---
class RedisSettings:
    DB: int = env.int("REDIS_DB", default=5)
    HOST: str = env.str("REDIS_HOST", default=None)
    PORT: int = env.int("REDIS_PORT", default=6379)
    USER: int = env.int("REDIS_USER", default="default")
    PASS: int = env.int("REDIS_PASS", default=None)

    URL: str = env.str("RD_URL", default=None)

    if all((DB, HOST, PORT)):
        URL = f"redis://{HOST}:{PORT}/{DB}"
        if all((USER, PASS)):
            URL = f"redis://{USER}:{PASS}@{HOST}:{PORT}/{DB}"


# ---< Telegram bot >---
BOT_NAME: str = env.str("BOT_NAME", default=None)
BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN", default=None)
SKIP_UPDATES: bool = env.bool("SKIP_UPDATES", default=False)
NEW_USER_ALERT_TO_GROUP: bool = env.bool("NEW_USER_ALERT_TO_GROUP", default=True)

ADMINS: list = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP: int = env.int("MODERATOR_GROUP_ID", default=None)

# AI
OPENAI_API_KEY: str = env.str("OPENAI_API_KEY", default=None)

# PAYMENT
CLICK_LIVE_TOKEN: str = env.str("CLICK_LIVE_TOKEN", default=None)
PAYME_LIVE_TOKEN: str = env.str("PAYME_LIVE_TOKEN", default=None)

TIME_ZONE = "UTC"

I18N_DOMAIN = "bot"

# ---< Search >---
CHANCE_COST: int = env.int("CHANCE_COST", default=0)
STARTER_CHANCE_COUNT: int = env.int("STARTER_CHANCE_COUNT", default=0)

# WEB APP
WEB_APP_URL: str = env.str("WEB_APP_URL", default=None)

# ---< Path\Dir >---
IMAGES_DIR: Path = DIR / "images"
LOGO_DIR = f"{IMAGES_DIR}/logo.png"

GRAPH_FILE_PATH: Path = IMAGES_DIR / "stats_graph.png"

LOCALES_DIR: Path = DIR / "data" / "locales"

LOG_FILE_PATH: Path = DIR / "logs" / "logs.log"

# ---< Other >---
database = DatabaseSettings()
redis = RedisSettings()
