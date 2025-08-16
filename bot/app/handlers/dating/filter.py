import json

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.types import ReplyKeyboardRemove

from bot.app.business.filter_service import send_filter
from bot.app.handlers.dating.create_profile import WebAppActionFilter
from bot.loader import _

import bot.app.filters.create_profile_filtres as filters

from bot.app.routers import dating_router
from bot.app.text import message_text as mt
from bot.database.models import UserModel
from bot.database.services import Filter
from bot.app.keyboards.default.search import search_kb


@dating_router.message(WebAppActionFilter("filter_submit"))
async def _create_filter_command(message: types.Message, session, user: UserModel):
    data = json.loads(message.web_app_data.data)
    filter = normalize_filter_data(data)
    await Filter.create_or_update(
        session=session,
        id=user.id,
        **filter,
    )

    await session.refresh(user)

    await message.answer(text=_(mt.FILTER_SUCCESSFULLY_ADDED), reply_markup=ReplyKeyboardRemove())
    await send_filter(session, message.from_user.id, user)

def normalize_filter_data(data: dict) -> dict:
    def to_int(value):
        return int(value) if value not in (None, '', ' ') else None

    return {
        "city_id": to_int(data.get("city")),
        "age_from": to_int(data.get("age_from")),
        "age_to": to_int(data.get("age_to")),
        "height_from": to_int(data.get("height_from")),
        "height_to": to_int(data.get("height_to")),
        "weight_from": to_int(data.get("weight_from")),
        "weight_to": to_int(data.get("weight_to")),
        "has_children": (
            filters.yes_no_map.get(data.get("has_children"))
            if data.get("has_children") not in (None, "", " ")
            else None
        ),
        "goal": filters.goal_map.get(data.get("goal"), data.get("goal")),
        "ethnicity_id": to_int(data.get("ethnicity")),
    }


@dating_router.message(StateFilter(None), F.text == _(mt.KB_MY_PROFILE))
async def filter_command(message: types.Message) -> None:
    """Отправляет фильтр пользователя"""
    keyboard = search_kb()
    await message.answer(mt.PROFILE_MENU, reply_markup=keyboard)

