from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from bot.app.keyboards.default.registration_form import create_profile_kb
from bot.database.models import UserModel
from bot.app.text import message_text as mt

from bot.app.business.menu_service import menu
from bot.app.routers import common_router


@common_router.message(StateFilter("*"), F.text == "💤")
@common_router.message(StateFilter("*"), Command("cancel"))
async def cancel_command(message: types.Message, state: FSMContext, user: UserModel) -> None:
    """Сбрасывает состояния и отправляет меню пользователю"""
    await state.clear()
    if user.profile:
        await menu(message.from_user.id)
    else:
        await message.answer(mt.EMPTY_PROFILE, reply_markup=create_profile_kb(user.language))
