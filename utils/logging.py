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