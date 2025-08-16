import json

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from bot.loader import _

from aiogram.types import Message


import bot.app.filters.create_profile_filtres as filters
from bot.app.routers import dating_router
from bot.database.models.user import UserModel
from bot.database.services import Profile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.app.business.profile_service import send_profile
from bot.app.keyboards.default.registration_form import profile_menu_kb

from bot.app.text import message_text as mt


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
async def _create_profile_command(message: types.Message, session: AsyncSession, user: UserModel):
    data = json.loads(message.web_app_data.data)
    profile = normalize_profile_data(data)
    await Profile.create_or_update(
        session=session,
        id=user.id,
        **profile,
    )
    await session.refresh(user)

    await message.answer(_(mt.PRFILE_SUCCESSFULLY_CREATED), reply_markup=ReplyKeyboardRemove())

    keyboard = profile_menu_kb(user.language, user.profile)
    await send_profile(session, message.from_user.id, user.profile, user.language)
    await message.answer(mt.PROFILE_MENU, reply_markup=keyboard)


def _to_int(v):
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None

def _to_bool_or_none(v):
    if v is True or v is False:
        return v

    if isinstance(v, str):
        if v.lower() in ("true", "1", "yes", "да"):
            return True
        if v.lower() in ("false", "0", "no", "нет"):
            return False
        if v == "":
            return None

    return None


def _none_if_empty(v):
    return None if (v is None or (isinstance(v, str) and v.strip() == "")) else v

def normalize_profile_data(data: dict) -> dict:
    # если у вас действительно нужны мапы на «допустимые» значения — оставьте ИХ,
    # но на вход им подавайте строки, а не bool/int
    gender = data.get("gender")
    education = data.get("education")
    goal = data.get("goal")
    religious_level = _none_if_empty(data.get("religious_level"))

    # Пример безопасных мапов (если нужны):
    if hasattr(filters, "gender_map"):
        gender = filters.gender_map.get(gender, gender)
    if hasattr(filters, "education_map"):
        education = filters.education_map.get(education, education)
    if hasattr(filters, "goal_map"):
        goal = filters.goal_map.get(goal, goal)
    if hasattr(filters, "religious_level_map") and religious_level is not None:
        religious_level = filters.religious_level_map.get(religious_level, religious_level)

    return {
        "name": _none_if_empty(data.get("name")),
        "age": _to_int(data.get("age")),
        "gender": gender,
        "city_id": _to_int(data.get("city")),
        "height": _to_int(data.get("height")),
        "weight": _to_int(data.get("weight")),
        "marital_status_id": _to_int(data.get("marital_status")),
        "has_children": bool(data.get("has_children")) if isinstance(data.get("has_children"), bool) else _to_bool_or_none(data.get("has_children")),
        "education": education,
        "goal": goal,
        "polygamy": _to_bool_or_none(data.get("polygamy")),   # nullable=True
        "religion_id": _to_int(data.get("religion")),
        "religious_level": religious_level,                   # nullable=True
        "ethnicity_id": _to_int(data.get("ethnicity")),
        "job": _none_if_empty(data.get("job")),
        "about": _none_if_empty(data.get("about")),
        "looking_for": _none_if_empty(data.get("looking_for")),
    }
