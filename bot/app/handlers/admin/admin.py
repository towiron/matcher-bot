from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from bot.loader import _

from bot.app.commands import set_admins_commands
from bot.app.routers import admin_router
from bot.app.text import message_text as mt


@admin_router.message(StateFilter(None), Command("admin"))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await set_admins_commands(message.from_user.id)
    await message.answer(_(mt.YOU_ARE_ADMIN))
