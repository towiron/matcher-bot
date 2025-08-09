from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from data.config import WEB_APP_URL
from database.models import FilterModel, UserModel
from loader import _
from urllib.parse import urlencode


from app.text import message_text as mt

def search_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_(mt.KB_SEARCH_FILTER),
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/filter")
                ),
                KeyboardButton(
                    text=_(mt.KB_BACK),
                )
            ]
        ],
        resize_keyboard=True
    )
    return kb

def search_menu_kb(user: UserModel) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_(mt.KB_SEARCH_BY_FILTER),
                ),
                KeyboardButton(
                    text=_(mt.KB_SEARCH_BY_AI),
                ),
            ],
            [
                KeyboardButton(
                    text=_(mt.KB_CHANGE_FILTER),
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/filter?{build_filter_query(user.filter, user.language)}")
                ),
                KeyboardButton(
                    text=_(mt.KB_BACK),
                )
            ]
        ],
        resize_keyboard=True
    )
    return kb

def build_filter_query(filter: FilterModel, language: str) -> str:
    params = {
        "language": language,
        "city": filter.city_id,
        "age_from": filter.age_from,
        "age_to": filter.age_to,
        "height_from": filter.height_from,
        "height_to": filter.height_to,
        "weight_from": filter.weight_from,
        "weight_to": filter.weight_to,
        "goal": filter.goal,
        "ethnicity": filter.ethnicity_id,
        "has_children": filter.has_children,
    }
    # Удаляем None
    clean_params = {k: v for k, v in params.items() if v is not None}
    return urlencode(clean_params)
