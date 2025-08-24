from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.business.menu_service import menu
from app.keyboards.inline.lang import lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import User
from utils.logging import logger
from sqlalchemy.ext.asyncio import AsyncSession


@common_router.message(CommandStart())
async def _start_command(message: types.Message, user: UserModel, state: FSMContext) -> None:
    """Команда /start с выбором языка и оферты"""
    
    # Очищаем любое состояние при команде /start
    current_state = await state.get_state()
    if current_state:
        logger.log("STATE_CLEAR", f"user={user.id} cleared_state={current_state} via /start command")
    await state.clear()

    if not user.accepted_offer:
        # Сначала предлагаем выбрать язык
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())
        return

    # Если пользователь уже принял оферту — продолжаем
    if user.profile:
        await menu(user.id)
    else:
        # Если профиля нет, но оферта принята - предлагаем создать профиль
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(F.data == "offer_accept")
async def _accept_offer(callback: CallbackQuery, user: UserModel, session: AsyncSession, state: FSMContext):
    # Очищаем любое состояние при принятии оферты
    current_state = await state.get_state()
    if current_state:
        logger.log("STATE_CLEAR", f"user={user.id} cleared_state={current_state} via offer_accept")
    await state.clear()
    
    await User.update_offer_accepted(session, user.id)
    await callback.message.edit_text("✅ Спасибо! Теперь вы можете пользоваться ботом.")

    # Продолжим с создания анкеты или меню
    if not user.profile:
        from app.keyboards.default.registration_form import create_profile_kb
        keyboard = create_profile_kb(user.language)
        await callback.message.answer(mt.WELCOME, reply_markup=keyboard)
    else:
        await menu(user.id)


@common_router.callback_query(F.data == "offer_decline")
async def _decline_offer(callback: CallbackQuery, state: FSMContext):
    # Очищаем любое состояние при отклонении оферты
    current_state = await state.get_state()
    if current_state:
        logger.log("STATE_CLEAR", f"user={user.id} cleared_state={current_state} via offer_decline")
    await state.clear()
    
    await callback.message.edit_text("❌ Без согласия с офертой вы не можете использовать бота.")