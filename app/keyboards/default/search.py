from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from data.config import WEB_APP_URL
from loader import _

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

def search_menu_kb() -> ReplyKeyboardMarkup:
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
