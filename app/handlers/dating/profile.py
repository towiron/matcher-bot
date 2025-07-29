from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.keyboards.default.registration_form import create_profile_kb
from loader import _

from app.business.menu_service import menu
from app.business.profile_service import send_profile
from app.keyboards.default.base import profile_kb
from app.routers import dating_router
from app.text import message_text as mt
from database.models import UserModel
from app.keyboards.default.registration_form import profile_menu_kb


@dating_router.message(StateFilter(None), F.text == _(mt.KB_MY_PROFILE))
async def profile_command(message: types.Message, user: UserModel) -> None:
    """Отправляет профиль пользователя"""
    keyboard = profile_menu_kb()
    await send_profile(message.from_user.id, user.profile)
    await message.answer(mt.PROFILE_MENU, reply_markup=keyboard)

@dating_router.message(StateFilter(None), F.text == _(mt.KB_BACK))
async def _return_to_menu(message: types.Message) -> None:
    await menu(message.from_user.id)
