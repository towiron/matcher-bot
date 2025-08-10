from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.business.menu_service import menu
from app.keyboards.inline.lang import lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import User


@common_router.message(StateFilter(None), CommandStart())
async def _start_command(message: types.Message, user: UserModel) -> None:
    """Команда /start с проверкой оферты"""

    if not user.accepted_offer:
        # Оферта и inline-кнопки
        offer_text = """
📄 <b>Пользовательское соглашение</b>

Используя этого бота, вы соглашаетесь с нашими условиями:
- Ваши данные могут быть использованы для предоставления сервиса.
- Вы не должны использовать бота в незаконных целях.

Пожалуйста, подтвердите согласие перед использованием.
"""
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Я согласен", callback_data="offer_accept"),
                    InlineKeyboardButton(text="❌ Не согласен", callback_data="offer_decline")
                ]
            ]
        )

        await message.answer(offer_text, reply_markup=keyboard, parse_mode="HTML")
        return

    # Если пользователь уже принял оферту — продолжаем
    if user.profile:
        await menu(user.id)
    else:
        await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(F.data == "offer_accept")
async def _accept_offer(callback: CallbackQuery, user: UserModel, session):
    await User.update_offer_accepted(session, user.id)  # метод ты уже реализовал
    await callback.message.edit_text("✅ Спасибо! Теперь вы можете пользоваться ботом.")

    # Продолжим с выбора языка (если анкеты нет)
    if not user.profile:
        await callback.message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())
    else:
        await menu(user.id)


@common_router.callback_query(F.data == "offer_decline")
async def _decline_offer(callback: CallbackQuery):
    await callback.message.edit_text("❌ Без согласия с офертой вы не можете использовать бота.")