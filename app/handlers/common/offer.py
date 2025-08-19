from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import UserModel
from app.text import message_text as mt
from database.services import User
from app.states.default import Onboarding
from loader import _, i18n


async def show_offer(message: Message, language: str) -> None:
    """Показывает оферту пользователю с кнопками на правильном языке"""
    with i18n.context() as ctx:
        ctx.locale = language
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=_(mt.OFFER_ACCEPT), callback_data="offer_accept"),
                    InlineKeyboardButton(text=_(mt.OFFER_NOT_ACCEPT), callback_data="offer_decline")
                ]
            ]
        )
        await message.answer(_(mt.OFFER), reply_markup=keyboard, parse_mode="HTML")


async def handle_offer_accept(callback, user: UserModel, session, state: FSMContext) -> None:
    """Обработчик принятия оферты"""
    await callback.answer()
    
    await User.update_offer_accepted(session, user.id)
    await callback.message.edit_text(mt.OFFER_ACCEPTED_ANSWER)

    # Завершаем onboarding процесс
    await state.clear()

    # Продолжаем с создания анкеты или меню
    if not user.profile:
        from app.keyboards.default.registration_form import create_profile_kb
        keyboard = create_profile_kb(user.language)
        await callback.message.answer(mt.WELCOME, reply_markup=keyboard)
    else:
        from app.business.menu_service import menu
        await menu(callback.from_user.id)


async def handle_offer_decline(callback, state: FSMContext) -> None:
    """Обработчик отклонения оферты"""
    await callback.answer()
    await callback.message.edit_text(mt.OFFER_NOT_ACCEPTED_ANSWER)
    
    # Завершаем onboarding процесс
    await state.clear()
