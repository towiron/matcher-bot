import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio

from aiogram.methods import DeleteWebhook

from bot.app.commands import set_default_commands
from bot.app.handlers import setup_handlers
from bot.app.middlewares import setup_middlewares
from bot.data.config import SKIP_UPDATES
from bot.loader import bot, dp
from bot.utils.logging import logger


async def on_startup() -> None:
    await set_default_commands()
    logger.log("BOT", "~ Bot startup")


async def on_shutdown() -> None:
    logger.log("BOT", "~ Bot shutting down...")


async def main():
    setup_middlewares(dp)
    setup_handlers(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot(DeleteWebhook(drop_pending_updates=SKIP_UPDATES))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
