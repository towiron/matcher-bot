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