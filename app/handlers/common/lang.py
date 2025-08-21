from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import I18n
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.menu_service import menu
from app.keyboards.default.registration_form import create_profile_kb
from app.keyboards.inline.lang import LangCallback, lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import User
from loader import i18n  # сам экземпляр I18n, не gettext-алиас _

def normalize_lang(code: str | None, default: str = "ru") -> str:
    if not code:
        return default
    return code.split("-")[0].lower()

@common_router.message(StateFilter(None), Command("language"))
@common_router.message(StateFilter(None), Command("lang"))
async def _lang(message: types.Message) -> None:
    await message.answer(mt.CHANGE_LANG,  reply_markup=lang_ikb())

@common_router.callback_query(StateFilter(None), LangCallback.filter())
async def _change_lang(
    callback: types.CallbackQuery,
    callback_data: LangCallback,
    user: UserModel,
    session: AsyncSession,
) -> None:
    # 1) нормализуем и сохраняем
    language = normalize_lang(callback_data.lang)
    await User.update(session=session, id=user.id, language=language)
    await session.commit()

    # 2) обновляем runtime-состояние
    user.language = language  # или: await session.refresh(user)

    # 3) переключаем i18n-контекст на этот апдейт
    i18n.ctx_locale.set(language)

    # важно: уберём «часики» у коллбэка
    await callback.answer()

    # Обновляем текст
    await callback.message.edit_text(mt.DONE_CHANGE_LANG(language))

    if not user.accepted_offer:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text=mt.OFFER_ACCEPT(language), callback_data="offer_accept"),
                InlineKeyboardButton(text=mt.OFFER_NOT_ACCEPT(language), callback_data="offer_decline"),
            ]]
        )
        # Без _(), т.к. mt.* уже локализован по language
        await callback.message.answer(mt.OFFER(language), reply_markup=keyboard, parse_mode="HTML")
    else:
        if user.profile:
            # если menu() само вытягивает user из БД — ок,
            # иначе пробрось language внутрь, если нужно
            await menu(callback.from_user.id)
        else:
            # используем СВЕЖИЙ language, не "user.language" из прошлого апдейта
            keyboard = create_profile_kb(language)
            await callback.message.answer(mt.WELCOME, reply_markup=keyboard)
