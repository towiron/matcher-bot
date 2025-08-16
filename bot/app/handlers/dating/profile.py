from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from bot.loader import _

from bot.app.business.menu_service import menu
from bot.app.business.profile_service import send_profile
from bot.app.routers import dating_router
from bot.app.text import message_text as mt
from bot.database.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from bot.app.keyboards.default.registration_form import profile_menu_kb


@dating_router.message(StateFilter(None), F.text == _(mt.KB_MY_PROFILE))
async def profile_command(message: types.Message, user: UserModel, session: AsyncSession) -> None:
    """Отправляет профиль пользователя"""
    keyboard = profile_menu_kb(user.language, user.profile)
    await send_profile(session, message.from_user.id, user.profile, user.language)
    await message.answer(mt.PROFILE_MENU, reply_markup=keyboard)

@dating_router.message(F.text == _(mt.KB_BACK))
async def _return_to_menu(message: types.Message, state: FSMContext) -> None:
    await state.clear()  # ✅ Очистка состояния
    await menu(message.from_user.id)