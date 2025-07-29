from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter

from app.business.menu_service import menu
from app.keyboards.inline.lang import lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel


@common_router.message(StateFilter(None), CommandStart())
async def _start_command(message: types.Message, user: UserModel) -> None:
    """Стандартная команда /start для запуска бота и начала взаимодействия с ним"""
    if user.profile:
        await menu(user.id)
    else:
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())
