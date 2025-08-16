from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.loader import _

from bot.app.text import message_text as mt


def report_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔞"), KeyboardButton(text="💰"), KeyboardButton(text="🔫")],
            [KeyboardButton(text=_(mt.KB_BACK))],
        ],
    )
    return kb
