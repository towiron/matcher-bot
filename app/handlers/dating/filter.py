import json

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.types import ReplyKeyboardRemove

from app.business.filter_service import send_filter
from app.handlers.dating.create_profile import WebAppActionFilter
from loader import _

import app.filters.create_profile_filtres as filters

from app.keyboards.default.base import search_kb
from app.routers import dating_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import Filter
from app.keyboards.default.search import search_kb


@dating_router.message(WebAppActionFilter("filter_submit"))
async def _create_profile_command(message: types.Message, session, user: UserModel):
    data = json.loads(message.web_app_data.data)
    filter = normalize_filter_data(data)
    await Filter.create_or_update(
        session=session,
        id=user.id,
        **filter,
    )

    await session.refresh(user)

    await message.answer(_(mt.FILTER_SUCCESSFULLY_ADDED), reply_markup=ReplyKeyboardRemove())
    await send_filter(message.from_user.id, user.filter)

def normalize_filter_data(data: dict) -> dict:
    return {
        "city": data.get("city"),
        "age_from": int(data.get("age_from")) if data.get("age_from") is not None else None,
        "age_to": int(data.get("age_to")) if data.get("age_to") is not None else None,
        "height_from": int(data.get("height_from")) if data.get("height_from") is not None else None,
        "height_to": int(data.get("height_to")) if data.get("height_to") is not None else None,
        "weight_from": int(data.get("weight_from")) if data.get("weight_from") is not None else None,
        "weight_to": int(data.get("weight_to")) if data.get("weight_to") is not None else None,
        "has_children": filters.yes_no_map.get(data.get("has_children"), data.get("has_children")),
        "goal": filters.goal_map.get(data.get("goal"), data.get("goal")),
        "ethnicity": data.get("ethnicity"),
    }


@dating_router.message(StateFilter(None), F.text == _(mt.KB_FIND_MATCH))
async def _search_command(
    message: types.Message, user: UserModel
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=search_kb())
    else:
        await message.answer(mt.FILL_FILTER, reply_markup=search_kb())


@dating_router.message(StateFilter(None), F.text == _(mt.KB_MY_PROFILE))
async def filter_command(message: types.Message) -> None:
    """Отправляет фильтр пользователя"""
    keyboard = search_kb()
    await message.answer(mt.PROFILE_MENU, reply_markup=keyboard)
