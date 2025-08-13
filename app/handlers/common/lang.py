from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards.default.registration_form import create_profile_kb
from app.keyboards.inline.lang import LangCallback, lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import User
from app.business.menu_service import menu
from loader import _


@common_router.message(StateFilter(None), Command("language"))
@common_router.message(StateFilter(None), Command("lang"))
async def _lang(message: types.Message) -> None:
    """Отображает список доступных языков и позволяет выбрать предпочтительный"""
    await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(StateFilter(None), LangCallback.filter())
async def _change_lang(
    callback: types.CallbackQuery, callback_data: LangCallback, user: UserModel, session
) -> None:
    """Обрабатывает выбранный пользователем язык, и устанавливает его"""
    language = callback_data.lang
    await User.update(
        session=session,
        id=user.id,
        language=language,
    )
    await callback.message.edit_text(mt.DONE_CHANGE_LANG(language))
    
    # Если пользователь еще не принял оферту, показываем её
    if not user.accepted_offer:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Я согласен", callback_data="offer_accept"),
                    InlineKeyboardButton(text="❌ Не согласен", callback_data="offer_decline")
                ]
            ]
        )

        await callback.message.answer(_(mt.OFFER), reply_markup=keyboard, parse_mode="HTML")
    else:
        # Если оферта уже принята, продолжаем как обычно
        if user.profile:
            await menu(callback.from_user.id)
        else:
            keyboard = create_profile_kb(user.language)
            await callback.message.answer(_(mt.WELCOME), reply_markup=keyboard)