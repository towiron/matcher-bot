import logging
from logging import getLogger

from loguru import logger

from data.config import LOG_FILE_PATH

FORMAT = "[{time}] [{level}] [{file.name}:{line}]  {message}"
ROTATION = "1 month"
COMPRESSION = "zip"

logger.add(
    LOG_FILE_PATH,
    format=FORMAT,
    level="DEBUG",
    rotation=ROTATION,
    compression=COMPRESSION,
)

logger.level("BOT", no=18, color="<green>", icon="🚨")
logger.level("MESSAGE", no=15, color="<blue>", icon="✍️")
logger.level("CALLBACK", no=15, color="<blue>", icon="📩")
logger.level("DATABASE", no=17, color="<magenta>", icon="💾")

# Уровни для умного поиска
logger.level("AI_MATCH", no=19, color="<cyan>", icon="🤝")          # чуть выше DATABASE(17)
logger.level("AI_MATCH_DEBUG", no=20, color="<blue>", icon="🔍")    # между AI_MATCH(19) и AI_MATCH_REASONS(21)
logger.level("AI_MATCH_REASONS", no=21, color="<magenta>", icon="🧠") # между INFO(20) и SUCCESS(25)
logger.level("AI_MATCH_ERROR", no=35, color="<red>", icon="❌")       # между WARNING(30) и ERROR(40)
logger.level("AI_MATCH_TRY_ERROR", no=36, color="<red>", icon="🔄")   # ошибки попыток API
logger.level("AI_MATCH_TRY_ERROR_FALLBACK", no=37, color="<red>", icon="🔄") # ошибки fallback попыток
logger.level("AI_MATCH_WARNING", no=30, color="<yellow>", icon="⚠️")  # предупреждения
logger.level("AI_MATCH_JSON_ERROR", no=38, color="<red>", icon="📄")  # ошибки JSON
logger.level("AI_MATCH_FULL_RESPONSE", no=39, color="<red>", icon="📄") # полный ответ при ошибке
logger.level("AI_MATCH_ITEM_SKIP", no=40, color="<red>", icon="⏭️")   # пропуск элементов
logger.level("AI_MATCH_EMPTY", no=41, color="<red>", icon="📭")      # пустой результат
logger.level("AI_MATCH_GIVE_UP", no=42, color="<red>", icon="🏳️")   # сдались после попыток

logger.level("BALANCE_DEBUG", no=22, color="<yellow>", icon="💰")    # между AI_MATCH_REASONS(21) и WARNING(30)
logger.level("BALANCE_DEBIT", no=23, color="<red>", icon="��")       # списание шансов
logger.level("BALANCE_CREDIT", no=24, color="<green>", icon="💎")    # пополнение шансов
logger.level("BALANCE_ERROR", no=35, color="<red>", icon="❌")       # ошибки баланса

# Уровни для отладки поиска
logger.level("RESUME_SEARCH_DEBUG", no=25, color="<cyan>", icon="🔄")  # отладка возобновления поиска
logger.level("GIVE_CHANCE_DEBUG", no=26, color="<blue>", icon="💝")    # отладка дачи шанса
logger.level("BALANCE_DEBIT_ERROR", no=36, color="<red>", icon="💸❌") # ошибки списания шансов

# Уровни для управления состояниями
logger.level("STATE_CLEAR", no=27, color="<magenta>", icon="🧹")       # очистка состояний FSM


getLogger("aiogram").addFilter(
    lambda r: r.getMessage().find("Field 'database_user' doesn't exist in") == -1
)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())



for log_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
    getLogger(log_name).handlers = [InterceptHandler()]
    getLogger(log_name).propagate = False