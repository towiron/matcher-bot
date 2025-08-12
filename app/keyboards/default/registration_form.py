from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from data.config import WEB_APP_URL
from database.models.profile import ProfileModel
from loader import _

from app.text import message_text as mt
from urllib.parse import urlencode

def create_profile_kb(language: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_(mt.CREATE_PROFILE),
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/profile?language={language}")
                )
            ]
        ],
        resize_keyboard=True
    )
    return kb

def profile_menu_kb(language: str, profile: ProfileModel) -> ReplyKeyboardMarkup:
    query_string = build_profile_query(profile, language)
    full_url = f"{WEB_APP_URL}/profile?{query_string}"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(mt.KB_FIND_MATCH)),
            ],
            [
                KeyboardButton(
                    text=_(mt.KB_FILL_PROFILE_AGAIN),
                    web_app=WebAppInfo(url=full_url)
                ),
                KeyboardButton(text=_(mt.KB_BACK)),
            ]
        ],
        resize_keyboard=True
    )
    return kb

def build_profile_query(profile: ProfileModel, language: str) -> str:
    query_data = {
        "language": language,
        "name": profile.name,
        "age": profile.age,
        "gender": profile.gender,
        "city_id": profile.city_id,
        "height": profile.height,
        "weight": profile.weight,
        "marital_status_id": profile.marital_status_id,
        "has_children": str(profile.has_children).lower(),  # True → "true"
        "education": profile.education,
        "goal": profile.goal,
        "polygamy": str(profile.polygamy).lower() if profile.polygamy is not None else None,
        "religion_id": profile.religion_id,
        "religious_level": profile.religious_level,
        "ethnicity_id": profile.ethnicity_id,
        "job": profile.job,
        "about": profile.about,
        "looking_for": profile.looking_for,
    }

    # Удалим None значения
    query_data_clean = {k: v for k, v in query_data.items() if v is not None}

    return urlencode(query_data_clean)
