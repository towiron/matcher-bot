from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery

from bot.app.business.menu_service import menu
from bot.app.keyboards.inline.lang import lang_ikb
from bot.app.routers import common_router
from bot.app.text import message_text as mt
from bot.database.models import UserModel
from bot.database.services import User


@common_router.message(StateFilter(None), CommandStart())
async def _start_command(message: types.Message, user: UserModel) -> None:
    """Команда /start с выбором языка и оферты"""

    if not user.accepted_offer:
        # Сначала предлагаем выбрать язык
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())
        return

    # Если пользователь уже принял оферту — продолжаем
    if user.profile:
        await menu(user.id)
    else:
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(F.data == "offer_accept")
async def _accept_offer(callback: CallbackQuery, user: UserModel, session):
    await User.update_offer_accepted(session, user.id)
    await callback.message.edit_text("✅ Спасибо! Теперь вы можете пользоваться ботом.")

    # Продолжим с создания анкеты или меню
    if not user.profile:
        from bot.app.keyboards.default.registration_form import create_profile_kb
        keyboard = create_profile_kb(user.language)
        await callback.message.answer(mt.WELCOME, reply_markup=keyboard)
    else:
        await menu(user.id)


@common_router.callback_query(F.data == "offer_decline")
async def _decline_offer(callback: CallbackQuery):
    await callback.message.edit_text("❌ Без согласия с офертой вы не можете использовать бота.")