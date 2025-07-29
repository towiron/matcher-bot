import json

from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove
from loader import _

from aiogram.types import Message


import app.filters.create_profile_filtres as filters
from app.routers import dating_router
from database.models.user import UserModel
from database.services import Profile
from utils.geopy import get_coordinates

from .profile import profile_command

from app.text import message_text as mt


def WebAppActionFilter(expected_action: str):
    def _filter(message: Message) -> bool:
        if not message.web_app_data:
            return False
        try:
            data = json.loads(message.web_app_data.data)
            return data.get("action") == expected_action
        except Exception:
            return False
    return _filter


@dating_router.message(WebAppActionFilter("profile_submit"))
async def _create_profile_command(message: types.Message, session, user: UserModel):
    data = json.loads(message.web_app_data.data)
    profile = normalize_profile_data(data)
    await Profile.create_or_update(
        session=session,
        id=user.id,
        **profile,
    )

    await session.refresh(user)

    await message.answer(_(mt.PRFILE_SUCCESSFULLY_CREATED), reply_markup=ReplyKeyboardRemove())
    await profile_command(message, user)

def normalize_profile_data(data: dict) -> dict:
    # Попытка получить координаты, если они не указаны, но указан город
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if (latitude is None or longitude is None) and data.get("city"):
        coordinates = get_coordinates(data["city"])
        if coordinates:
            latitude, longitude = coordinates

    return {
        "gender": filters.gender_map.get(data.get("gender"), data.get("gender")),
        "marital_status": filters.marital_status_map.get(data.get("marital_status"), data.get("marital_status")),
        "education": filters.education_map.get(data.get("education"), data.get("education")),
        "goal": filters.goal_map.get(data.get("goal"), data.get("goal")),
        "religion": filters.religion_map.get(data.get("religion"), data.get("religion")),
        "religious_level": filters.religious_level_map.get(data.get("religious_level"), data.get("religious_level")),
        "has_children": filters.yes_no_map.get(data.get("has_children"), data.get("has_children")),
        "polygamy": filters.yes_no_map.get(data.get("polygamy"), data.get("polygamy")),
        "name": data.get("name"),
        "surname": data.get("surname"),
        "age": int(data.get("age")) if data.get("age") is not None else None,
        "city": data.get("city"),
        "latitude": latitude,
        "longitude": longitude,
        "height": int(data.get("height")) if data.get("height") is not None else None,
        "weight": int(data.get("weight")) if data.get("weight") is not None else None,
        "ethnicity": data.get("ethnicity"),
        "job": data.get("job"),
        "about": data.get("about"),
        "looking_for": data.get("looking_for"),
    }